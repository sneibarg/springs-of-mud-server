from __future__ import annotations

from injector import inject

from api.CharacterApi import CharacterApi
from api.InterpApi import InterpApi
from api.ItemApi import ItemApi
from api.WizSetApi import WizSetApi
from area.Room import Room
from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from game.WizHandler import WizHandler
from interp.Context import Context
from item.ExtraDescriptionData import ExtraDescriptionData
from mobile.Mobile import Mobile
from player.Character import Character
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil
from util.ItemUtil import ItemUtil
from util.MobileUtil import MobileUtil
from util.WizUtil import WizUtil


class Wiz:
    @inject
    def __init__(self,
                 registry_service: RegistryService,
                 wiz_handler: WizHandler,
                 interp_api: InterpApi,
                 wiz_set_api: WizSetApi,
                 enum_provider: EnumProvider):
        self.__name__ = "Wiz"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.wiz_handler = wiz_handler
        self.interp_api = interp_api
        self.wiz_set_api = wiz_set_api
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.area_registry = registry_service.area_registry
        self.item_registry = registry_service.item_registry
        self.mobile_registry = registry_service.mobile_registry
        self.interp_registry = registry_service.interp_registry
        self.special_registry = registry_service.special_registry
        self.PlayerActBitsEnum = enum_provider.get("playerActBits")
        self.CommFlagsEnum = enum_provider.get("commFlags")
        self.WiznetFlagsEnum = enum_provider.get("wiznetFlags")
        self.PositionsEnum = enum_provider.get("positions")
        self.ActBitsEnum = enum_provider.get("actBits")
        self.ItemFlagsEnum = enum_provider.get("itemFlags")
        self.GameParameters = enum_provider.get("gameParameters")

    def execute(self, character: Character, context: Context):
        command_name = (getattr(context.command, "name", "") or "").strip().lower()
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
            "log": self.do_log,
            "memory": self.do_memory,
            "set": self.do_set,
            "snoop": self.do_snoop,
            "string": self.do_string,
            "switch": self.do_switch,
            "clone": self.do_clone,
        }
        handler = handlers.get(command_name)
        if handler is None:
            context.finish()
            return {"to_char": f"{command_name} is not implemented yet.\r\n"}
        return handler(character, context)

    def do_wizhelp(self, _character: Character, context: Context):
        names = []
        for cmd in self.interp_registry.all_commands():
            if (getattr(cmd, "role", "") or "").strip().lower() == "immortal":
                names.append(str(getattr(cmd, "name", "") or ""))
        context.finish()
        return {"to_char": "Wizard commands:\r\n" + " ".join(sorted(name for name in names if name)) + "\r\n"}

    def do_wiznet(self, character: Character, context: Context):
        flags = GenericUtil.to_int((character.context or {}).get("WiznetFlagsEnum", 0), 0)
        on_bit = CharacterApi.enum_bit(self.WiznetFlagsEnum, "WIZ_ON")
        arg = WizUtil.argument_text(context.result, context.parameters).strip().lower()

        if arg == "":
            enabled = (flags & on_bit) == 0
            character.context["WiznetFlagsEnum"] = flags | on_bit if enabled else flags & ~on_bit
            context.finish()
            return self._command_payload("enable" if enabled else "disable")
        if arg == "on":
            character.context["WiznetFlagsEnum"] = flags | on_bit
            context.finish()
            return self._command_payload("enable")
        if arg == "off":
            character.context["WiznetFlagsEnum"] = flags & ~on_bit
            context.finish()
            return self._command_payload("disable")
        if arg == "status":
            names = [
                name.replace("WIZ_", "").lower()
                for name in CharacterApi.enum_names(self.WiznetFlagsEnum, "WIZ_")
                if CharacterApi.enum_bit(self.WiznetFlagsEnum, name)
                and (flags & CharacterApi.enum_bit(self.WiznetFlagsEnum, name)) != 0
            ]
            off = "off " if on_bit and (flags & on_bit) == 0 else ""
            context.finish()
            return {"to_char": f"Wiznet status:\r\n{off}{' '.join(names)}\r\n"}
        if arg == "show":
            context.finish()
            return {"to_char": "Wiznet options available to you are:\r\n" + " ".join(self.wiz_handler.wiznet_option_names(character)) + "\r\n"}

        bit_name = f"WIZ_{arg.upper()}"
        bit = CharacterApi.enum_bit(self.WiznetFlagsEnum, bit_name)
        if bit == 0 or self.wiz_handler.wiznet_option_level(bit_name) > CharacterApi.get_trust(character):
            context.finish()
            return self._command_payload("no_such_option")
        if (flags & bit) != 0:
            character.context["WiznetFlagsEnum"] = flags & ~bit
            context.finish()
            return self._command_payload("enable_option", tokens={"s": arg})
        character.context["WiznetFlagsEnum"] = flags | bit
        context.finish()
        return self._command_payload("disable_option", tokens={"s": arg})

    def do_holylight(self, character: Character, context: Context):
        enabled = not CharacterApi.is_set(character.status_flags.act, CharacterApi.enum_bit(self.PlayerActBitsEnum, "PLR_HOLYLIGHT"))
        if enabled:
            CharacterApi.set_act_flags(character, self.PlayerActBitsEnum.PLR_HOLYLIGHT.value)
        else:
            CharacterApi.unset_act_flags(character, self.PlayerActBitsEnum.PLR_HOLYLIGHT.value)
        context.finish()
        return self._command_payload("enable" if enabled else "disable")

    def do_invis(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        arg = WizUtil.argument_text(context.result, context.parameters).strip()
        current = GenericUtil.to_int(getattr(character.status_flags, "invis_level", 0), 0)
        if not arg:
            character.status_flags.invis_level = 0 if current > 0 else CharacterApi.get_trust(character)
        else:
            character.status_flags.invis_level = GenericUtil.to_int(arg, 0)
        room = self.room_registry.get_or_none(id=character.room_id)
        context.finish()
        return self._command_payload(
            "enable" if GenericUtil.to_int(getattr(character.status_flags, "invis_level", 0), 0) > 0 else "disable",
            targets=[] if room is None else room.player_targets(character),
        )

    def do_incognito(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        arg = WizUtil.argument_text(context.result, context.parameters).strip()
        current = GenericUtil.to_int(getattr(character.status_flags, "incog_level", 0), 0)
        if not arg:
            character.status_flags.incog_level = 0 if current > 0 else CharacterApi.get_trust(character)
        else:
            character.status_flags.incog_level = GenericUtil.to_int(arg, 0)
        room = self.room_registry.get_or_none(id=character.room_id)
        context.finish()
        return self._command_payload(
            "enable" if GenericUtil.to_int(getattr(character.status_flags, "incog_level", 0), 0) > 0 else "disable",
            targets=[] if room is None else room.player_targets(character),
        )

    def do_bamfin(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        text = WizUtil.argument_text(context.result, context.parameters).strip()
        if not text:
            context.finish()
            return self._command_payload("default", tokens={"s": (character.context or {}).get("poofin", "")})
        character.context["poofin"] = text
        context.finish()
        return self._command_payload("set", tokens={"s": text})

    def do_bamfout(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        text = WizUtil.argument_text(context.result, context.parameters).strip()
        if not text:
            context.finish()
            return self._command_payload("default", tokens={"s": (character.context or {}).get("poofout", "")})
        character.context["poofout"] = text
        context.finish()
        return self._command_payload("set", tokens={"s": text})

    def do_echo(self, character: Character, context: Context):
        argument = WizUtil.argument_text(context.result, context.parameters)
        if not argument:
            context.finish()
            return self._command_payload("local_echo_what")
        room = self.room_registry.get_or_none(id=character.room_id)
        context.finish()
        return {"to_char": f"{argument}\r\n", "room_message": f"{argument}\r\n", "room_targets": [] if room is None else room.player_targets(character)}

    def do_gecho(self, character: Character, context: Context):
        argument = WizUtil.argument_text(context.result, context.parameters)
        if not argument:
            context.finish()
            return self._command_payload("no_argument")
        context.finish()
        return {"to_char": f"{argument}\r\n", "broadcast_message": f"{argument}\r\n", "exclude_character_ids": [character.id]}

    def do_zecho(self, character: Character, context: Context):
        argument = WizUtil.argument_text(context.result, context.parameters)
        if not argument:
            context.finish()
            return self._command_payload("no_argument")
        targets = [ch for ch in self.character_registry.all_characters() if str(getattr(ch, "area_id", "")) == str(character.area_id) and ch.id != character.id]
        context.finish()
        return {"to_char": f"{argument}\r\n", "global_message": f"{argument}\r\n", "global_targets": targets}

    def do_pecho(self, _character: Character, context: Context):
        target_name, message = WizUtil.split_argument(WizUtil.argument_text(context.result, context.parameters))
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, target_name, include_mobiles=False)
        if not target_name or not message:
            context.finish()
            return self._command_payload("no_argument")
        if victim is None:
            context.finish()
            return self._command_payload("target_not_found")
        context.finish()
        return self._command_payload("default", victim=victim, tokens={"s": message})

    def do_goto(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        room = CharacterApi.find_location(WizUtil.argument_text(context.result, context.parameters), self.room_registry, self.character_registry, WizUtil.name_matches)
        from_room = WizUtil.move_entity(self.room_registry, character, room)
        if from_room is None or room is None:
            context.finish()
            return {"to_char": "No such location.\r\n"}
        context.finish()
        return {
            "from_room_targets": self._visible_room_targets(from_room, character),
            "from_room_message": f"{self._poof_text(character, 'poofout', f'{character.name} leaves in a swirling mist.')}\r\n",
            "to_room_targets": self._visible_room_targets(room, character),
            "to_room_message": f"{self._poof_text(character, 'poofin', f'{character.name} appears in a swirling mist.')}\r\n",
            "to_room_obj": room,
            "view_character": character,
        }

    def do_transfer(self, character: Character, context: Context):
        argument = WizUtil.argument_text(context.result, context.parameters)
        target_name, destination = WizUtil.split_argument(argument)
        if not target_name:
            context.finish()
            return {"to_char": "Transfer whom (and where)?\r\n"}
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, target_name)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        room = self.room_registry.get_or_none(id=character.room_id) if not destination else CharacterApi.find_location(destination, self.room_registry, self.character_registry, WizUtil.name_matches)
        if room is None:
            context.finish()
            return {"to_char": "No such location.\r\n"}
        if self.wiz_handler.room_is_private_for_actor(character, room):
            context.finish()
            return {"to_char": "That room is private right now.\r\n"}
        from_room = WizUtil.move_entity(self.room_registry, victim, room)
        context.finish()
        return {
            "to_char": "Ok.\r\n",
            "victim": victim if not CharacterApi.is_npc(victim) else None,
            "to_victim": "" if CharacterApi.is_npc(victim) else f"{character.name} has transferred you.\r\n",
            "from_room_targets": [] if from_room is None else from_room.player_targets(victim) if not CharacterApi.is_npc(victim) else from_room.players_in_room(),
            "from_room_message": f"{WizUtil.display_name(victim)} disappears in a mushroom cloud.\r\n",
            "to_room_targets": room.player_targets(victim) if not CharacterApi.is_npc(victim) else room.players_in_room(),
            "to_room_message": f"{WizUtil.display_name(victim)} arrives from a puff of smoke.\r\n",
            "to_room_obj": room,
            "view_character": victim,
        }

    def do_return(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        original, body = self.wiz_handler.return_character(character)
        if original is None:
            context.finish()
            return self._command_payload("switch_inactive")
        context.character = original
        context.finish()
        return self._command_payload(
            "default",
            view_character=original,
            wiznet_actor=original,
            wiznet_flag="WIZ_SWITCHES",
            wiznet_skip_flag="WIZ_SECURE",
            wiznet_min_level=CharacterApi.get_trust(character),
            tokens={"c": getattr(original, "name", ""), "t": WizUtil.display_name(body)},
        )

    def do_nochannels(self, character: Character, context: Context):
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, WizUtil.argument_text(context.result, context.parameters))
        bit = CharacterApi.enum_bit(self.CommFlagsEnum, "COMM_NOCHANNELS")
        enabled = CharacterApi.is_set(victim.status_flags.comm, bit)
        if enabled:
            CharacterApi.unset_comm_flags(victim, bit)
        else:
            CharacterApi.set_comm_flags(victim, bit)
        context.finish()
        return self._command_payload("removed" if enabled else "set", victim=victim, wiznet_flag="WIZ_PENALTIES", wiznet_skip_flag="WIZ_SECURE")

    def do_noemote(self, character: Character, context: Context):
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, WizUtil.argument_text(context.result, context.parameters))
        bit = CharacterApi.enum_bit(self.CommFlagsEnum, "COMM_NOEMOTE")
        enabled = CharacterApi.is_set(victim.status_flags.comm, bit)
        if enabled:
            CharacterApi.unset_comm_flags(victim, bit)
        else:
            CharacterApi.set_comm_flags(victim, bit)
        context.finish()
        return self._command_payload("removed" if enabled else "set", victim=victim, wiznet_flag="WIZ_PENALTIES", wiznet_skip_flag="WIZ_SECURE")

    def do_noshout(self, character: Character, context: Context):
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, WizUtil.argument_text(context.result, context.parameters))
        bit = CharacterApi.enum_bit(self.CommFlagsEnum, "COMM_NOSHOUT")
        enabled = CharacterApi.is_set(victim.status_flags.comm, bit)
        if enabled:
            CharacterApi.unset_comm_flags(victim, bit)
        else:
            CharacterApi.set_comm_flags(victim, bit)
        context.finish()
        return self._command_payload("removed" if enabled else "set", victim=victim, wiznet_flag="WIZ_PENALTIES", wiznet_skip_flag="WIZ_SECURE")

    def do_notell(self, character: Character, context: Context):
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, WizUtil.argument_text(context.result, context.parameters))
        bit = CharacterApi.enum_bit(self.CommFlagsEnum, "COMM_NOTELL")
        enabled = CharacterApi.is_set(victim.status_flags.comm, bit)
        if enabled:
            CharacterApi.unset_comm_flags(victim, bit)
        else:
            CharacterApi.set_comm_flags(victim, bit)
        context.finish()
        return self._command_payload("removed" if enabled else "set", victim=victim, wiznet_flag="WIZ_PENALTIES", wiznet_skip_flag="WIZ_SECURE")

    def do_freeze(self, character: Character, context: Context):
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, WizUtil.argument_text(context.result, context.parameters))
        bit = CharacterApi.enum_bit(self.PlayerActBitsEnum, "PLR_FREEZE")
        enabled = CharacterApi.is_set(victim.status_flags.act, bit)
        if enabled:
            CharacterApi.unset_act_flags(victim, bit)
        else:
            CharacterApi.set_act_flags(victim, bit)
        context.finish()
        return self._command_payload("removed" if enabled else "set", victim=victim, wiznet_flag="WIZ_PENALTIES", wiznet_skip_flag="WIZ_SECURE")

    def do_restore(self, character: Character, context: Context):
        arg = WizUtil.argument_text(context.result, context.parameters).strip().lower()
        room = self.room_registry.get_or_none(id=character.room_id)
        if arg in ("", "room"):
            for target in ([] if room is None else list(room.characters.values()) + list(room.mobiles.values())):
                CharacterApi.restore_character(target)
            context.finish()
            return {
                "to_char": "Room restored.\r\n",
                "to_wiznet": f"{character.name} restored room {getattr(room, 'vnum', '')}.\r\n",
                "wiznet_flag": "WIZ_RESTORE",
                "wiznet_skip_flag": "WIZ_SECURE",
                "wiznet_min_level": CharacterApi.get_trust(character),
            }
        if arg == "all" and CharacterApi.get_trust(character) >= self.GameParameters.MAX_LEVEL.value - 1:
            for session in self.wiz_handler.session_handler.get_playing_sessions():
                victim = session.character
                if victim is not None and not CharacterApi.is_npc(victim):
                    CharacterApi.restore_character(victim)
            context.finish()
            return self._command_payload("active_players")
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, arg)
        if victim is None:
            context.finish()
            return self._command_payload("target_missing")
        CharacterApi.restore_character(victim)
        context.finish()
        return self._command_payload("default", victim=victim, wiznet_flag="WIZ_RESTORE", wiznet_skip_flag="WIZ_SECURE", wiznet_min_level=CharacterApi.get_trust(character))

    def do_purge(self, character: Character, context: Context):
        argument = WizUtil.argument_text(context.result, context.parameters).strip()
        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        if not argument:
            nopurge_act = CharacterApi.enum_bit(self.ActBitsEnum, "ACT_NOPURGE")
            nopurge_item = CharacterApi.enum_bit(self.ItemFlagsEnum, "ITEM_NOPURGE")
            for victim in list(room.mobiles.values()):
                if victim == character:
                    continue
                if nopurge_act and CharacterApi.is_set(getattr(victim.status_flags, "act", 0), nopurge_act):
                    continue
                room.remove_mobile_from_room(victim)
            for obj in list(room.contents.values()):
                if nopurge_item and GameApi.is_set(getattr(obj, "extra_flags", 0), nopurge_item):
                    continue
                room.remove_item_from_room(obj)
            context.finish()
            return {"to_char": "Ok.\r\n", "room_message": f"{character.name} purges the room!\r\n", "room_targets": room.player_targets(character)}

        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, argument)
        if victim is None:
            context.finish()
            return self._command_payload("target_missing")
        if not CharacterApi.is_npc(victim):
            if victim == character:
                context.finish()
                return self._command_payload("target_self")
            if CharacterApi.get_trust(character) <= CharacterApi.get_trust(victim):
                context.finish()
                return self._command_payload("insufficient_level", victim=victim, tokens={"c": character.name})
            victim_room = WizUtil.room_of_entity(self.room_registry, victim)
            if victim_room is not None:
                victim_room.remove_player_from_room(victim)
            victim.room_id = ""
            context.finish()
            return {
                "room_message": f"{character.name} disintegrates {victim.name}.\r\n",
                "room_targets": [] if victim_room is None else victim_room.player_targets(victim),
                "disconnect_character": victim,
            }
        victim_room = WizUtil.room_of_entity(self.room_registry, victim)
        if victim_room is not None:
            victim_room.remove_mobile_from_room(victim)
        context.finish()
        return {"room_message": f"{character.name} purges {WizUtil.display_name(victim)}.\r\n", "room_targets": [] if victim_room is None else victim_room.players_in_room()}

    def do_peace(self, _character: Character, context: Context):
        room = self.room_registry.get_or_none(id=context.character.room_id)
        if room is None:
            context.finish()
            return {"to_char": "You are nowhere.\r\n"}
        aggressive = CharacterApi.enum_bit(self.ActBitsEnum, "ACT_AGGRESSIVE")
        for target in list(room.characters.values()) + list(room.mobiles.values()):
            target.fighting = None
            if hasattr(target, "character_attributes") and getattr(target, "character_attributes", None) is not None:
                CharacterApi.set_position(target, "POS_STANDING")
            if CharacterApi.is_npc(target) and aggressive:
                target.status_flags.act = CharacterApi.unset_bit(getattr(target.status_flags, "act", 0), aggressive)
        context.finish()
        return {"to_char": "Ok.\r\n"}

    def do_mwhere(self, _character: Character, context: Context):
        arg = WizUtil.argument_text(context.result, context.parameters).strip().lower()
        lines = []
        for room in self.room_registry.all_rooms():
            for mob in room.mobiles.values():
                name = f"{mob.name or ''} {mob.short_description or ''}".strip().lower()
                if not arg or arg in name:
                    lines.append(f"[{mob.vnum}] {mob.short_description} - [{room.vnum}] {room.name}")
        context.finish()
        return {"to_char": "Nothing like that in heaven or earth.\r\n" if not lines else "\r\n".join(lines) + "\r\n"}

    def do_owhere(self, _character: Character, context: Context):
        arg = WizUtil.argument_text(context.result, context.parameters).strip().lower()
        if not arg:
            context.finish()
            return {"to_char": "Owhere what?\r\n"}
        lines = []
        for room in self.room_registry.all_rooms():
            for obj in room.contents.values():
                if arg in str(getattr(obj, "name", "") or "").lower():
                    lines.append(f"[{obj.vnum}] {obj.short_description} - [{room.vnum}] {room.name}")
        context.finish()
        return {"to_char": "Nothing like that in heaven or earth.\r\n" if not lines else "\r\n".join(lines) + "\r\n"}

    def do_vnum(self, _character: Character, context: Context):
        arg = WizUtil.argument_text(context.result, context.parameters).strip().lower()
        if not arg:
            context.finish()
            return self._command_payload("syntax")
        lines = []
        for mob in self.mobile_registry.all_mobiles():
            if arg in str(getattr(mob, "name", "") or "").lower():
                lines.append(f"M [{mob.vnum}] {mob.short_description}")
        for obj in self.item_registry.all_items():
            if arg in str(getattr(obj, "name", "") or "").lower():
                lines.append(f"O [{obj.vnum}] {obj.short_description}")
        context.finish()
        return {"to_char": "No vnum has that keyword.\r\n" if not lines else "\r\n".join(lines[:200]) + "\r\n"}

    def do_stat(self, character: Character, context: Context):
        kind, value = WizUtil.split_argument(WizUtil.argument_text(context.result, context.parameters))
        if not kind:
            context.finish()
            return self._command_payload("syntax")
        if kind in ("room", "r"):
            room = self.room_registry.get_or_none(id=character.room_id)
            context.finish()
            if room is None:
                return self._command_payload("room_missing")
            return {"to_char": f"Room [{room.vnum}] {room.name}\r\nFlags: {room.room_flags} Sector: {room.sector_type}\r\n"}
        if kind in ("char", "mob", "player", "m"):
            target = WizUtil.find_world_entity(self.character_registry, self.room_registry, value or kind)
            context.finish()
            return {"to_char": self._stat_character_text(target)} if target is not None else self._command_payload("no_such_target")
        if kind in ("obj", "item", "o"):
            target = WizUtil.find_world_item(self.character_registry, self.room_registry, value)
            context.finish()
            return {"to_char": self._stat_object_text(target)} if target is not None else self._command_payload("no_such_target")
        target = WizUtil.find_world_entity(self.character_registry, self.room_registry, kind)
        if target is not None:
            context.finish()
            return {"to_char": self._stat_character_text(target)}
        obj = WizUtil.find_world_item(self.character_registry, self.room_registry, kind)
        context.finish()
        return {"to_char": self._stat_object_text(obj)} if obj is not None else self._command_payload("no_such_target")

    def do_load(self, character: Character, context: Context):
        raw = WizUtil.argument_text(context.result, context.parameters)
        kind, rest = WizUtil.split_argument(raw)
        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return self._command_payload("room_missing")

        if kind in ("mob", "mobile", "mload") or (kind or "").isdigit():
            vnum = kind if (kind or "").isdigit() else rest
            if not str(vnum or "").strip().isdigit():
                context.finish()
                return self._command_payload("mobile_syntax")
            proto = self.mobile_registry.get_or_none(vnum=str(vnum).strip())
            if proto is None:
                context.finish()
                return self._command_payload("no_such_mobile")
            mob = MobileUtil.create_mobile(proto, CharacterApi.enums())
            room.add_mobile_to_room(mob)
            context.finish()
            return {
                **self._command_payload("default", tokens={"t": mob.short_description}),
                "room_message": self._command_text(context, "created", channel="to_room", c=character.name, t=mob.short_description),
                "room_targets": room.player_targets(character),
                "to_wiznet": self._command_text(context, "loads", channel="to_wiznet", c=character.name, t=mob.short_description),
                "wiznet_flag": "WIZ_LOAD",
                "wiznet_skip_flag": "WIZ_SECURE",
                "wiznet_min_level": CharacterApi.get_trust(character),
            }
        if kind in ("obj", "item", "oload"):
            vnum_text, level_text = WizUtil.split_argument(rest)
            if not str(vnum_text or "").strip().isdigit():
                context.finish()
                return self._command_payload("object_syntax")
            level = CharacterApi.get_trust(character)
            if level_text:
                if not level_text.isdigit():
                    context.finish()
                    return self._command_payload("oload_syntax")
                level = GenericUtil.to_int(level_text, -1)
                if level < 0 or level > CharacterApi.get_trust(character):
                    context.finish()
                    return self._command_payload("invalid_object_level")
            proto = self.item_registry.get_or_none(vnum=str(vnum_text).strip())
            if proto is None:
                context.finish()
                return self._command_payload("no_such_object")
            obj = ItemUtil.create_object(proto)
            obj.level = level
            if ItemUtil.item_takeable(obj) and not CharacterApi.is_npc(character):
                character.add_item(obj)
            elif ItemUtil.item_takeable(obj) and CharacterApi.is_npc(character):
                MobileUtil.add_inventory_item(character, obj)
            else:
                room.add_item_to_room(obj)
            context.finish()
            return {
                **self._command_payload("default", tokens={"t": obj.short_description}),
                "room_message": self._command_text(context, "created", channel="to_room", c=character.name, t=obj.short_description),
                "room_targets": room.player_targets(character),
                "to_wiznet": self._command_text(context, "loads", channel="to_wiznet", c=character.name, t=obj.short_description),
                "wiznet_flag": "WIZ_LOAD",
                "wiznet_skip_flag": "WIZ_SECURE",
                "wiznet_min_level": CharacterApi.get_trust(character),
            }
        context.finish()
        return self._command_payload("syntax")

    def do_smote(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        text = WizUtil.argument_text(context.result, context.parameters)
        room = self.room_registry.get_or_none(id=character.room_id)
        target_messages = []
        if room is not None:
            for viewer in room.player_targets(character):
                target_messages.append({"id": viewer.id, "text": WizUtil.personalize_smote(text, getattr(viewer, "name", "")) + "\r\n"})
        context.finish()
        return {"to_char": f"{text}\r\n", "target_messages": target_messages}

    def do_sockets(self, character: Character, context: Context):
        context.finish()
        return {"to_char": self.wiz_handler.render_sockets(character, WizUtil.argument_text(context.result, context.parameters))}

    def do_immtalk(self, character: Character, context: Context):
        text = WizUtil.argument_text(context.result, context.parameters)
        nowiz_bit = CharacterApi.enum_bit(self.CommFlagsEnum, "COMM_NOWIZ")
        if not text:
            enabled = CharacterApi.is_set(character.status_flags.comm, nowiz_bit)
            if enabled:
                CharacterApi.unset_comm_flags(character, nowiz_bit)
            else:
                CharacterApi.set_comm_flags(character, nowiz_bit)
            context.finish()
            return self._command_payload("immortal_channel_now" if enabled else "immortal_channel_now_off")

        CharacterApi.unset_comm_flags(character, nowiz_bit)
        targets = []
        for session in self.wiz_handler.session_handler.get_playing_sessions():
            victim = session.character
            if victim is None or victim.id == character.id or not CharacterApi.is_immortal(victim):
                continue
            if CharacterApi.is_set(getattr(victim.status_flags, "comm", 0), nowiz_bit):
                continue
            targets.append({"id": victim.id, "text": f"{character.name}: {text}\r\n"})
        context.finish()
        return {"to_char": f"{character.name}: {text}\r\n", "target_messages": targets}

    def do_prefix(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        argument = WizUtil.argument_text(context.result, context.parameters).strip()
        current = str((character.context or {}).get("prefix", "") or "")
        if not argument:
            character.context["prefix"] = ""
            context.finish()
            return self._command_payload("removed")
        character.context["prefix"] = argument
        context.finish()
        return self._command_payload("changed" if current else "set", tokens={"s": argument})

    def do_prefi(self, _character: Character, context: Context):
        context.finish()
        return {"to_char": "You cannot abbreviate the prefix command.\r\n"}

    def do_log(self, character: Character, context: Context):
        argument = WizUtil.argument_text(context.result, context.parameters).strip().lower()
        if argument == "all":
            enabled = self.wiz_handler.toggle_log_all()
            context.finish()
            return self._command_payload("enable_log_all" if enabled else "disable_log_all")
        victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, argument)
        bit = CharacterApi.enum_bit(self.PlayerActBitsEnum, "PLR_LOG")
        enabled = CharacterApi.is_set(victim.status_flags.act, bit)
        if enabled:
            CharacterApi.unset_act_flags(victim, bit)
        else:
            CharacterApi.set_act_flags(victim, bit)
        context.finish()
        return self._command_payload("remove" if enabled else "set")

    def do_memory(self, _character: Character, context: Context):
        context.finish()
        return {"to_char": self.wiz_handler.memory_report()}

    def do_set(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        return self.wiz_set_api.dispatch(character, context)

    def do_snoop(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        target = WizUtil.find_world_entity(self.character_registry, self.room_registry, WizUtil.argument_text(context.result, context.parameters))
        if target == character:
            self.wiz_handler.cancel_snoops(character)
            context.finish()
            return self._command_payload("cancel_all", wiznet_flag="WIZ_SNOOPS", wiznet_skip_flag="WIZ_SECURE", wiznet_min_level=CharacterApi.get_trust(character))
        self.wiz_handler.start_snoop(character, target)
        context.finish()
        return self._command_payload("default", tokens={"t": WizUtil.display_name(target)}, wiznet_flag="WIZ_SNOOPS", wiznet_skip_flag="WIZ_SECURE", wiznet_min_level=CharacterApi.get_trust(character))

    def do_string(self, _character: Character, context: Context):
        raw = WizUtil.argument_text(context.result, context.parameters)
        parts = raw.split(maxsplit=3)
        if len(parts) < 4:
            context.finish()
            return self._command_payload("syntax")
        target_type, target_name, field_name, rest = parts
        target_type = target_type.lower()
        field_name = field_name.lower()

        if target_type in ("char", "character", "mobile"):
            victim = WizUtil.find_world_entity(self.character_registry, self.room_registry, target_name)
            if victim is None:
                context.finish()
                return self._command_payload("target_missing")
            if field_name == "name":
                if not CharacterApi.is_npc(victim):
                    context.finish()
                    return self._command_payload("pc_invalid")
                victim.name = rest
            elif field_name in ("desc", "description"):
                victim.description = rest
            elif field_name == "short":
                setattr(victim, "short_description", rest)
            elif field_name == "long":
                setattr(victim, "long_description", rest if rest.endswith("\r\n") else rest + "\r\n")
            elif field_name == "title":
                if CharacterApi.is_npc(victim):
                    context.finish()
                    return self._command_payload("npc_invalid")
                victim.title = rest if rest.startswith((" ", ".", ",", "!", "?")) else f" {rest}"
            elif field_name == "spec":
                if not CharacterApi.is_npc(victim):
                    context.finish()
                    return self._command_payload("pc_invalid")
                special = next((entry for entry in self.special_registry.all_specials() if str(getattr(entry, "name", "") or "").strip().lower() == rest.strip().lower()), None)
                if special is None:
                    context.finish()
                    return self._command_payload("no_such_spec_fun")
                victim.special_name = special.name
                victim.special_function = list(getattr(special, "special_function", []) or [])
            else:
                context.finish()
                return self._command_payload("syntax")
            context.finish()
            return {"to_char": ""}

        if target_type in ("obj", "object"):
            obj = WizUtil.find_world_item(self.character_registry, self.room_registry, target_name)
            if obj is None:
                context.finish()
                return self._command_payload("no_such_object")
            if field_name == "name":
                obj.name = rest
            elif field_name == "short":
                obj.short_description = rest
            elif field_name == "long":
                obj.long_description = rest
            elif field_name in ("ed", "extended"):
                pieces = rest.split(maxsplit=1)
                if len(pieces) < 2:
                    context.finish()
                    return self._command_payload("oset_syntax")
                keyword, description = pieces
                obj.extra_descr = [keyword, description]
                obj.extra_description = ExtraDescriptionData(valid=True, keyword=keyword, description=description)
            else:
                context.finish()
                return self._command_payload("syntax")
            context.finish()
            return {"to_char": ""}

        context.finish()
        return self._command_payload("syntax")

    def do_switch(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        target = WizUtil.find_world_entity(self.character_registry, self.room_registry, WizUtil.argument_text(context.result, context.parameters))
        if target == character:
            context.finish()
            return self._command_payload("default")
        self.wiz_handler.switch_character(character, target)
        context.character = target
        context.finish()
        return self._command_payload(
            "default",
            view_character=target,
            wiznet_actor=character,
            wiznet_flag="WIZ_SWITCHES",
            wiznet_skip_flag="WIZ_SECURE",
            wiznet_min_level=CharacterApi.get_trust(character),
            tokens={"c": getattr(character, "name", ""), "t": WizUtil.display_name(target)},
        )

    def do_clone(self, character: Character, context: Context):
        blocked = self.interp_api.evaluate_guards_only(context, context.command.name)
        if blocked is not None:
            return blocked
        room = self.room_registry.get_or_none(id=character.room_id)
        raw = WizUtil.argument_text(context.result, context.parameters)
        arg1, rest = WizUtil.split_argument(raw)
        obj = None
        mob = None
        if arg1 in ("object", "obj"):
            obj = ItemUtil.find_item(character, room, rest)
        elif arg1 in ("mobile", "character", "mob"):
            mob = None if room is None else room.find_visible_target(character, rest)
        else:
            obj = ItemUtil.find_item(character, room, raw)
            mob = None if room is None else room.find_visible_target(character, raw)
        if obj is None and mob is None:
            context.finish()
            return self._command_payload("target_missing")
        if obj is not None:
            if not WizUtil.can_clone_object(character, obj):
                context.finish()
                return self._command_payload("insufficient_level")
            clone = ItemUtil.clone_object_instance(obj)
            if room is not None and obj in room.contents.values():
                room.add_item_to_room(clone)
            elif CharacterApi.is_npc(character):
                MobileUtil.add_inventory_item(character, clone)
            else:
                character.add_item(clone)
            context.finish()
            return {
                **self._command_payload("default", wiznet_flag="WIZ_LOAD", wiznet_skip_flag="WIZ_SECURE", wiznet_min_level=CharacterApi.get_trust(character), tokens={"t": clone.short_description}),
                "room_message": f"{character.name} has created {clone.short_description}.\r\n",
                "room_targets": [] if room is None else room.player_targets(character),
            }
        if not CharacterApi.is_npc(mob):
            context.finish()
            return self._command_payload("mobiles_only")
        if not WizUtil.can_clone_mobile(character, mob):
            context.finish()
            return self._command_payload("insufficient_level")
        clone = MobileUtil.clone_mobile_instance(mob, CharacterApi.enums())
        if room is not None:
            room.add_mobile_to_room(clone)
        context.finish()
        return {
            **self._command_payload("default", wiznet_flag="WIZ_LOAD", wiznet_skip_flag="WIZ_SECURE", wiznet_min_level=CharacterApi.get_trust(character), tokens={"t": clone.short_description}),
            "room_message": f"{character.name} has created {clone.short_description}.\r\n",
            "room_targets": [] if room is None else room.player_targets(character),
        }

    @staticmethod
    def _command_payload(message_key: str, *, victim=None, targets=None, channel: str = "", tokens: dict | None = None, **extra) -> dict:
        payload = {"message_key": str(message_key or "")}
        if channel:
            payload["channel"] = channel
        if victim is not None:
            payload["victim"] = victim
        if targets is not None:
            payload["targets"] = list(targets)
        if tokens:
            payload["tokens"] = dict(tokens)
        payload.update(extra)
        return payload

    def _command_text(self, context: Context, message_key: str, *, channel: str = "to_char", fallback: str = "", **tokens) -> str:
        payload = self.interp_api.render_message_key(context, message_key, channel=channel, fallback=fallback, **tokens)
        return str(payload.get(channel, "") or "")

    @staticmethod
    def _poof_text(character, key: str, default: str) -> str:
        return str((getattr(character, "context", {}) or {}).get(key, "") or default)

    @staticmethod
    def _visible_room_targets(room: Room | None, character) -> list:
        if room is None:
            return []
        return [
            viewer for viewer in room.player_targets(character)
            if CharacterApi.get_trust(viewer) >= GenericUtil.to_int(getattr(character.status_flags, "invis_level", 0), 0)
        ]

    @staticmethod
    def _stat_character_text(target) -> str:
        return (
            f"{WizUtil.display_name(target)} lvl {getattr(target, 'level', 0)} "
            f"hp {getattr(target, 'hit', 0)}/{getattr(target, 'max_hit', 0)} "
            f"mana {getattr(target, 'mana', 0)}/{getattr(target, 'max_mana', 0)} "
            f"mv {getattr(target, 'movement', 0)}/{getattr(target, 'max_movement', 0)}\r\n"
        )

    @staticmethod
    def _stat_object_text(obj) -> str:
        return (
            f"Obj [{obj.vnum}] {obj.short_description}\r\n"
            f"Type: {obj.item_type} Flags: {obj.extra_flags} Wear: {obj.wear_flags}\r\n"
        )
