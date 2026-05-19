from __future__ import annotations

from copy import deepcopy

from injector import inject

from api.CharacterApi import CharacterApi
from game.RegistryService import RegistryService
from server.LoggerFactory import LoggerFactory
from server.connection.ConnectionManager import ConnectionManager
from server.session.SessionHandler import SessionHandler
from util.GenericUtil import GenericUtil
from util.WizUtil import WizUtil


class WizHandler:
    WIZNET_LEVELS = {
        "WIZ_ON": "LEVEL_IMMORTAL",
        "WIZ_PREFIX": "LEVEL_IMMORTAL",
        "WIZ_TICKS": "LEVEL_IMMORTAL",
        "WIZ_LOGINS": "LEVEL_IMMORTAL",
        "WIZ_SITES": "GOD",
        "WIZ_LINKS": "ANGEL",
        "WIZ_NEWBIE": "LEVEL_IMMORTAL",
        "WIZ_SPAM": "IMMORTAL",
        "WIZ_DEATHS": "LEVEL_IMMORTAL",
        "WIZ_RESETS": "GOD",
        "WIZ_MOBDEATHS": "GOD",
        "WIZ_FLAGS": "IMMORTAL",
        "WIZ_PENALTIES": "IMMORTAL",
        "WIZ_SACCING": "IMMORTAL",
        "WIZ_LEVELS": "LEVEL_IMMORTAL",
        "WIZ_LOAD": "SUPREME",
        "WIZ_RESTORE": "SUPREME",
        "WIZ_SNOOPS": "SUPREME",
        "WIZ_SWITCHES": "SUPREME",
        "WIZ_SECURE": "CREATOR",
    }

    @inject
    def __init__(self,
                 registry_service: RegistryService,
                 session_handler: SessionHandler,
                 connection_manager: ConnectionManager):
        self.__name__ = "WizHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.room_registry = registry_service.room_registry
        self.session_handler = session_handler
        self.connection_manager = connection_manager
        self.log_all = False

    def toggle_log_all(self) -> bool:
        self.log_all = not self.log_all
        return self.log_all

    def current_session(self, character):
        if character is None:
            return None
        return self.session_handler.get_session_by_character(getattr(character, "id", ""))

    def switched_original(self, character):
        session = self.current_session(character)
        if session is None:
            return None
        return session.metadata.get("switched_original")

    def is_switched(self, character) -> bool:
        return self.switched_original(character) is not None

    def switch_character(self, character, target):
        session = self.current_session(character)
        if session is None:
            return None

        original = session.metadata.get("switched_original") or character
        current = session.character
        if current is not None:
            self.connection_manager.unbind_character(getattr(current, "id", ""))

        session.metadata["switched_original"] = original
        session.metadata["switched_original_id"] = getattr(original, "id", "")
        session.character = target
        self.connection_manager.bind_character(getattr(target, "id", ""), session.session_id)

        target.context = dict(getattr(target, "context", {}) or {})
        target.context["controller_original"] = original
        target.context["controller_original_id"] = getattr(original, "id", "")
        if getattr(original, "prompt_format", None) is not None:
            target.prompt_format = deepcopy(original.prompt_format)
        target.carriage_return = bool(getattr(original, "carriage_return", True))
        if getattr(target, "status_flags", None) is not None and getattr(original, "status_flags", None) is not None:
            target.status_flags.comm = getattr(original.status_flags, "comm", 0)
        return original

    def return_character(self, character):
        session = self.current_session(character)
        if session is None:
            return None, None

        original = session.metadata.get("switched_original")
        if original is None:
            return None, None

        current = session.character
        if current is not None:
            self.connection_manager.unbind_character(getattr(current, "id", ""))
            current.context = dict(getattr(current, "context", {}) or {})
            current.context.pop("controller_original", None)
            current.context.pop("controller_original_id", None)

        session.character = original
        self.connection_manager.bind_character(getattr(original, "id", ""), session.session_id)
        session.metadata.pop("switched_original", None)
        session.metadata.pop("switched_original_id", None)
        return original, current

    def cancel_snoops(self, character) -> None:
        session = self.current_session(character)
        if session is None:
            return
        for other in self.session_handler.get_playing_sessions():
            if other.metadata.get("snoop_by_session_id") == session.session_id:
                other.metadata["snoop_by_session_id"] = ""

    def start_snoop(self, character, target) -> bool:
        actor_session = self.current_session(character)
        target_session = self.current_session(target)
        if actor_session is None or target_session is None:
            return False
        target_session.metadata["snoop_by_session_id"] = actor_session.session_id
        return True

    def snoop_loop(self, character, target) -> bool:
        session = self.current_session(character)
        if session is None:
            return False

        current_id = session.metadata.get("snoop_by_session_id", "")
        while current_id:
            current = self.session_handler.get_session(current_id)
            if current is None:
                return False
            if current.character == target or current.metadata.get("switched_original") == target:
                return True
            current_id = current.metadata.get("snoop_by_session_id", "")
        return False

    def room_is_private_for_actor(self, actor, room, *, implementor_only: bool = False) -> bool:
        if actor is None or room is None:
            return False
        actor_room_id = str(getattr(actor, "room_id", "") or "")
        if actor_room_id == str(getattr(room, "id", "") or ""):
            return False

        room_flags = CharacterApi.get_enum("roomFlags")
        if room_flags is None or not room.is_private(room_flags):
            return False

        game_parameters = CharacterApi.get_enum("gameParameters")
        if game_parameters is None:
            return True
        required = game_parameters.IMPLEMENTOR.value if implementor_only and hasattr(game_parameters, "IMPLEMENTOR") else game_parameters.MAX_LEVEL.value
        return CharacterApi.get_trust(actor) < int(required)

    def wiznet_targets(self, actor, *, flag_name: str = "", skip_flag_name: str = "", min_level: int = 0) -> list:
        wiznet_flags = CharacterApi.get_enum("wiznetFlags")
        required_bit = CharacterApi.enum_bit(wiznet_flags, flag_name) if flag_name else 0
        skip_bit = CharacterApi.enum_bit(wiznet_flags, skip_flag_name) if skip_flag_name else 0
        on_bit = CharacterApi.enum_bit(wiznet_flags, "WIZ_ON")
        targets = []
        for session in self.session_handler.get_playing_sessions():
            victim = session.character
            if victim is None or victim == actor:
                continue
            if not CharacterApi.is_immortal(victim):
                continue
            flags = GenericUtil.to_int((getattr(victim, "context", {}) or {}).get("WiznetFlagsEnum", 0), 0)
            if on_bit and (flags & on_bit) == 0:
                continue
            if required_bit and (flags & required_bit) == 0:
                continue
            if skip_bit and (flags & skip_bit) != 0:
                continue
            if CharacterApi.get_trust(victim) < GenericUtil.to_int(min_level, 0):
                continue
            targets.append(victim)
        return targets

    def decorate_wiznet_text(self, recipient, text: str) -> str:
        wiznet_flags = CharacterApi.get_enum("wiznetFlags")
        prefix_bit = CharacterApi.enum_bit(wiznet_flags, "WIZ_PREFIX")
        flags = GenericUtil.to_int((getattr(recipient, "context", {}) or {}).get("WiznetFlagsEnum", 0), 0)
        if prefix_bit and (flags & prefix_bit) != 0:
            return f"--> {text}"
        return text

    def wiznet_option_names(self, actor) -> list[str]:
        names = []
        for field_name in CharacterApi.enum_names(CharacterApi.get_enum("wiznetFlags"), "WIZ_"):
            if self.wiznet_option_level(field_name) > CharacterApi.get_trust(actor):
                continue
            names.append(field_name.replace("WIZ_", "").lower())
        return names

    def wiznet_option_level(self, field_name: str) -> int:
        game_parameters = CharacterApi.get_enum("gameParameters")
        if game_parameters is None:
            return 0
        level_name = self.WIZNET_LEVELS.get(str(field_name or "").strip().upper(), "")
        if level_name and hasattr(game_parameters, level_name):
            return int(getattr(game_parameters, level_name).value)
        return 0

    def render_sockets(self, actor, argument: str) -> str:
        wanted = str(argument or "").strip().lower()
        lines = []
        count = 0
        for session in self.session_handler.get_playing_sessions():
            current = session.character
            if current is None:
                continue
            original = session.metadata.get("switched_original")
            names = [
                str(getattr(current, "name", "") or "").strip().lower(),
                str(getattr(original, "name", "") or "").strip().lower(),
            ]
            if wanted and all(not name or (name != wanted and not name.startswith(wanted)) for name in names):
                continue

            connection = self.connection_manager.get_connection(session.session_id)
            descriptor = -1
            host = "unknown"
            if connection is not None:
                try:
                    sock = connection.writer.get_extra_info("socket")
                    descriptor = -1 if sock is None else int(sock.fileno())
                except Exception:
                    descriptor = -1
                peer = connection.get_peer_info()
                if isinstance(peer, tuple) and len(peer) > 0:
                    host = str(peer[0] or "unknown")
                else:
                    host = str(peer or "unknown")

            name = getattr(original, "name", "") if original is not None else getattr(current, "name", "")
            lines.append(f"[{descriptor:>3} {int(getattr(session.status, 'value', 0)):>2}] {name}@{host}")
            count += 1

        if count == 0:
            return "No one by that name is connected.\r\n"
        suffix = "" if count == 1 else "s"
        return "\r\n".join(lines) + f"\r\n{count} user{suffix}\r\n"

    def memory_report(self) -> str:
        areas = len(list(getattr(self.registry_service.area_registry, "all_areas", lambda: [])() or []))
        rooms = len(list(self.room_registry.all_rooms() or []))
        helps = len([command for command in self.registry_service.interp_registry.all_commands() if getattr(command, "help", None) is not None])
        socials = len(list(self.registry_service.social_registry.all_socials() or []))
        mobs = len(list(self.registry_service.mobile_registry.all_mobiles() or []))
        items = len(list(self.registry_service.item_registry.all_items() or []))
        resets = len(list(self.registry_service.reset_registry.all_resets() or []))
        shops = len(list(self.registry_service.shop_registry.all_shops() or []))
        exits = 0
        exdes = 0
        mobile_count = 0
        for room in self.room_registry.all_rooms():
            exits += len(list(getattr(room, "exits", []) or []))
            exdes += 1 if getattr(room, "extra_description", None) else 0
            mobile_count += len(list(getattr(room, "mobiles", {}).values()))
            for obj in list(getattr(room, "contents", {}).values()):
                exdes += WizUtil.count_extra_descriptions(obj)

        lines = [
            f"Affects {WizUtil.count_active_effects(self.registry_service):5d}",
            f"Areas   {areas:5d}",
            f"ExDes   {exdes:5d}",
            f"Exits   {exits:5d}",
            f"Helps   {helps:5d}",
            f"Socials {socials:5d}",
            f"Mobs    {mobs:5d}",
            f"(in use){mobile_count:5d}",
            f"Objs    {items:5d}",
            f"Resets  {resets:5d}",
            f"Rooms   {rooms:5d}",
            f"Shops   {shops:5d}",
        ]
        return "\r\n".join(lines) + "\r\n"
