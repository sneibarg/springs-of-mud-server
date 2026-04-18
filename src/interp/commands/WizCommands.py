from __future__ import annotations

from injector import inject

from game.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.WizUtil import WizUtil
from mobile.MobileUtil import MobileUtil
from object.ItemUtil import ItemUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from server.LoggerFactory import LoggerFactory


class WizCommands:
    @inject
    def __init__(self, registry_service: RegistryService, character_macros: CharacterMacros, player_helper: PlayerHelper):
        self.__name__ = "WizCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.area_registry = registry_service.area_registry
        self.item_registry = registry_service.item_registry
        self.mobile_registry = registry_service.mobile_registry
        self.interp_registry = registry_service.interp_registry
        self.character_macros = character_macros
        self.player_helper = player_helper
        self.player_act_bits = character_macros.enums.get("playerActBits")
        self.comm_flags = character_macros.enums.get("commFlags")
        self.wiznet_flags = character_macros.enums.get("wiznetFlags")

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
        flags = GenericUtil.to_int((character.context or {}).get("wiznet_flags", 0), 0)
        on_bit = self._wiznet_flag("WIZ_ON")
        arg = (argument or "").strip().lower()

        if arg in ("", "on"):
            if on_bit:
                flags |= on_bit
            character.context["wiznet_flags"] = flags
            context.finish()
            return {"to_char": "Welcome to Wiznet!\r\n"}
        if arg == "off":
            if on_bit:
                flags &= ~on_bit
            character.context["wiznet_flags"] = flags
            context.finish()
            return {"to_char": "Signing off of Wiznet.\r\n"}
        if arg == "status":
            names = []
            for bit_name in self._wiznet_names():
                bit = self._wiznet_flag(bit_name)
                if bit and (flags & bit):
                    names.append(bit_name.replace("WIZ_", "").lower())
            off = "off " if on_bit and (flags & on_bit) == 0 else ""
            context.finish()
            return {"to_char": f"Wiznet status:\r\n{off}{' '.join(names)}\r\n"}
        if arg == "show":
            names = [name.replace("WIZ_", "").lower() for name in self._wiznet_names()]
            context.finish()
            return {"to_char": "Wiznet options available to you are:\r\n" + " ".join(names) + "\r\n"}

        bit_name = f"WIZ_{arg.upper()}"
        bit = self._wiznet_flag(bit_name)
        if bit == 0:
            context.finish()
            return {"to_char": "No such option.\r\n"}
        if (flags & bit) != 0:
            flags &= ~bit
            character.context["wiznet_flags"] = flags
            context.finish()
            return {"to_char": f"You will no longer see {arg} on wiznet.\r\n"}
        flags |= bit
        character.context["wiznet_flags"] = flags
        context.finish()
        return {"to_char": f"You will now see {arg} on wiznet.\r\n"}

    def do_holylight(self, character: Character, context: Context, argument: str):
        bit = self._player_act_bit("PLR_HOLYLIGHT")
        if bit == 0:
            context.finish()
            return {"to_char": "This feature is unavailable.\r\n"}
        act = GenericUtil.to_int(self.character_macros.convert_flags(getattr(character.character_flags, "act", "") or "0"), 0)
        if self.character_macros.is_set(act, bit):
            act = self.character_macros.unset_bit(act, bit)
            character.character_flags.act = GenericUtil.flags_to_letters(act)
            context.finish()
            return {"to_char": "Holy light mode off.\r\n"}
        act = self.character_macros.set_bit(act, bit)
        character.character_flags.act = GenericUtil.flags_to_letters(act)
        context.finish()
        return {"to_char": "Holy light mode on.\r\n"}

    def do_invis(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip()
        level = GenericUtil.to_int(arg, -1) if arg else -1
        if level < 0:
            level = 0 if GenericUtil.to_int(getattr(character, "invis_level", 0), 0) > 0 else int(getattr(character, "level", 0))
        character.invis_level = level
        context.finish()
        if level > 0:
            return {"to_char": f"You vanish into thin air (level {level}).\r\n"}
        return {"to_char": "You are now fully visible.\r\n"}

    def do_incognito(self, character: Character, context: Context, argument: str):
        arg = (argument or "").strip()
        level = GenericUtil.to_int(arg, -1) if arg else -1
        if level < 0:
            level = 0 if GenericUtil.to_int(getattr(character, "incog_level", 0), 0) > 0 else int(getattr(character, "level", 0))
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
        room = self._find_location(character, arg)
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

        room = self.room_registry.get_or_none(id=character.room_id) if not destination else self._find_location(character, destination)
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
                self._restore_character(victim)
            context.finish()
            return {"to_char": "All active players restored.\r\n"}

        victim = self._find_character_world(arg)
        if victim is None:
            context.finish()
            return {"to_char": "Restore whom?\r\n"}
        self._restore_character(victim)
        context.finish()
        return {"to_char": "Ok.\r\n", "victim": victim, "to_victim": "You have been restored.\r\n"}

    def do_purge(self, character: Character, context: Context, argument: str):
        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        arg = (argument or "").strip()
        if arg:
            victim = self._find_character_in_room(room, arg)
            if victim is not None and victim.id != character.id:
                room.remove_player_from_room(victim)
                victim.room_id = ""
                context.finish()
                return {"to_char": "Ok.\r\n", "victim": victim, "to_victim": "You are purged!\r\n"}
            item = self._find_item_in_room(room, arg)
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
            if attrs is not None and self.character_macros.PositionsEnum is not None and hasattr(self.character_macros.PositionsEnum, "POS_STANDING"):
                attrs.position = int(self.character_macros.PositionsEnum.POS_STANDING.value)
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
            obj = self._find_item_in_room(room, value)
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
        vnum = (vnum_text or "").strip()
        proto = self.mobile_registry.get_or_none(vnum=vnum)
        if proto is None:
            context.finish()
            return {"to_char": "No mobile has that vnum.\r\n"}
        mob = MobileUtil.create_mobile(proto, self.character_macros.enums, self.character_macros)
        room = self.room_registry.get_or_none(id=context.character.room_id)
        if room is not None:
            room.add_mobile_to_room(mob)
        context.finish()
        return {"to_char": "Mobile loaded.\r\n"}

    def _do_oload(self, context: Context, vnum_text: str):
        vnum = (vnum_text or "").strip()
        proto = self.item_registry.get_or_none(vnum=vnum)
        if proto is None:
            context.finish()
            return {"to_char": "No object has that vnum.\r\n"}
        obj = ItemUtil.create_object(proto)
        room = self.room_registry.get_or_none(id=context.character.room_id)
        if room is not None:
            room.add_item_to_room(obj)
        context.finish()
        return {"to_char": "Object loaded.\r\n"}

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
        targets = [ch.id for ch in self.character_registry.all_characters() if ch.id != character.id and self.character_macros.is_immortal(ch)]
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
        victim = self._find_character_world((argument or "").strip())
        if victim is None:
            context.finish()
            return {"to_char": f"{label.lower()} whom?\r\n"}
        bit = self._comm_flag(bit_name)
        if bit == 0:
            context.finish()
            return {"to_char": "This feature is unavailable.\r\n"}
        raw = GenericUtil.to_int(self.character_macros.convert_flags(getattr(victim.character_flags, "comm", "") or "0"), 0)
        if self.character_macros.is_set(raw, bit):
            raw = self.character_macros.unset_bit(raw, bit)
            victim.character_flags.comm = GenericUtil.flags_to_letters(raw)
            context.finish()
            return {"to_char": f"{label} removed.\r\n", "victim": victim, "to_victim": "The gods have restored your privileges.\r\n"}
        raw = self.character_macros.set_bit(raw, bit)
        victim.character_flags.comm = GenericUtil.flags_to_letters(raw)
        context.finish()
        return {"to_char": f"{label} set.\r\n", "victim": victim, "to_victim": "The gods have revoked your privileges.\r\n"}

    @staticmethod
    def _restore_character(victim: Character):
        victim.hit = int(getattr(victim, "max_hit", 0))
        victim.mana = int(getattr(victim, "max_mana", 0))
        victim.movement = int(getattr(victim, "max_movement", 0))

    def _find_character_world(self, arg: str):
        q = (arg or "").strip().lower()
        if not q:
            return None
        if q == "self":
            return None
        for ch in self.character_registry.all_characters():
            if WizUtil.name_matches(q, getattr(ch, "name", "")):
                return ch
        return None

    @staticmethod
    def _find_character_in_room(room, arg: str):
        if room is None:
            return None
        q = (arg or "").strip().lower()
        for ch in room.characters.values():
            if WizUtil.name_matches(q, getattr(ch, "name", "")):
                return ch
        return None

    @staticmethod
    def _find_item_in_room(room, arg: str):
        if room is None:
            return None
        q = (arg or "").strip().lower()
        for item in room.contents.values():
            if WizUtil.name_matches(q, getattr(item, "name", "")):
                return item
        return None

    def _find_location(self, character: Character, arg: str):
        value = (arg or "").strip()
        if value.isdigit():
            room = self.room_registry.get_or_none(vnum=value)
            if room is not None:
                return room
        victim = self._find_character_world(value)
        if victim is not None:
            return self.room_registry.get_or_none(id=victim.room_id)

        # Support goto by mobile name (e.g., goto hassan).
        q = value.lower()
        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for mob in room.mobiles.values():
                mob_name = f"{getattr(mob, 'name', '')} {getattr(mob, 'short_description', '')}".strip()
                if WizUtil.name_matches(q, mob_name):
                    return room

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            if WizUtil.name_matches(value, getattr(room, "name", "")):
                return room
        return None

    def _player_act_bit(self, name: str) -> int:
        if self.player_act_bits is None or not hasattr(self.player_act_bits, name):
            return 0
        return int(getattr(self.player_act_bits, name).value)

    def _comm_flag(self, name: str) -> int:
        if self.comm_flags is None or not hasattr(self.comm_flags, name):
            return 0
        return int(getattr(self.comm_flags, name).value)

    def _wiznet_flag(self, name: str) -> int:
        if self.wiznet_flags is None or not hasattr(self.wiznet_flags, name):
            return 0
        return int(getattr(self.wiznet_flags, name).value)

    def _wiznet_names(self) -> list[str]:
        if self.wiznet_flags is None:
            return []
        names = []
        for field in dir(self.wiznet_flags):
            if field.startswith("WIZ_"):
                names.append(field)
        return sorted(names)
