from __future__ import annotations

from injector import inject

from game.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.ObjectUtils import ObjectUtils
from object.EffectHelper import EffectHelper
from object.ItemUtil import ItemUtil
from object.ObjectMacros import ObjectMacros
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from server.LoggerFactory import LoggerFactory


class ObjectCommands:
    @inject
    def __init__(self, registry_service: RegistryService, object_macros: ObjectMacros, character_macros: CharacterMacros, player_helper: PlayerHelper, effect_helper: EffectHelper):
        self.__name__ = "ObjectCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.object_macros = object_macros
        self.character_macros = character_macros
        self.player_helper = player_helper
        self.item_types = object_macros.ItemTypes
        self.item_flags = object_macros.ItemFlags
        self.wear_flags = character_macros.enums.get("wearFlags")
        self.effect_helper = effect_helper

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

        target_item = None
        container = None
        if rem:
            container = ObjectUtils.find_container(character, room, rem.split()[0])
            if container is None:
                context.finish()
                return {"to_char": "I see no container here.\r\n"}
            if self.object_macros.is_container_closed(container):
                context.finish()
                return {"to_char": "It is closed.\r\n"}
            target_item = ObjectUtils.find_in_contains(container, arg1)
        else:
            target_item = ObjectUtils.find_room_item(room, arg1)

        if target_item is None:
            context.finish()
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
        if self.object_macros.is_container_closed(container):
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
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        if ObjectUtils.is_nodrop(item, self.item_flags):
            context.finish()
            return {"to_char": "You can't let go of it.\r\n"}

        slot = ObjectUtils.equipped_slot_of(character, item)
        if slot:
            self.effect_helper.remove_item_effects(character, item)
            ObjectUtils.unequip_item(character, slot)
        ObjectUtils.remove_from_inventory(character, item)
        room.add_item_to_room(item)
        context.finish()
        return {
            "to_char": f"You drop {ObjectUtils.short(item)}.\r\n",
            "to_room": f"{character.name} drops {ObjectUtils.short(item)}.\r\n",
            "targets": self.player_helper.players_in_room(character, room),
        }

    def do_junk(self, character: Character, context: Context):
        return self.destroy_carried(character, context, "Junk what?\r\n")

    def do_sacrifice(self, character: Character, context: Context):
        return self.destroy_carried(character, context, "Sacrifice what?\r\n", "Mota gives you one silver coin for your sacrifice.\r\n")

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
            self.effect_helper.remove_item_effects(character, item)
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
        victim = ObjectUtils.find_character_in_room(room, character, rem.split()[0])
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
            self.effect_helper.remove_item_effects(character, item)
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
        if not arg1:
            context.finish()
            return {"to_char": "Wear what?\r\n"}
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        slot = ObjectUtils.find_wear_slot(character, item, self.wear_flags, forced=rem.split()[0] if rem else "")
        if slot is None:
            context.finish()
            return {"to_char": "You can't wear that there.\r\n"}
        ObjectUtils.equip_item(character, item, slot)
        self.effect_helper.apply_item_effects(character, item)
        context.finish()
        return {"to_char": f"You wear {ObjectUtils.short(item)}.\r\n"}

    def do_wield(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "wielded", "Wield what?\r\n")

    def do_hold(self, character: Character, context: Context):
        return self.equip_to_slot(character, context, "held", "Hold what?\r\n")

    def equip_to_slot(self, character: Character, context: Context, slot: str, empty_msg: str):
        arg1, _ = ObjectUtils.parse_raw_arguments(context.result, context.parameters)
        if not arg1:
            context.finish()
            return {"to_char": empty_msg}
        item = ObjectUtils.find_inventory_item(character, arg1)
        if item is None:
            context.finish()
            return {"to_char": "You do not have that item.\r\n"}
        equipped = ObjectUtils.ensure_equipped(character)
        if getattr(equipped, slot, None) is not None:
            context.finish()
            return {"to_char": "Your hands are full.\r\n"}
        ObjectUtils.equip_item(character, item, slot)
        self.effect_helper.apply_item_effects(character, item)
        context.finish()
        return {"to_char": f"You equip {ObjectUtils.short(item)}.\r\n"}

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
            self.effect_helper.remove_item_effects(character, item)
            context.finish()
            return {"to_char": f"You stop using {ObjectUtils.short(item)}.\r\n"}

        for slot, item in equipped.__dict__.items():
            if item is None:
                continue
            name = (getattr(item, "name", "") or "").lower()
            if name == arg1 or name.startswith(arg1):
                self.effect_helper.remove_item_effects(character, item)
                ObjectUtils.unequip_item(character, slot)
                context.finish()
                return {"to_char": f"You stop using {ObjectUtils.short(item)}.\r\n"}
        context.finish()
        return {"to_char": "You aren't wearing that.\r\n"}

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
            self.effect_helper.remove_item_effects(character, item)
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
