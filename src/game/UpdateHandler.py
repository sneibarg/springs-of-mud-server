import random

from enum import IntEnum

from injector import inject
from area.AreaHandler import AreaHandler
from game.GameMacros import GameMacros
from game.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from game.WeatherHandler import WeatherHandler
from mobile.MobileHandler import MobileHandler
from object.EffectUtil import EffectUtil
from player.PlayerHelper import PlayerHelper
from server.messaging.MessageBus import MessageBus


class UpdateHandler:
    @inject
    def __init__(self,
                 player_helper: PlayerHelper,
                 weather_handler: WeatherHandler,
                 area_handler: AreaHandler,
                 mobile_handler: MobileHandler,
                 message_bus: MessageBus,
                 registry_service: RegistryService):
        self.player_helper = player_helper
        self.weather_handler = weather_handler
        self.area_handler = area_handler
        self.mobile_handler = mobile_handler
        self.message_bus = message_bus
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.enums: dict[str, IntEnum] = {}
        self.pulse_area = 0
        self.pulse_mobile = 0
        self.pulse_violence = 0
        self.pulse_point = 0
        self.pulse_music = 0  # maybe we skip migrating music
        self.GameParametersEnum = None
        self.PositionsEnum = None
        self.ItemTypes = None
        self.WearLocation = None
        self.WearFlags = None

    def set_enums(self, enums: dict[str, IntEnum]):
        self.enums = enums
        self.GameParametersEnum = enums.get('gameParameters')
        self.PositionsEnum = enums.get('positions')
        self.ItemTypes = enums.get('itemTypes')
        self.WearLocation = enums.get('wearLocation')
        self.WearFlags = enums.get('wearFlags')
        self.mobile_handler.set_enums(enums)

    async def handle_updates(self):
        self.pulse_area -= 1
        self.pulse_mobile -= 1
        self.pulse_violence -= 1
        self.pulse_point -= 1
        self.pulse_music -= 1

        if self.pulse_area <= 0:
            self.pulse_area = self.GameParametersEnum.PULSE_AREA.value
            self.area_handler.area_update()
        if self.pulse_point <= 0:
            self.pulse_point = self.GameParametersEnum.PULSE_TICK.value
            await self.weather_handler.update()
            await self.char_update()
            await self.obj_update()
        if self.pulse_music <= 0:
            self.pulse_music = self.GameParametersEnum.PULSE_MUSIC.value
        if self.pulse_mobile <= 0:
            self.pulse_mobile = self.GameParametersEnum.PULSE_MOBILE.value
            await self.mobile_handler.mobile_update()
        if self.pulse_violence <= 0:
            self.pulse_violence = self.GameParametersEnum.PULSE_VIOLENCE.value

    async def char_update(self):
        if self.PositionsEnum is None:
            return

        pos_stunned = self.PositionsEnum.POS_STUNNED.value
        for ch in self.character_registry.all_characters():
            attrs = getattr(ch, "character_attributes", None)
            if attrs is None:
                continue
            pos = GenericUtil.to_int(getattr(attrs, "position", 0), 0)
            if pos < pos_stunned:
                await self._tick_effects(ch)
                continue
            self._tick_regen(ch)
            await self._tick_effects(ch)

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for mob in room.mobiles.values():
                pos = GenericUtil.to_int(getattr(mob, "position", getattr(mob, "start_pos", 0)), 0)
                if pos < pos_stunned:
                    await self._tick_effects(mob)
                    continue
                self._tick_regen(mob)
                await self._tick_effects(mob)

    async def obj_update(self):
        if self.ItemTypes is None:
            return

        for item in self._all_world_items():
            await self._tick_item_effects(item)
            timer = GenericUtil.to_int(getattr(item, "timer", -1), -1)
            if timer <= 0:
                continue
            timer -= 1
            item.timer = timer
            if timer > 0:
                continue
            await self._expire_world_item(item)

    @staticmethod
    def _tick_regen(entity):
        max_hit = GenericUtil.to_int(getattr(entity, "max_hit", 0), 0)
        max_mana = GenericUtil.to_int(getattr(entity, "max_mana", 0), 0)
        max_move = GenericUtil.to_int(getattr(entity, "max_movement", 0), 0)

        hit = GenericUtil.to_int(getattr(entity, "hit", 0), 0)
        mana = GenericUtil.to_int(getattr(entity, "mana", 0), 0)
        move = GenericUtil.to_int(getattr(entity, "movement", 0), 0)

        hit_gain = max(1, max_hit // 20) if max_hit > 0 else 0
        mana_gain = max(1, max_mana // 20) if max_mana > 0 else 0
        move_gain = max(1, max_move // 20) if max_move > 0 else 0

        if hit < max_hit:
            setattr(entity, "hit", min(max_hit, hit + hit_gain))
        if mana < max_mana:
            setattr(entity, "mana", min(max_mana, mana + mana_gain))
        if move < max_move:
            setattr(entity, "movement", min(max_move, move + move_gain))

    def _all_world_items(self):
        seen = set()
        items = []

        def walk_item(item):
            if item is None:
                return
            key = id(item)
            if key in seen:
                return
            seen.add(key)
            items.append(item)
            for child in list(getattr(item, "contains", []) or []):
                walk_item(child)

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for obj in room.contents.values():
                walk_item(obj)
            for ch in room.characters.values():
                for obj in list(getattr(ch, "loot", []) or []):
                    walk_item(obj)
                equipped = getattr(ch, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    walk_item(obj)
            for mob in room.mobiles.values():
                for obj in list(getattr(mob, "inventory", []) or []):
                    walk_item(obj)
                equipped = getattr(mob, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    walk_item(obj)

        return items

    async def _expire_world_item(self, item):
        item_type = str(getattr(item, "item_type", "") or "").upper()
        is_pc_corpse = self.ItemTypes is not None and item_type in [self.ItemTypes.ITEM_CORPSE_PC.name]
        is_float = (
            self.WearLocation is not None
            and GenericUtil.to_int(getattr(item, "wear_loc", -1), -1) in [self.WearLocation.WEAR_FLOAT.value]
        )

        location = self._locate_item(item)
        if location is None:
            return

        parent_kind = location["kind"]
        parent = location["parent"]
        container = location["container"]
        room = location.get("room")

        message = self._decay_message(item, is_float=is_float)
        await self._emit_item_decay_message(message, item, parent_kind, parent, room, is_float)

        contents = list(getattr(item, "contains", []) or [])
        if (is_pc_corpse or is_float) and contents:
            for child in contents:
                self._move_child_from_expiring_item(child, parent_kind, parent, container, room)
            item.contains = []

        self._remove_item_at_location(item, parent_kind, parent, container)

    def _move_child_from_expiring_item(self, child, parent_kind: str, parent, container, room):
        if parent_kind == "room":
            parent.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child
            return
        if parent_kind == "char_loot":
            parent.loot.append(child)
            return
        if parent_kind == "mob_inventory":
            parent.inventory.append(child)
            return
        if parent_kind == "item_contains":
            container.append(child)
            return
        if parent_kind == "char_equipped":
            holder = room or self.room_registry.get_or_none(id=getattr(parent, "room_id", ""))
            if holder is not None:
                holder.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child
            return
        if parent_kind == "mob_equipped":
            holder = room
            if holder is not None:
                holder.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child

    @staticmethod
    def _remove_item_at_location(item, parent_kind: str, parent, container):
        if parent_kind == "room":
            parent.contents.pop(getattr(item, "id", ""), None)
            return
        if parent_kind == "char_loot":
            if item in parent.loot:
                parent.loot.remove(item)
            return
        if parent_kind == "mob_inventory":
            if item in parent.inventory:
                parent.inventory.remove(item)
            return
        if parent_kind == "item_contains":
            if item in container:
                container.remove(item)
            return
        if parent_kind in ["char_equipped", "mob_equipped"]:
            equipped = getattr(parent, "equipped", None)
            if equipped is None:
                return
            for slot, equipped_item in getattr(equipped, "__dict__", {}).items():
                if equipped_item is item:
                    setattr(equipped, slot, None)
                    break

    def _locate_item(self, target):
        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for obj in room.contents.values():
                if obj is target:
                    return {"kind": "room", "parent": room, "container": None, "room": room}
                found = self._locate_in_contains(target, obj.contains, room)
                if found is not None:
                    return found

            for ch in room.characters.values():
                for obj in list(getattr(ch, "loot", []) or []):
                    if obj is target:
                        return {"kind": "char_loot", "parent": ch, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains, room)
                    if found is not None:
                        return found

                equipped = getattr(ch, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    if obj is target:
                        return {"kind": "char_equipped", "parent": ch, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains if obj is not None else [], room)
                    if found is not None:
                        return found

            for mob in room.mobiles.values():
                for obj in list(getattr(mob, "inventory", []) or []):
                    if obj is target:
                        return {"kind": "mob_inventory", "parent": mob, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains, room)
                    if found is not None:
                        return found

                equipped = getattr(mob, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    if obj is target:
                        return {"kind": "mob_equipped", "parent": mob, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains if obj is not None else [], room)
                    if found is not None:
                        return found
        return None

    def _locate_in_contains(self, target, container, room):
        for obj in list(container or []):
            if obj is target:
                return {"kind": "item_contains", "parent": None, "container": container, "room": room}
            found = self._locate_in_contains(target, getattr(obj, "contains", []), room)
            if found is not None:
                return found
        return None

    async def _tick_effects(self, entity):
        effects = list(EffectUtil.ensure_effects(entity))
        for idx, effect in enumerate(effects):
            duration = GenericUtil.to_int(getattr(effect, "duration", 0), 0)
            if duration > 0:
                effect.duration = duration - 1
                level = GenericUtil.to_int(getattr(effect, "level", 0), 0)
                if level > 0 and random.randint(0, 4) == 0:
                    effect.level = level - 1
                continue
            if duration < 0:
                continue

            next_effect = effects[idx + 1] if idx + 1 < len(effects) else None
            suppress_msg = (
                next_effect is not None
                and str(getattr(next_effect, "type", "")).strip().lower() == str(getattr(effect, "type", "")).strip().lower()
                and GenericUtil.to_int(getattr(next_effect, "duration", 0), 0) > 0
            )
            if type(entity) is Character and not suppress_msg:
                msg_off = self._lookup_effect_message(getattr(effect, "type", ""), "msg_off")
                if msg_off:
                    await self.message_bus.send_to_character(entity.id, self.message_bus.text_to_message(f"{msg_off}\r\n"))
            EffectUtil.affect_remove(entity, effect, self.enums)

    async def _tick_item_effects(self, item):
        effects = list(EffectUtil.ensure_effects(item))
        for idx, effect in enumerate(effects):
            duration = GenericUtil.to_int(getattr(effect, "duration", 0), 0)
            if duration > 0:
                effect.duration = duration - 1
                level = GenericUtil.to_int(getattr(effect, "level", 0), 0)
                if level > 0 and random.randint(0, 4) == 0:
                    effect.level = level - 1
                continue
            if duration < 0:
                continue

            next_effect = effects[idx + 1] if idx + 1 < len(effects) else None
            suppress_msg = (
                next_effect is not None
                and str(getattr(next_effect, "type", "")).strip().lower() == str(getattr(effect, "type", "")).strip().lower()
                and GenericUtil.to_int(getattr(next_effect, "duration", 0), 0) > 0
            )
            if not suppress_msg:
                msg_obj = self._lookup_effect_message(getattr(effect, "type", ""), "msg_obj")
                if msg_obj:
                    await self._emit_obj_effect_message(item, msg_obj)
            EffectUtil.affect_remove_obj(item, effect, self.enums)

    def _lookup_effect_message(self, effect_type, field_name: str) -> str:
        want = str(effect_type or "").strip().lower()
        if not want:
            return ""

        for spell in self.spell_registry.all_spells():
            candidates = [
                str(getattr(spell, "handler_id", "") or "").strip().lower(),
                str(getattr(spell, "name", "") or "").strip().lower(),
                str(getattr(spell, "id", "") or "").strip().lower(),
            ]
            if want in candidates:
                return str(getattr(spell, field_name, "") or "")

        return ""

    async def _emit_obj_effect_message(self, item, message: str):
        location = self._locate_item(item)
        if location is None:
            return

        parent_kind = location["kind"]
        parent = location["parent"]
        room = location.get("room")
        text = self._format_item_message(message, item)
        if not text:
            return

        if parent_kind in ["char_loot", "char_equipped"]:
            await self.message_bus.send_to_character(parent.id, self.message_bus.text_to_message(text + "\r\n"))
            return
        if room is not None:
            in_room = self.player_helper.players_in_room(parent, room)
            message = self.message_bus.text_to_message(text + "\r\n")
            await self.message_bus.send_to_room(message, in_room)

    def _decay_message(self, item, is_float: bool) -> str:
        item_type = str(getattr(item, "item_type", "") or "").upper()
        if self.ItemTypes is None:
            return "$p crumbles into dust."
        if item_type in [self.ItemTypes.ITEM_FOUNTAIN.name]:
            return "$p dries up."
        if item_type in [self.ItemTypes.ITEM_CORPSE_NPC.name, self.ItemTypes.ITEM_CORPSE_PC.name]:
            return "$p decays into dust."
        if item_type in [self.ItemTypes.ITEM_FOOD.name]:
            return "$p decomposes."
        if item_type in [self.ItemTypes.ITEM_POTION.name]:
            return "$p has evaporated from disuse."
        if item_type in [self.ItemTypes.ITEM_PORTAL.name]:
            return "$p fades out of existence."
        if item_type in [self.ItemTypes.ITEM_CONTAINER.name]:
            if self._can_wear_float(item):
                if list(getattr(item, "contains", []) or []):
                    return "$p flickers and vanishes, spilling its contents on the floor."
                return "$p flickers and vanishes."
            return "$p crumbles into dust."
        return "$p crumbles into dust."

    def _can_wear_float(self, item) -> bool:
        if self.WearFlags is None or not hasattr(self.WearFlags, "ITEM_WEAR_FLOAT"):
            return False
        wear_raw = GameMacros.flags_to_int(getattr(item, "wear_flags", 0))
        return GameMacros.is_set(wear_raw, self.WearFlags.ITEM_WEAR_FLOAT.value)

    async def _emit_item_decay_message(self, message: str, item, parent_kind: str, parent, room, is_float: bool):
        text = self._format_item_message(message, item)
        if not text:
            return

        message = self.message_bus.text_to_message(text + "\r\n")
        if parent_kind in ["char_loot", "char_equipped"]:
            await self.message_bus.send_to_character(parent.id, self.message_bus.text_to_message(text + "\r\n"))
            in_room = self.player_helper.players_in_room(parent, room)
            if is_float and room is not None:
                await self.message_bus.send_to_room(message, in_room)
            return
        if room is not None:
            in_room = self.player_helper.players_in_room(parent, room)
            await self.message_bus.send_to_room(message, in_room)

    @staticmethod
    def _format_item_message(message: str, item) -> str:
        item_name = str(getattr(item, "short_description", "") or getattr(item, "name", "something"))
        return str(message or "").replace("$p", item_name)

