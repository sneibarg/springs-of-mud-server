from __future__ import annotations

from injector import inject

from game.Equipped import Equipped
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from util.ObjectUtil import ObjectUtils
from util.EffectUtil import EffectUtil
from util.ItemUtil import ItemUtil
from object.ObjectMacros import ObjectMacros
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from server.LoggerFactory import LoggerFactory


class ObjectCommands:
    @inject
    def __init__(self, registry_service: RegistryService, player_helper: PlayerHelper):
        self.__name__ = "ObjectCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.player_helper = player_helper
        self.item_types = None
        self.item_flags = None
        self.wear_flags = None

    def lazy_load(self):
        self.item_types = CharacterMacros.get_enum("itemTypes")
        self.item_flags = CharacterMacros.get_enum("itemFlags")
        self.wear_flags = CharacterMacros.get_enum("wearFlags")
        if self.item_types is None or self.item_flags is None or self.wear_flags is None:
            raise ValueError("Failed to load item types, flags, or wear flags")

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
        handlers = {
            "get": self.do_get,
            "put": self.do_put,
            "drop": self.do_drop,
            "junk": self.do_junk,
            "sacrifice": self.do_sacrifice,
            "give": self.do_give,
            "wear": self.do_wear,
            "wield": self.do_wield,
            "hold": self.do_hold,
            "grab": self.do_hold,
            "remove": self.do_remove,
            "drink": self.do_drink,
            "eat": self.do_eat,
            "fill": self.do_fill,
            "pour": self.do_pour,
            "quaff": self.do_quaff,
            "recite": self.do_recite,
            "brandish": self.do_brandish,
            "zap": self.do_zap,
        }
        fn = handlers.get(name)
        if fn is None:
            context.finish()
            return {"to_char": f"{name} is not implemented yet.\r\n"}
        return fn(character, context)

    def do_get(self, character: Character, context: Context):
        arg1, rem = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": "Get what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        container = None
        if rem:
            container = ObjectUtils.find_container(character, room, rem.split()[0])
            if container is None:
                context.finish()
                return {"to_char": "I see no container here.\r\n"}
            if not ItemUtil.is_container_like(container):
                context.finish()
                return {"to_char": "That's not a container.\r\n"}
            if ObjectMacros.is_container_closed(container):
                context.finish()
                return {"to_char": "It is closed.\r\n"}
            if arg1 == "all" or arg1.startswith("all."):
                payload = self._get_all_from_container(character, room, container, arg1)
                context.finish()
                return payload
            target_item = ObjectUtils.find_in_contains(container, arg1)
        else:
            target_item = ObjectUtils.find_room_item(room, arg1)

        if target_item is None:
            context.finish()
            if container is not None:
                return {"to_char": f"I see nothing like that in {ObjectUtils.short(container)}.\r\n"}
            return {"to_char": "I see nothing like that here.\r\n"}

        if not ObjectUtils.item_takeable(target_item, self.wear_flags):
            context.finish()
            return {"to_char": "You can't take that.\r\n"}

        if container is not None:
            ObjectUtils.remove_from_contains(container, target_item)
        else:
            room.remove_item_from_room(target_item)
        ObjectUtils.add_to_inventory(character, target_item)
        context.finish()
        return {
            "to_char": f"You get {ObjectUtils.short(target_item)}.\r\n",
            "to_room": f"{character.name} gets {ObjectUtils.short(target_item)}.\r\n",
            "targets": self.player_helper.players_in_room(character, room),
        }

    def _get_all_from_container(self, character: Character, room, container, arg1: str):
        wanted = ""
        if arg1.startswith("all."):
            wanted = arg1[4:].strip().lower()

        picked = []
        for obj in list(getattr(container, "contains", []) or []):
            name = str(getattr(obj, "name", "") or "").strip().lower()
            if wanted and wanted not in name.split() and not name.startswith(wanted):
                continue
            if not ObjectUtils.item_takeable(obj, self.wear_flags):
                continue
            ObjectUtils.remove_from_contains(container, obj)
            ObjectUtils.add_to_inventory(character, obj)
            picked.append(obj)

        if not picked:
            if wanted:
                return {"to_char": f"I see nothing like that in {ObjectUtils.short(container)}.\r\n"}
            return {"to_char": f"I see nothing in {ObjectUtils.short(container)}.\r\n"}

        return {
            "to_char": "".join(f"You get {ObjectUtils.short(obj)} from {ObjectUtils.short(container)}.\r\n" for obj in picked),
            "to_room": "".join(f"{character.name} gets {ObjectUtils.short(obj)} from {ObjectUtils.short(container)}.\r\n" for obj in picked),
            "targets": self.player_helper.players_in_room(character, room),
        }

    def do_put(self, character: Character, context: Context):
        arg1, rem = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1 or not rem:
            context.finish()
            return {"to_char": "Put what in what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}

        obj = ObjectUtils.find_inventory_item(character, arg1)
        if obj is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        container = ObjectUtils.find_container(character, room, rem.split()[0])
        if container is None:
            context.finish()
            return {"to_char": "I see no container here.\r\n"}
        if not ObjectUtils.is_container(container):
            context.finish()
            return {"to_char": "That's not a container.\r\n"}
        if ObjectMacros.is_container_closed(container):
            context.finish()
            return {"to_char": "It is closed.\r\n"}
        if obj is container:
            context.finish()
            return {"to_char": "You can't fold it into itself.\r\n"}

        ObjectUtils.remove_from_inventory(character, obj)
        ObjectUtils.add_to_contains(container, obj)
        context.finish()
        return {
            "to_char": f"You put {ObjectUtils.short(obj)} in {ObjectUtils.short(container)}.\r\n",
            "to_room": f"{character.name} puts {ObjectUtils.short(obj)} in {ObjectUtils.short(container)}.\r\n",
            "targets": self.player_helper.players_in_room(character, room),
        }

    def do_drop(self, character: Character, context: Context):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": "Drop what?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        if arg1 == "all" or arg1.startswith("all."):
            payload = self._drop_all(character, room, arg1)
            context.finish()
            return payload
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        if ObjectUtils.is_nodrop(item, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}

        payload = self._drop_one(character, room, item)
        context.finish()
        return payload

    def _drop_all(self, character: Character, room, arg1: str):
        wanted = arg1[4:].strip().lower() if arg1.startswith("all.") else ""
        dropped = []
        room_lines = []
        char_lines = []

        for item in list(getattr(character, "loot", []) or []):
            if ObjectUtils.equipped_slot_of(character, item):
                continue
            if ObjectUtils.is_nodrop(item, self.item_flags):
                continue
            name = str(getattr(item, "name", "") or "").strip().lower()
            if wanted and wanted not in name.split() and not name.startswith(wanted):
                continue
            payload = self._drop_one(character, room, item)
            dropped.append(item)
            char_lines.append(payload.get("to_char", ""))
            room_lines.append(payload.get("to_room", ""))

        if not dropped:
            if wanted:
                return {"to_char": f"You are not carrying any {wanted}.\r\n"}
            return {"to_char": "You are not carrying anything.\r\n"}

        return {
            "to_char": "".join(char_lines),
            "to_room": "".join(room_lines),
            "targets": self.player_helper.players_in_room(character, room),
        }

    def _drop_one(self, character: Character, room, item):
        slot = ObjectUtils.equipped_slot_of(character, item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            ObjectUtils.unequip_item(character, slot)
        ObjectUtils.remove_from_inventory(character, item)

        if self._melts_on_drop(item):
            return {
                "to_char": f"You drop {ObjectUtils.short(item)}.\r\n{ObjectUtils.short(item)} dissolves into smoke.\r\n",
                "to_room": f"{character.name} drops {ObjectUtils.short(item)}.\r\n{ObjectUtils.short(item)} dissolves into smoke.\r\n",
            }

        room.add_item_to_room(item)
        return {
            "to_char": f"You drop {ObjectUtils.short(item)}.\r\n",
            "to_room": f"{character.name} drops {ObjectUtils.short(item)}.\r\n",
        }

    def _melts_on_drop(self, item) -> bool:
        if not hasattr(self.item_flags, "ITEM_MELT_DROP"):
            return False
        return ObjectUtils.has_flag(getattr(item, "extra_flags", 0), self.item_flags.ITEM_MELT_DROP.value)

    def do_junk(self, character: Character, context: Context):
        return self.destroy_carried(character, context, "Junk what?\r\n")

    def do_sacrifice(self, character: Character, context: Context):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1 or arg1.lower() == str(getattr(character, "name", "") or "").strip().lower():
            context.finish()
            return {
                "to_char": "Mota appreciates your offer and may accept it later.\r\n",
                "to_room": f"{character.name} offers themselves to Mota, who graciously declines.\r\n",
                "targets": self.player_helper.players_in_room(character, room),
            }

        item = ObjectUtils.find_room_item(room, arg1) if room is not None else None
        if item is None:
            context.finish()
            return {"to_char": "You can't find it.\r\n"}
        if ObjectUtils.is_pc_corpse(item) and list(getattr(item, "contains", []) or []):
            context.finish()
            return {"to_char": "Mota wouldn't like that.\r\n"}
        if not ObjectUtils.item_takeable(item, self.wear_flags) or ObjectUtils.is_nosac(item, self.item_flags):
            context.finish()
            return {"to_char": f"{ObjectUtils.short(item)} is not an acceptable sacrifice.\r\n"}

        for occupant in list(getattr(room, "characters", {}).values()) + list(getattr(room, "mobiles", {}).values()) if room is not None else []:
            if getattr(occupant, "on", None) is item:
                name = getattr(occupant, "short_description", None) or getattr(occupant, "name", "Someone")
                context.finish()
                return {"to_char": f"{name} appears to be using {ObjectUtils.short(item)}.\r\n"}

        silver = ObjectUtils.sacrifice_silver_value(item)
        room.remove_item_from_room(item)
        character.silver = int(getattr(character, "silver", 0) or 0) + silver
        context.finish()
        return {
            "to_char": ObjectUtils.sacrifice_reward_message(silver),
            "to_room": f"{character.name} sacrifices {ObjectUtils.short(item)} to Mota.\r\n",
            "targets": self.player_helper.players_in_room(character, room),
        }

    def destroy_carried(self, character: Character, context: Context, empty_msg: str, success_msg: str = "Ok.\r\n"):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        if not arg1:
            context.finish()
            return {"to_char": empty_msg}
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        if ObjectUtils.is_nodrop(item, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}
        slot = ObjectUtils.equipped_slot_of(character, item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            ObjectUtils.unequip_item(character, slot)
        ObjectUtils.remove_from_inventory(character, item)
        context.finish()
        return {"to_char": success_msg}

    def do_give(self, character: Character, context: Context):
        arg1, rem = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1 or not rem:
            context.finish()
            return {"to_char": "Give what to whom?\r\n"}
        if room is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        victim = room.find_character_in_room(character, rem.split()[0])
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        if ObjectUtils.is_nodrop(item, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}

        slot = ObjectUtils.equipped_slot_of(character, item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            ObjectUtils.unequip_item(character, slot)
        ObjectUtils.remove_from_inventory(character, item)
        ObjectUtils.add_to_inventory(victim, item)
        context.finish()
        return {
            "to_char": f"You give {ObjectUtils.short(item)} to {victim.name}.\r\n",
            "to_victim": f"{character.name} gives you {ObjectUtils.short(item)}.\r\n",
            "victim": victim,
            "to_room": f"{character.name} gives {ObjectUtils.short(item)} to {victim.name}.\r\n",
            "targets": self.player_helper.players_in_room(character, room),
        }

    def do_wear(self, character: Character, context: Context):
        arg1, rem = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": "Wear, wield, or hold what?\r\n"}
        if arg1 == "all":
            payload = self._wear_all(character, room)
            context.finish()
            return payload
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        forced_slot = rem.split()[0] if rem else ""
        invalid_msg = "You can't wear that there.\r\n" if forced_slot else "You can't wear, wield, or hold that.\r\n"
        payload = self._wear_item(character, item, room, replace=True, forced_slot=forced_slot, invalid_msg=invalid_msg)
        context.finish()
        return payload

    def do_wield(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "wielded", "Wield what?\r\n", "You can't wield that.\r\n")

    def do_hold(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "held", "Hold what?\r\n", "You can't hold that.\r\n")

    def equip_to_slot(self, character: Character, context: Context, slot: str, empty_msg: str, invalid_msg: str):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": empty_msg}
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        payload = self._wear_item(character, item, room, replace=True, preferred_slot=slot, invalid_msg=invalid_msg)
        context.finish()
        return payload

    def do_remove(self, character: Character, context: Context):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        if not arg1:
            context.finish()
            return {"to_char": "Remove what?\r\n"}
        equipped = ObjectUtils.ensure_equipped(character)

        # Match by slot name first, then item name.
        if hasattr(equipped, arg1):
            item = ObjectUtils.unequip_item(character, arg1)
            if item is None:
                context.finish()
                return {"to_char": "You aren't wearing that.\r\n"}
            EffectUtil.remove_item_effects(character, item)
            context.finish()
            return {"to_char": f"You stop using {ObjectUtils.short(item)}.\r\n"}

        for slot, item in equipped.__dict__.items():
            if item is None:
                continue
            name = (getattr(item, "name", "") or "").lower()
            if name == arg1 or name.startswith(arg1):
                EffectUtil.remove_item_effects(character, item)
                ObjectUtils.unequip_item(character, slot)
                context.finish()
                return {"to_char": f"You stop using {ObjectUtils.short(item)}.\r\n"}
        context.finish()
        return {"to_char": "You aren't wearing that.\r\n"}

    def _wear_all(self, character: Character, room):
        char_lines = []
        room_lines = []

        for item in list(getattr(character, "loot", []) or []):
            payload = self._wear_item(character, item, room, replace=False)
            if not isinstance(payload, dict):
                continue
            if payload.get("to_char"):
                char_lines.append(payload["to_char"])
            if payload.get("to_room"):
                room_lines.append(payload["to_room"])

        result = {"to_char": "".join(char_lines)}
        if room_lines and room is not None:
            result["to_room"] = "".join(room_lines)
            result["targets"] = self.player_helper.players_in_room(character, room)
        return result

    def _wear_item(self, character: Character, item, room, *, replace: bool, preferred_slot: str = "",
                   forced_slot: str = "", invalid_msg: str = "You can't wear, wield, or hold that.\r\n") -> dict:
        level = GenericUtil.to_int(getattr(character, "level", 0), 0)
        item_level = GenericUtil.to_int(getattr(item, "level", 0), 0)
        if level < item_level:
            return Equipped.build_wear_payload(character, room,
                                               to_char=f"You must be level {item_level} to use this object.\r\n",
                                               to_room=f"{character.name} tries to use {ObjectUtils.short(item)}, but is too inexperienced.\r\n")

        equipped = ObjectUtils.ensure_equipped(character)
        slot_groups = equipped.wear_slot_groups_for_item(item, self.wear_flags, preferred_slot=preferred_slot, forced_slot=forced_slot)
        if not slot_groups:
            return {"to_char": invalid_msg if replace else ""}

        char_lines = []
        room_lines = []
        slots = slot_groups[0]
        selected_slot, removed_payload = equipped.resolve_wear_slot(character, slots, replace, can_remove_item=self._can_remove_worn_item, remove_item=self._remove_worn_item)
        if removed_payload:
            if removed_payload.get("to_char"):
                char_lines.append(removed_payload["to_char"])
            if removed_payload.get("to_room"):
                room_lines.append(removed_payload["to_room"])
        if selected_slot is None:
            return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines) if room_lines else "")

        if selected_slot == "shield":
            weapon = getattr(getattr(character, "equipped", None), "wielded", None)
            if weapon is not None and self._character_size(character) < self._large_size_value() and item.is_two_handed_weapon():
                char_lines.append("Your hands are tied up with your weapon!\r\n")
                return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))

        if selected_slot == "wielded" and not item.weapon_too_heavy(character):
            shield = getattr(getattr(character, "equipped", None), "shield", None)
            if shield is not None and self._character_size(character) < self._large_size_value() and item.is_two_handed_weapon():
                char_lines.append("You need two hands free for that weapon.\r\n")
                return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))
        else:
            char_lines.append("It is too heavy for you to wield.\r\n")
            return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))

        ObjectUtils.equip_item(character, item, selected_slot)
        EffectUtil.apply_item_effects(character, item)
        equip_payload = equipped.slot_wear_payload(character, room, item, selected_slot)
        char_lines.append(equip_payload.get("to_char", ""))
        room_lines.append(equip_payload.get("to_room", ""))
        if selected_slot == "wielded":
            skill_feedback = self._weapon_skill_feedback(character, item)
            if skill_feedback:
                char_lines.append(skill_feedback)
        return Equipped.build_wear_payload(character, room, "".join(char_lines), "".join(room_lines))

    def _can_remove_worn_item(self, item) -> bool:
        if not hasattr(self.item_flags, "ITEM_NOREMOVE"):
            return True
        return not ObjectUtils.has_flag(getattr(item, "extra_flags", 0), self.item_flags.ITEM_NOREMOVE.value)

    @staticmethod
    def _remove_worn_item(character: Character, slot: str, item) -> None:
        EffectUtil.remove_item_effects(character, item)
        ObjectUtils.unequip_item(character, slot)

    def _character_size(self, character: Character) -> int:
        direct_size = GenericUtil.to_int(getattr(character, "size", None), None)
        if direct_size is not None:
            return direct_size

        race_name = str(getattr(character, "race", "") or "").strip().lower()
        try:
            race_data = CharacterMacros._pc_races_map().get(race_name, {})
        except RuntimeError:
            race_data = {}
        raw_size = race_data.get("size")
        try:
            size_enum = CharacterMacros.get_enum("size")
        except RuntimeError:
            size_enum = None
        if isinstance(raw_size, str) and size_enum is not None and hasattr(size_enum, raw_size):
            return int(getattr(size_enum, raw_size).value)
        size_value = GenericUtil.to_int(raw_size, None)
        if size_value is not None:
            return size_value
        return self._large_size_value() - 1

    @staticmethod
    def _large_size_value() -> int:
        try:
            size_enum = CharacterMacros.get_enum("size")
        except RuntimeError:
            size_enum = None
        if size_enum is not None and hasattr(size_enum, "SIZE_LARGE"):
            return int(size_enum.SIZE_LARGE.value)
        return 3

    @staticmethod
    def _weapon_skill_feedback(character: Character, item) -> str:
        if CharacterMacros.is_npc(character):
            return ""

        try:
            weapon_class = CharacterMacros.get_enum("weaponClass")
        except RuntimeError:
            weapon_class = None
        if weapon_class is None:
            return ""

        skill_map = {
            getattr(weapon_class, "WEAPON_SWORD", None): "sword",
            getattr(weapon_class, "WEAPON_DAGGER", None): "dagger",
            getattr(weapon_class, "WEAPON_SPEAR", None): "spear",
            getattr(weapon_class, "WEAPON_MACE", None): "mace",
            getattr(weapon_class, "WEAPON_AXE", None): "axe",
            getattr(weapon_class, "WEAPON_FLAIL", None): "flail",
            getattr(weapon_class, "WEAPON_WHIP", None): "whip",
            getattr(weapon_class, "WEAPON_POLEARM", None): "polearm",
        }
        class_value = GenericUtil.to_int(getattr(item, "value0", 0), 0)
        skill_name = ""
        for enum_member, name in skill_map.items():
            if enum_member is not None and class_value == int(enum_member.value):
                skill_name = name
                break
        if not skill_name:
            return ""

        skill = 0
        for entry in list(getattr(character, "skills", []) or []):
            if isinstance(entry, dict):
                entry_name = str(entry.get("name", "")).strip().lower()
                entry_level = entry.get("level", 0)
            else:
                entry_name = str(getattr(entry, "name", "")).strip().lower()
                entry_level = getattr(entry, "level", 0)
            if entry_name == skill_name:
                skill = max(0, min(100, GenericUtil.to_int(entry_level, 0)))
                break

        short = ObjectUtils.short(item)
        if skill >= 100:
            return f"{short} feels like a part of you!\r\n"
        if skill > 85:
            return f"You feel quite confident with {short}.\r\n"
        if skill > 70:
            return f"You are skilled with {short}.\r\n"
        if skill > 50:
            return f"Your skill with {short} is adequate.\r\n"
        if skill > 25:
            return f"{short} feels a little clumsy in your hands.\r\n"
        if skill > 1:
            return f"You fumble and almost drop {short}.\r\n"
        return f"You don't even know which end is up on {short}.\r\n"

    def do_drink(self, character: Character, context: Context):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        item = ObjectUtils.find_inventory_item(character, arg1) if arg1 else None
        if item is None:
            item = ObjectUtils.find_room_item(room, arg1) if arg1 else None
        if item is None:
            context.finish()
            return {"to_char": "Drink what?\r\n"}
        if not ItemUtil.is_drink_container(item):
            context.finish()
            return {"to_char": "You can't drink from that.\r\n"}
        value1 = GenericUtil.to_int(getattr(item, "value1", 0), 0)
        if value1 <= 0:
            context.finish()
            return {"to_char": "It is already empty.\r\n"}
        item.value1 = str(max(0, value1 - 1))
        context.finish()
        return {"to_char": "You take a drink.\r\n"}

    def do_eat(self, character: Character, context: Context):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        if not arg1:
            context.finish()
            return {"to_char": "Eat what?\r\n"}
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        item_type = (getattr(item, "item_type", "") or "").upper()
        if "FOOD" not in item_type and "PILL" not in item_type:
            context.finish()
            return {"to_char": "That's not edible.\r\n"}
        slot = ObjectUtils.equipped_slot_of(character, item)
        if slot:
            EffectUtil.remove_item_effects(character, item)
            ObjectUtils.unequip_item(character, slot)
        ObjectUtils.remove_from_inventory(character, item)
        context.finish()
        return {"to_char": "You eat it.\r\n"}

    def do_fill(self, character: Character, context: Context):
        arg1, rem = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        if not arg1:
            context.finish()
            return {"to_char": "Fill what?\r\n"}
        dest = ObjectUtils.find_inventory_item(character, arg1)
        if dest is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        src_name = rem.split()[0] if rem else ""
        src = ObjectUtils.find_container(character, room, src_name) if src_name else None
        if src is None:
            # fallback to first fountain in room
            src = ObjectUtils.first_fountain(room)
        if src is None:
            context.finish()
            return {"to_char": "There is no source of liquid here.\r\n"}
        if not ItemUtil.is_drink_container(dest) or not ItemUtil.is_drink_container(src):
            context.finish()
            return {"to_char": "You can't fill that.\r\n"}
        dest_cap = GenericUtil.to_int(getattr(dest, "value0", 0), 0)
        src_amt = GenericUtil.to_int(getattr(src, "value1", 0), 0)
        if src_amt <= 0:
            context.finish()
            return {"to_char": "It is empty.\r\n"}
        dest.value1 = str(dest_cap if dest_cap > 0 else src_amt)
        context.finish()
        return {"to_char": "Ok.\r\n"}

    def do_pour(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Pour is not implemented yet.\r\n"}

    def do_quaff(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Quaff is not implemented yet.\r\n"}

    def do_recite(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Recite is not implemented yet.\r\n"}

    def do_brandish(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Brandish is not implemented yet.\r\n"}

    def do_zap(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Zap is not implemented yet.\r\n"}
