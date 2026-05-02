from __future__ import annotations

from injector import inject

from game.GameMacros import GameMacros
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from util.WizUtil import WizUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from server.LoggerFactory import LoggerFactory


class WizCommands:
    @inject
    def __init__(self, registry_service: RegistryService, player_helper: PlayerHelper):
        self.__name__ = "WizCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.area_registry = registry_service.area_registry
        self.item_registry = registry_service.item_registry
        self.mobile_registry = registry_service.mobile_registry
        self.interp_registry = registry_service.interp_registry
        self.player_helper = player_helper
        self.PlayerActBitsEnum = None
        self.CommFlagsEnum = None
        self.WiznetFlagsEnum = None
        self.PositionsEnum = None

    def lazy_load(self):
        self.PlayerActBitsEnum = CharacterMacros.get_enum("playerActBits")
        self.CommFlagsEnum = CharacterMacros.get_enum("commFlags")
        self.WiznetFlagsEnum = CharacterMacros.get_enum("wiznetFlags")
        self.PositionsEnum = CharacterMacros.get_enum("positions")

    def execute(self, character: Character, context: Context):
        command_name = (getattr(context.command, "name", "") or "").strip().lower()
        argument = WizUtil.argument_text(context.result, context.parameters)

        handlers = {
            "wizhelp": self.do_wizhelp,
            "wiznet": self.do_wiznet,
            "holylight": self.do_holylight,
            "invis": self.do_invis,
            "incognito": self.do_incognito,
            "wizinvis": self.do_invis,
            "poofin": self.do_bamfin,
            "poofout": self.do_bamfout,
            "echo": self.do_echo,
            "gecho": self.do_gecho,
            "zecho": self.do_zecho,
            "pecho": self.do_pecho,
            "goto": self.do_goto,
            "transfer": self.do_transfer,
            "teleport": self.do_transfer,
            "return": self.do_return,
            "nochannels": self.do_nochannels,
            "noemote": self.do_noemote,
            "noshout": self.do_noshout,
            "notell": self.do_notell,
            "freeze": self.do_freeze,
            "restore": self.do_restore,
            "purge": self.do_purge,
            "peace": self.do_peace,
            "mwhere": self.do_mwhere,
            "owhere": self.do_owhere,
            "vnum": self.do_vnum,
            "stat": self.do_stat,
            "load": self.do_load,
            "smote": self.do_smote,
            "sockets": self.do_sockets,
            ":": self.do_immtalk,
            "immtalk": self.do_immtalk,
            "prefix": self.do_prefix,
            "prefi": self.do_prefi,
        }

        handler = handlers.get(command_name)
        if handler is None:
            context.finish()
            return {"to_char": f"{command_name} is not implemented yet.\r\n"}
        return handler(character, context, argument)

    def do_wizhelp(self, character: Character, context: Context, argument: str):
        names = []
        for cmd in self.interp_registry.all_commands():
            if (getattr(cmd, "role", "") or "").strip().lower() == "immortal":
                names.append(str(getattr(cmd, "name", "") or ""))
        names = sorted([name for name in names if name])
        context.finish()
        return {"to_char": "Wizard commands:\r\n" + " ".join(names) + "\r\n"}

    def do_wiznet(self, character: Character, context: Context, argument: str):
        flags = GenericUtil.to_int((character.context or {}).get("WiznetFlagsEnum", 0), 0)
        on_bit = CharacterMacros.enum_bit(self.WiznetFlagsEnum, "WIZ_ON")
        arg = (argument or "").strip().lower()

        if arg in ("", "on"):
            if on_bit:
                flags |= on_bit
            character.context["WiznetFlagsEnum"] = flags
            context.finish()
            return {"to_char": "Welcome to Wiznet!\r\n"}
        if arg == "off":
            if on_bit:
                flags &= ~on_bit
            character.context["WiznetFlagsEnum"] = flags
            context.finish()
            return {"to_char": "Signing off of Wiznet.\r\n"}
        if arg == "status":
            names = []
            for bit_name in CharacterMacros.enum_names(self.WiznetFlagsEnum, "WIZ_"):
                bit = CharacterMacros.enum_bit(self.WiznetFlagsEnum, bit_name)
                if bit and (flags & bit):
                    names.append(bit_name.replace("WIZ_", "").lower())
            off = "off " if on_bit and (flags & on_bit) == 0 else ""
            context.finish()
            return {"to_char": f"Wiznet status:\r\n{off}{' '.join(names)}\r\n"}
        if arg == "show":
            names = [name.replace("WIZ_", "").lower() for name in CharacterMacros.enum_names(self.WiznetFlagsEnum, "WIZ_")]
            context.finish()
            return {"to_char": "Wiznet options available to you are:\r\n" + " ".join(names) + "\r\n"}

        bit_name = f"WIZ_{arg.upper()}"
        bit = CharacterMacros.enum_bit(self.WiznetFlagsEnum, bit_name)
        if bit == 0:
            context.finish()
            return {"to_char": "No such option.\r\n"}
        if (flags & bit) != 0:
            flags &= ~bit
            character.context["WiznetFlagsEnum"] = flags
            context.finish()
            return {"to_char": f"You will no longer see {arg} on wiznet.\r\n"}
        flags |= bit
        character.context["WiznetFlagsEnum"] = flags
        context.finish()
        return {"to_char": f"You will now see {arg} on wiznet.\r\n"}

    def do_holylight(self, character: Character, context: Context, argument: str):
        bit = CharacterMacros.enum_bit(self.PlayerActBitsEnum, "PLR_HOLYLIGHT")
        if bit == 0:
            context.finish()
            return {"to_char": "This feature is unavailable.\r\n"}
        act = GenericUtil.to_int(CharacterMacros.convert_flags(getattr(character.status_flags, "act", "") or "0"), 0)
        if CharacterMacros.is_set(act, bit):
            act = CharacterMacros.unset_bit(act, bit)
            character.status_flags.act = GameMacros.flags_to_letters(act)
            context.finish()
            return {"to_char": "Holy light mode off.\r\n"}
        act = CharacterMacros.set_bit(act, bit)
        character.status_flags.act = GameMacros.flags_to_letters(act)
        context.finish()
        return {"to_char": "Holy light mode on.\r\n"}

    def do_invis(self, character: Character, context: Context, argument: str):
        if not CharacterMacros.is_immortal(character):
            context.finish()
            return {"to_char": "Huh?\r\n"}

        arg = (argument or "").strip()
        level = GenericUtil.to_int(arg, -1) if arg else -1
        if level < 0:
            level = 0 if GenericUtil.to_int(getattr(character.status_flags, "invis_level", 0), 0) > 0 else int(getattr(character, "level", 0))
        max_level = GenericUtil.to_int(CharacterMacros.get_trust(character), int(getattr(character, "level", 0)))
        if level > max_level:
            level = max_level
        character.invis_level = level
        context.finish()
        if level > 0:
            return {"to_char": f"You vanish into thin air (level {level}).\r\n"}
        return {"to_char": "You are now fully visible.\r\n"}

    def do_incognito(self, character: Character, context: Context, argument: str):
        if not CharacterMacros.is_immortal(character):
            context.finish()
            return {"to_char": "Huh?\r\n"}

        arg = (argument or "").strip()
        level = GenericUtil.to_int(arg, -1) if arg else -1
        if level < 0:
            level = 0 if GenericUtil.to_int(getattr(character, "incog_level", 0), 0) > 0 else int(getattr(character, "level", 0))
        max_level = GenericUtil.to_int(CharacterMacros.get_trust(character), int(getattr(character, "level", 0)))
        if level > max_level:
            level = max_level
        character.incog_level = level
        context.finish()
        if level > 0:
            return {"to_char": f"Incognito mode enabled at level {level}.\r\n"}
        return {"to_char": "Incognito mode disabled.\r\n"}

    def do_bamfin(self, character: Character, context: Context, argument: str):
        text = (argument or "").strip()
        if not text:
            text = f"{character.name} appears in a swirling mist."
        character.context["poofin"] = text
        context.finish()
        return {"to_char": "Poofin set.\r\n"}

    def do_bamfout(self, character: Character, context: Context, argument: str):
        text = (argument or "").strip()
        if not text:
            text = f"{character.name} leaves in a swirling mist."
        character.context["poofout"] = text
        context.finish()
        return {"to_char": "Poofout set.\r\n"}

    def do_echo(self, character: Character, context: Context, argument: str):
        if not (argument or "").strip():
            context.finish()
            return {"to_char": "Echo what?\r\n"}
        context.finish()
        return {
            "to_char": f"{argument}\r\n",
            "room_message": f"{argument}\r\n",
            "room_targets": self.player_helper.players_in_room(character, self.room_registry.get_or_none(id=character.room_id)),
        }

    def do_gecho(self, character: Character, context: Context, argument: str):
        if not (argument or "").strip():
            context.finish()
            return {"to_char": "Global echo what?\r\n"}
        context.finish()
        return {
            "to_char": f"{argument}\r\n",
            "broadcast_message": f"{argument}\r\n",
            "exclude_character_ids": [character.id],
        }

    def do_zecho(self, character: Character, context: Context, argument: str):
        if not (argument or "").strip():
            context.finish()
            return {"to_char": "Zone echo what?\r\n"}
        targets = [ch for ch in self.character_registry.all_characters() if str(getattr(ch, "area_id", "")) == str(character.area_id) and ch.id != character.id]
        context.finish()
        return {"to_char": f"{argument}\r\n", "global_message": f"{argument}\r\n", "global_targets": targets}

    def do_pecho(self, character: Character, context: Context, argument: str):
        target_name, message = WizUtil.split_argument(argument)
        if not target_name or not message:
            context.finish()
            return {"to_char": "Pecho whom what?\r\n"}
        victim = self._find_character_world(target_name)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        context.finish()
        return {"to_char": "Ok.\r\n", "victim": victim, "to_victim": f"{message}\r\n"}

    def do_goto(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip()
        if not arg:
            context.finish()
            return {"to_char": "Goto where?\r\n"}
        room = CharacterMacros.find_location(arg, self.room_registry, self.character_registry, WizUtil.name_matches)
        if room is None:
            context.finish()
            return {"to_char": "No such location.\r\n"}
        in_room = self.room_registry.get_or_none(id=character.room_id)
        if in_room is None or room.id == in_room.id:
            context.finish()
            return {"to_char": "Ok.\r\n"}

        character.context["return_room_id"] = in_room.id
        from_targets = self.player_helper.players_in_room(character, in_room)
        in_room.remove_player_from_room(character)
        room.add_player_to_room(character)
        character.room_id = room.id
        character.area_id = room.area_id
        to_targets = self.player_helper.players_in_room(character, room)
        poofout = (character.context or {}).get("poofout", f"{character.name} leaves in a swirling mist.")
        poofin = (character.context or {}).get("poofin", f"{character.name} appears in a swirling mist.")
        context.finish()
        return {
            "from_room_targets": from_targets,
            "from_room_message": f"{poofout}\r\n",
            "to_room_targets": to_targets,
            "to_room_message": f"{poofin}\r\n",
            "to_room_obj": room,
        }

    def do_transfer(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip()
        if not arg:
            context.finish()
            return {"to_char": "Transfer whom (and where)?\r\n"}
        target_name, destination = WizUtil.split_argument(arg)
        victim = self._find_character_world(target_name)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id) if not destination else CharacterMacros.find_location(destination, self.room_registry, self.character_registry, WizUtil.name_matches)
        if room is None:
            context.finish()
            return {"to_char": "No such location.\r\n"}
        source = self.room_registry.get_or_none(id=victim.room_id)
        if source is None:
            context.finish()
            return {"to_char": "They are nowhere.\r\n"}

        from_targets = self.player_helper.players_in_room(victim, source)
        source.remove_player_from_room(victim)
        room.add_player_to_room(victim)
        victim.room_id = room.id
        victim.area_id = room.area_id
        to_targets = self.player_helper.players_in_room(victim, room)
        context.finish()
        return {
            "to_char": "Ok.\r\n",
            "victim": victim,
            "to_victim": f"{character.name} has summoned you.\r\n",
            "from_room_targets": from_targets,
            "from_room_message": f"{victim.name} disappears in a mushroom cloud.\r\n",
            "to_room_targets": to_targets,
            "to_room_message": f"{victim.name} arrives from a puff of smoke.\r\n",
        }

    def do_return(self, character: Character, context: Context, argument: str):
        room_id = (character.context or {}).get("return_room_id")
        if not room_id:
            context.finish()
            return {"to_char": "You have nowhere to return to.\r\n"}
        room = self.room_registry.get_or_none(id=room_id)
        if room is None:
            context.finish()
            return {"to_char": "Return location no longer exists.\r\n"}
        in_room = self.room_registry.get_or_none(id=character.room_id)
        if in_room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        from_targets = self.player_helper.players_in_room(character, in_room)
        in_room.remove_player_from_room(character)
        room.add_player_to_room(character)
        character.room_id = room.id
        character.area_id = room.area_id
        to_targets = self.player_helper.players_in_room(character, room)
        character.context["return_room_id"] = ""
        context.finish()
        return {
            "from_room_targets": from_targets,
            "from_room_message": f"{character.name} vanishes.\r\n",
            "to_room_targets": to_targets,
            "to_room_message": f"{character.name} appears.\r\n",
            "to_room_obj": room,
        }

    def do_nochannels(self, character: Character, context: Context, argument: str):
        return self._toggle_comm_on_target(character, context, argument, "COMM_NOCHANNELS", "NOCHANNELS")

    def do_noemote(self, character: Character, context: Context, argument: str):
        return self._toggle_comm_on_target(character, context, argument, "COMM_NOEMOTE", "NOEMOTE")

    def do_noshout(self, character: Character, context: Context, argument: str):
        return self._toggle_comm_on_target(character, context, argument, "COMM_NOSHOUT", "NOSHOUT")

    def do_notell(self, character: Character, context: Context, argument: str):
        return self._toggle_comm_on_target(character, context, argument, "COMM_NOTELL", "NOTELL")

    def do_freeze(self, character: Character, context: Context, argument: str):
        victim = self._find_character_world((argument or "").strip())
        if victim is None:
            context.finish()
            return {"to_char": "Freeze whom?\r\n"}
        frozen = bool((victim.context or {}).get("frozen", False))
        victim.context["frozen"] = not frozen
        context.finish()
        if frozen:
            return {"to_char": "FREEZE removed.\r\n", "victim": victim, "to_victim": "You can play again.\r\n"}
        return {"to_char": "FREEZE set.\r\n", "victim": victim, "to_victim": "You can't do anything!\r\n"}

    def do_restore(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip().lower()
        if arg == "all":
            for victim in self.character_registry.all_characters():
                CharacterMacros.restore_character(victim)
            context.finish()
            return {"to_char": "All active players restored.\r\n"}

        victim = self._find_character_world(arg)
        if victim is None:
            context.finish()
            return {"to_char": "Restore whom?\r\n"}
        CharacterMacros.restore_character(victim)
        context.finish()
        return {"to_char": "Ok.\r\n", "victim": victim, "to_victim": "You have been restored.\r\n"}

    def do_purge(self, character: Character, context: Context, argument: str):
        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        arg = (argument or "").strip()
        if arg:
            victim = room.find_character_in_room(arg, WizUtil.name_matches)
            if victim is not None and victim.id != character.id:
                room.remove_player_from_room(victim)
                victim.room_id = ""
                context.finish()
                return {"to_char": "Ok.\r\n", "victim": victim, "to_victim": "You are purged!\r\n"}
            item = room.find_item_in_room(arg, WizUtil.name_matches)
            if item is not None:
                room.remove_item_from_room(item)
                context.finish()
                return {"to_char": "Ok.\r\n"}
            context.finish()
            return {"to_char": "They aren't here.\r\n"}

        room.mobiles.clear()
        room.contents.clear()
        context.finish()
        return {"to_char": "Ok.\r\n"}

    def do_peace(self, character: Character, context: Context, argument: str):
        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        for ch in room.characters.values():
            ch.fighting = None
            attrs = getattr(ch, "character_attributes", None)
            if attrs is not None and hasattr(self.PositionsEnum, "POS_STANDING"):
                attrs.position = int(self.PositionsEnum.POS_STANDING.value)
        for mob in room.mobiles.values():
            setattr(mob, "fighting", None)
        context.finish()
        return {"to_char": "Ok.\r\n"}

    def do_mwhere(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip().lower()
        lines = []
        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for mob in room.mobiles.values():
                name = f"{mob.name or ''} {mob.short_description or ''}".strip().lower()
                if not arg or arg in name:
                    lines.append(f"[{mob.vnum}] {mob.short_description} - [{room.vnum}] {room.name}")
        context.finish()
        if not lines:
            return {"to_char": "Nothing like that in heaven or earth.\r\n"}
        return {"to_char": "\r\n".join(lines) + "\r\n"}

    def do_owhere(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Owhere what?\r\n"}
        lines = []
        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for obj in room.contents.values():
                name = (obj.name or obj.short_description or "").lower()
                if arg in name:
                    lines.append(f"[{obj.vnum}] {obj.short_description} - [{room.vnum}] {room.name}")
        context.finish()
        if not lines:
            return {"to_char": "Nothing like that in heaven or earth.\r\n"}
        return {"to_char": "\r\n".join(lines) + "\r\n"}

    def do_vnum(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Vnum what?\r\n"}
        lines = []
        for mob in self.mobile_registry.all_mobiles():
            if arg in (mob.name or "").lower():
                lines.append(f"M [{mob.vnum}] {mob.short_description}")
        for obj in self.item_registry.all_items():
            if arg in (obj.name or "").lower():
                lines.append(f"O [{obj.vnum}] {obj.short_description}")
        context.finish()
        if not lines:
            return {"to_char": "No vnum has that keyword.\r\n"}
        return {"to_char": "\r\n".join(lines[:200]) + "\r\n"}

    def do_stat(self, character: Character, context: Context, argument: str):
        kind, value = WizUtil.split_argument(argument)
        if not kind:
            context.finish()
            return {"to_char": "Stat what?\r\n"}
        if kind in ("room", "r"):
            room = self.room_registry.get_or_none(id=character.room_id)
            if room is None:
                context.finish()
                return {"to_char": "No room.\r\n"}
            context.finish()
            return {"to_char": f"Room [{room.vnum}] {room.name}\r\nFlags: {room.room_flags} Sector: {room.sector_type}\r\n"}
        if kind in ("char", "mob", "player", "m"):
            target = self._find_character_world(value or kind)
            if target is None:
                context.finish()
                return {"to_char": "No such character.\r\n"}
            context.finish()
            return {"to_char": f"{target.name} lvl {target.level} hp {target.hit}/{target.max_hit} mana {target.mana}/{target.max_mana} mv {target.movement}/{target.max_movement}\r\n"}
        if kind in ("obj", "object", "o"):
            room = self.room_registry.get_or_none(id=character.room_id)
            obj = CharacterMacros.find_item_in_room(room, value, WizUtil.name_matches)
            if obj is None:
                context.finish()
                return {"to_char": "No such object in room.\r\n"}
            context.finish()
            return {"to_char": f"Obj [{obj.vnum}] {obj.short_description}\r\nType: {obj.item_type} Flags: {obj.extra_flags} Wear: {obj.wear_flags}\r\n"}
        context.finish()
        return {"to_char": "Stat usage: stat room|char <name>|obj <name>\r\n"}

    def do_load(self, character: Character, context: Context, argument: str):
        kind, rest = WizUtil.split_argument(argument)
        if kind in ("mob", "mobile", "mload"):
            return self._do_mload(context, rest)
        if kind in ("obj", "object", "oload"):
            return self._do_oload(context, rest)
        if (kind or "").isdigit():
            return self._do_mload(context, kind)
        context.finish()
        return {"to_char": "Load syntax: load mob <vnum> | load obj <vnum>\r\n"}

    def _do_mload(self, context: Context, vnum_text: str):
        return CharacterMacros.wiz_do_mload(context, vnum_text, self.mobile_registry, self.room_registry)

    def _do_oload(self, context: Context, vnum_text: str):
        return CharacterMacros.wiz_do_oload(context, vnum_text, self.item_registry, self.room_registry)

    def do_smote(self, character: Character, context: Context, argument: str):
        text = (argument or "").strip()
        if not text:
            context.finish()
            return {"to_char": "Smote what?\r\n"}
        if (character.name or "") not in text:
            context.finish()
            return {"to_char": "You must include your name in an smote.\r\n"}
        room = self.room_registry.get_or_none(id=character.room_id)
        context.finish()
        return {
            "to_char": f"{text}\r\n",
            "room_message": f"{text}\r\n",
            "room_targets": self.player_helper.players_in_room(character, room),
        }

    def do_sockets(self, character: Character, context: Context, argument: str):
        # Networking/session introspection is handler-owned in this codebase.
        context.finish()
        return {"to_char": "Sockets output is not implemented yet.\r\n"}

    def do_immtalk(self, character: Character, context: Context, argument: str):
        text = (argument or "").strip()
        if not text:
            context.finish()
            return {"to_char": "Immtalk what?\r\n"}
        targets = [ch.id for ch in self.character_registry.all_characters() if ch.id != character.id and CharacterMacros.is_immortal(ch)]
        context.finish()
        return {"to_char": f"[immtalk] {text}\r\n", "global_message": f"[immtalk] {character.name}: {text}\r\n", "global_targets": targets}

    def do_prefix(self, character: Character, context: Context, argument: str):
        character.context["prefix"] = (argument or "").strip()
        context.finish()
        return {"to_char": "Prefix set.\r\n"}

    def do_prefi(self, character: Character, context: Context, argument: str):
        context.finish()
        return {"to_char": "You cannot abbreviate the prefix command.\r\n"}

    def _toggle_comm_on_target(self, character: Character, context: Context, argument: str, bit_name: str, label: str):
        return CharacterMacros.wiz_toggle_comm_on_target(context, argument, bit_name, label, self.CommFlagsEnum, self._find_character_world)

    def _find_character_world(self, arg: str):
        return CharacterMacros.find_character_world(arg, self.character_registry, WizUtil.name_matches, allow_self=False)
