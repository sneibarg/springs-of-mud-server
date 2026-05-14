import asyncio
import random

from enum import IntEnum

from injector import inject
from area.AreaHandler import AreaHandler
from fight.CombatRegistry import CombatRegistry
from fight.FightHandler import FightHandler
from game.GameMacros import GameMacros
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from game.WeatherHandler import WeatherHandler
from mobile.MobileHandler import MobileHandler
from util.EffectUtil import EffectUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.CharacterService import CharacterService
from server.messaging.MessageBus import MessageBus
from server.session.SessionHandler import SessionHandler


class UpdateHandler:
    @inject
    def __init__(self,
                 weather_handler: WeatherHandler,
                 area_handler: AreaHandler,
                 mobile_handler: MobileHandler,
                 fight_handler: FightHandler,
                 message_bus: MessageBus,
                 registry_service: RegistryService,
                 character_service: CharacterService,
                 session_handler: SessionHandler):
        self.weather_handler = weather_handler
        self.area_handler = area_handler
        self.mobile_handler = mobile_handler
        self.fight_handler = fight_handler
        self.message_bus = message_bus
        self.character_service = character_service
        self.session_handler = session_handler
        self.character_registry = registry_service.character_registry
        self.area_registry = registry_service.area_registry
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.combat_registry: CombatRegistry = registry_service.combat_registry
        self.enums: dict[str, IntEnum] = {}
        self.pulse_area = 0
        self.pulse_mobile = 0
        self.pulse_violence = 0
        self.pulse_point = 0
        self.pulse_music = 0  # maybe we skip migrating music
        self.save_cycle = 30
        self.save_number = 0
        self.GameParametersEnum = None
        self.PositionsEnum = None
        self.ItemTypes = None
        self.WearLocation = None
        self.WearFlags = None

    def set_enums(self, enums: dict[str, IntEnum]):
        def _macro_enum(enum_name: str):
            try:
                return CharacterMacros.get_enum(enum_name)
            except RuntimeError:
                return None

        self.enums = enums
        self.GameParametersEnum = _macro_enum("gameParameters") or enums.get('gameParameters')
        self.PositionsEnum = _macro_enum("positions") or enums.get('positions')
        self.ItemTypes = _macro_enum("itemTypes") or enums.get('itemTypes')
        self.WearLocation = _macro_enum("wearLocation") or enums.get('wearLocation')
        self.WearFlags = _macro_enum("wearFlags") or enums.get('wearFlags')
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
            self._refresh_combat_registry_from_world()
            await self._violence_update()
        await self._aggr_update()

    def _refresh_combat_registry_from_world(self):
        active_keys: set[tuple[str, str, str]] = set()

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for attacker in room.people():
                defender = getattr(attacker, "fighting", None)
                if defender is None:
                    continue
                attacker_id = str(getattr(attacker, "id", "") or "")
                defender_id = str(getattr(defender, "id", "") or "")
                if not attacker_id or not defender_id:
                    self.fight_handler.stop_fighting(attacker, both=False)
                    continue
                if room.find_entity_in_room(defender_id) is None:
                    self.fight_handler.stop_fighting(attacker, both=False)
                    continue
                key = (attacker_id, defender_id, str(room.id))
                active_keys.add(key)
                self.combat_registry.upsert(attacker_id, defender_id, room.id)

        self.combat_registry.retain_keys(active_keys)

    async def _violence_update(self):
        try:
            positions_enum = CharacterMacros.get_enum("positions")
        except RuntimeError:
            positions_enum = self.PositionsEnum
        if positions_enum is None:
            return

        prompted_characters: dict[str, Character] = {}
        events = list(self.combat_registry.all_events())
        decorated_events = []
        for index, event in enumerate(events):
            room = self.room_registry.get_or_none(id=event.room_id)
            attacker = room.find_entity_in_room(event.attacker_id) if room is not None else None
            decorated_events.append((0 if (attacker is not None and CharacterMacros.is_npc(attacker)) else 1, index, event))

        for _, _, event in sorted(decorated_events, key=lambda item: (item[0], item[1])):
            room = self.room_registry.get_or_none(id=event.room_id)
            if room is None:
                self.combat_registry.remove_by_id(event.id)
                continue

            attacker = room.find_entity_in_room(event.attacker_id)
            defender = room.find_entity_in_room(event.defender_id)
            if attacker is None or defender is None:
                self.combat_registry.remove_by_id(event.id)
                continue

            if not CharacterMacros.is_awake(attacker):
                self.fight_handler.stop_fighting(attacker, both=False)
                continue

            # ROM fight.c parity: if awake and in same room then multi_hit(), else stop_fighting().
            if room.find_entity_in_room(event.defender_id) is None:
                self.fight_handler.stop_fighting(attacker, both=False)
                continue

            result = self.fight_handler.multi_hit(attacker, defender, dt="TYPE_UNDEFINED")
            payload = self.fight_handler.build_round_payload(attacker, defender, room, result)
            prompted = await self._emit_combat_payload(attacker, payload)
            prompted_characters.update({character.id: character for character in prompted})
            if getattr(attacker, "fighting", None) is not None:
                self.fight_handler.check_assist(attacker, defender)

        for character in prompted_characters.values():
            room = self.room_registry.get_or_none(id=character.room_id)
            area = self.area_registry.get_or_none(id=getattr(room, "area_id", getattr(character, "area_id", ""))) if room is not None else self.area_registry.get_or_none(id=character.area_id)
            if room is not None and area is not None:
                await self.message_bus.send_prompt(character, area, room)

    async def _emit_combat_payload(self, attacker, payload: dict) -> list[Character]:
        prompted: list[Character] = []
        if not isinstance(payload, dict):
            return prompted

        if payload.get("to_char") and not CharacterMacros.is_npc(attacker):
            await self.message_bus.send_to_character(attacker.id, self.message_bus.text_to_message(payload["to_char"]))
            prompted.append(attacker)
        if payload.get("to_victim") and payload.get("victim") is not None and not CharacterMacros.is_npc(payload["victim"]):
            await self.message_bus.send_to_character(payload["victim"].id, self.message_bus.text_to_message(payload["to_victim"]))
            prompted.append(payload["victim"])
        if payload.get("to_room"):
            targets = payload.get("targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)
        return prompted

    async def _aggr_update(self):
        prompted_characters: dict[str, Character] = {}
        for room in self.room_registry.all_rooms():
            if room is None:
                continue

            for attacker, payload in self.fight_handler.aggressive_room_rounds(room):
                prompted = await self.fight_handler.emit_round_payload(attacker, payload)
                prompted_characters.update({victim.id: victim for victim in prompted})

        for character in prompted_characters.values():
            room = self.room_registry.get_or_none(id=character.room_id)
            area = self.area_registry.get_or_none(id=getattr(room, "area_id", getattr(character, "area_id", ""))) if room is not None else self.area_registry.get_or_none(id=character.area_id)
            if room is not None and area is not None:
                await self.message_bus.send_prompt(character, area, room)

    async def char_update(self):
        if self.PositionsEnum is None:
            return

        self._advance_save_counter()
        pos_stunned = self.PositionsEnum.POS_STUNNED.value
        for ch in self._active_player_characters():
            await self._tick_conditions(ch)
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

        await self._autosave_due_characters()

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

    def _advance_save_counter(self) -> None:
        self.save_number += 1
        if self.save_number >= self.save_cycle:
            self.save_number = 0

    async def _autosave_due_characters(self) -> None:
        due = [
            character for character in self._active_player_characters()
            if self._autosave_bucket(character.id) == self.save_number
        ]
        if not due:
            return

        await asyncio.gather(*[
            asyncio.to_thread(self.character_service.save_character, character)
            for character in due
        ])

    def _active_player_characters(self) -> list[Character]:
        active: list[Character] = []
        seen: set[str] = set()
        for session in self.session_handler.get_playing_sessions():
            character = getattr(session, "character", None)
            if not isinstance(character, Character):
                continue
            character_id = str(getattr(character, "id", "") or "")
            if not character_id or character_id in seen:
                continue
            seen.add(character_id)
            active.append(character)
        return active

    def _autosave_bucket(self, character_id: str) -> int:
        if self.save_cycle <= 0:
            return 0
        return sum(str(character_id).encode("utf-8")) % self.save_cycle

    async def _tick_conditions(self, entity) -> None:
        if not isinstance(entity, Character):
            return
        if CharacterMacros.is_npc(entity) or CharacterMacros.is_immortal(entity):
            return

        await self._gain_condition(entity, "drunk", -1)
        await self._gain_condition(entity, "thirst", -1)
        await self._gain_condition(entity, "hunger", -2 if self._is_large_race(entity) else -1)

    async def _gain_condition(self, character: Character, condition_name: str, value: int) -> None:
        if value == 0:
            return

        status_flags = getattr(character, "status_flags", None)
        if status_flags is None or not hasattr(status_flags, condition_name):
            return

        current = GenericUtil.to_int(getattr(status_flags, condition_name, -1), -1)
        if current == -1:
            return

        updated = max(0, min(48, current + value))
        setattr(status_flags, condition_name, updated)
        if updated != 0:
            return

        message = None
        if condition_name == "hunger":
            message = "You are hungry.\r\n"
        elif condition_name == "thirst":
            message = "You are thirsty.\r\n"
        elif condition_name == "drunk" and current != 0:
            message = "You are sober.\r\n"

        if message:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    def _is_large_race(self, character: Character) -> bool:
        race = getattr(character, "character_race", None)
        raw_size = getattr(race, "size", getattr(character, "size", None))
        if raw_size is None:
            return False

        try:
            size_enum = CharacterMacros.get_enum("size")
        except RuntimeError:
            size_enum = None

        if isinstance(raw_size, str):
            normalized = raw_size.strip().upper()
            if size_enum is not None and hasattr(size_enum, normalized):
                raw_size = getattr(size_enum, normalized).value
            else:
                return normalized in {"SIZE_LARGE", "SIZE_HUGE", "SIZE_GIANT"}

        size_value = GenericUtil.to_int(raw_size, None)
        if size_value is None:
            return False

        if size_enum is not None and hasattr(size_enum, "SIZE_MEDIUM"):
            return size_value > int(size_enum.SIZE_MEDIUM.value)
        return size_value >= 3

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
            EffectUtil.affect_remove(entity, effect)

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
            EffectUtil.affect_remove_obj(item, effect)

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
            in_room = room.players_in_room()
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
            in_room = room.players_in_room()
            if is_float and room is not None:
                await self.message_bus.send_to_room(message, in_room)
            return
        if room is not None:
            in_room = room.players_in_room()
            await self.message_bus.send_to_room(message, in_room)

    @staticmethod
    def _format_item_message(message: str, item) -> str:
        item_name = str(getattr(item, "short_description", "") or getattr(item, "name", "something"))
        return str(message or "").replace("$p", item_name)
