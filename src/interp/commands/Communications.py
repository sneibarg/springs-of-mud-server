from __future__ import annotations

import random

from injector import inject

from api.CommunicationsApi import CommunicationsApi
from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from interp.Context import Context
from api.InterpApi import InterpApi
from util.CommunicationsUtil import CommunicationsUtil
from api.CharacterApi import CharacterApi
from player.CharacterService import CharacterService
from server.LoggerFactory import LoggerFactory
from server.session.SessionHandler import SessionHandler


class Communications:
    POSES = [
        "strikes a heroic pose.",
        "looks around cautiously.",
        "smiles happily.",
        "yawns loudly.",
        "ponders the meaning of life.",
    ]

    @inject
    def __init__(self,
                 registry_service: RegistryService,
                 session_handler: SessionHandler,
                 character_service: CharacterService,
                 enum_provider: EnumProvider,
                 interp_api: InterpApi):
        self.__name__ = "Communications"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.session_handler = session_handler
        self.character_service = character_service
        self.interp_api = interp_api
        self.communications_api = CommunicationsApi
        self.comm_flags = enum_provider.get("commFlags")

    def execute(self, context: Context):
        name = (context.command.name or "").strip().lower()
        handlers = {
            "say": self.do_say,
            "tell": self.do_tell,
            "reply": self.do_reply,
            "yell": self.do_yell,
            "shout": self.do_shout,
            "emote": self.do_emote,
            "pmote": self.do_pmote,
            "pose": self.do_pose,
            "gtell": self.do_gtell,
            "gossip": self.do_gossip,
            ",": self.do_gossip,
            "auction": self.do_auction,
            "music": self.do_music,
            "question": self.do_question,
            "answer": self.do_question,
            "quote": self.do_quote,
            ";": self.do_quote,
            "grats": self.do_grats,
            ".": self.do_grats,
            "afk": self.do_afk,
            "quiet": self.do_quiet,
            "channels": self.do_channels,
            "deaf": self.do_deaf,
            "replay": self.do_replay,
            "bug": self.do_bug,
            "typo": self.do_typo,
            "rent": self.do_rent,
            "save": self.do_save,
            "follow": self.do_follow,
            "order": self.do_order,
            "group": self.do_group,
            "split": self.do_split,
        }
        fn = handlers.get(name)
        if fn is None:
            context.finish()
            return {"to_char": f"{name} is not implemented yet.\r\n"}
        return fn(context)

    def do_channels(self, context: Context):
        character = context.character

        def on_off(bit_name: str) -> str:
            return "OFF" if CommunicationsUtil.has_comm(character, self.comm_flags, bit_name) else "ON"

        lines = [
            "   channel     status",
            "---------------------",
            f"gossip         {on_off('COMM_NOGOSSIP')}",
            f"auction        {on_off('COMM_NOAUCTION')}",
            f"music          {on_off('COMM_NOMUSIC')}",
            f"Q/A            {on_off('COMM_NOQUESTION')}",
            f"Quote          {on_off('COMM_NOQUOTE')}",
            f"grats          {on_off('COMM_NOGRATS')}",
            f"shouts         {'OFF' if CommunicationsUtil.has_comm(character, self.comm_flags, 'COMM_SHOUTSOFF') else 'ON'}",
            f"tells          {'OFF' if CommunicationsUtil.has_comm(character, self.comm_flags, 'COMM_DEAF') else 'ON'}",
            f"quiet mode     {'ON' if CommunicationsUtil.has_comm(character, self.comm_flags, 'COMM_QUIET') else 'OFF'}",
        ]
        if CharacterApi.is_immortal(character):
            lines.insert(8,
                         f"god channel    {'OFF' if CommunicationsUtil.has_comm(character, self.comm_flags, 'COMM_NOWIZ') else 'ON'}")
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_AFK"):
            lines.append("You are AFK.")
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOSHOUT"):
            lines.append("You cannot shout.")
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOTELL"):
            lines.append("You cannot use tell.")
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOCHANNELS"):
            lines.append("You cannot use channels.")
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOEMOTE"):
            lines.append("You cannot show emotions.")
        prompt_text = character.prompt_format.current_prompt_text()
        if prompt_text:
            lines.append(f"Your current prompt is: {prompt_text}")
        context.finish()
        return {"to_char": "\r\n".join(lines) + "\r\n"}

    def do_deaf(self, context: Context):
        character = context.character
        enabled = CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_DEAF")
        CommunicationsUtil.set_comm(character, self.comm_flags, "COMM_DEAF", not enabled)
        context.finish()
        return self._render_message_key(context, "disable" if enabled else "enable")

    def do_quiet(self, context: Context):
        character = context.character
        enabled = CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_QUIET")
        CommunicationsUtil.set_comm(character, self.comm_flags, "COMM_QUIET", not enabled)
        context.finish()
        return self._render_message_key(context, "disable" if enabled else "enable")

    def do_afk(self, context: Context):
        character = context.character
        payload = self.interp_api.run_action(context, context.command.name)
        if "enable" in payload:
            enabled = True
        elif "disable" in payload:
            enabled = False
        CommunicationsUtil.set_comm(character, self.comm_flags, "COMM_AFK", enabled)
        context.finish()
        return self._render_message_key(context, "disable" if enabled else "enable")

    def do_replay(self, context: Context):
        character = context.character
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        history = self.communications_api.get_tell_buffer(character)
        missed_tells = "".join(entry.format_message() for entry in history)
        return missed_tells

    def do_say(self, context: Context):
        character = context.character
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        payload["targets"] = room.player_targets(character)
        return payload

    def do_emote(self, context: Context):
        character = context.character
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        payload["targets"] = self._room_targets(character, room)
        return payload

    def do_pmote(self, context: Context):
        character = context.character
        # Minimal pass-through; per-target rewriting can be added in parity pass.
        return self.do_emote(character, context)

    def do_pose(self, context: Context):
        character = context.character
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        text = random.choice(self.POSES)
        context.finish()
        return {
            "to_char": f"You {text}\r\n",
            "to_room": f"{character.name} {text}\r\n",
            "targets": self._room_targets(character, room),
        }

    def do_tell(self, context: Context):
        character = context.character
        target_name, message = CommunicationsUtil.split_first(
            CommunicationsUtil.parse_argument(context.result, context.parameters))
        context.tell_target_name = target_name
        context.tell_target = CharacterApi.find_playing_character(target_name, self.session_handler)
        context.interp_tokens = {"t": target_name, "s": message}
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        victim = context.tell_target
        if victim is None:
            return self._blocked_message(context, "target_missing")
        return self._deliver_tell(context, victim, message)

    def do_reply(self, context: Context):
        character = context.character
        message = CommunicationsUtil.parse_argument(context.result, context.parameters)
        reply_to = (character.context or {}).get("reply_to", "")
        victim = self.character_registry.get_or_none(id=reply_to)
        context.reply_target = victim
        context.interp_tokens = {"s": message, "t": "" if victim is None else victim.name}
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        if victim is None:
            return self._blocked_message(context, "target_missing")
        return self._deliver_tell(context, victim, message)

    def do_shout(self, context: Context):
        character = context.character
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        payload["area_id"] = character.area_id
        return payload

    def do_yell(self, context: Context):
        character = context.character
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        targets = []
        for session in self.session_handler.get_playing_sessions():
            victim = session.character
            if victim is None or victim.id == character.id:
                continue
            if str(victim.area_id) == str(character.area_id):
                targets.append(victim)
        payload["global_message"] = f"{character.name} yells '{text}'\r\n"
        payload["global_targets"] = targets
        return payload

    def do_gossip(self, context: Context):
        return self._channel(context, "COMM_NOGOSSIP", "gossip", "Gossip channel is now ON.\r\n",
                             "Gossip channel is now OFF.\r\n")

    def do_auction(self, context: Context):
        return self._channel(context, "COMM_NOAUCTION", "auction", "Auction channel is now ON.\r\n",
                             "Auction channel is now OFF.\r\n")

    def do_music(self, context: Context):
        return self._channel(context, "COMM_NOMUSIC", "music", "Music channel is now ON.\r\n",
                             "Music channel is now OFF.\r\n")

    def do_question(self, context: Context):
        return self._channel(context, "COMM_NOQUESTION", "question", "Q/A channel is now ON.\r\n",
                             "Q/A channel is now OFF.\r\n")

    def do_quote(self, context: Context):
        return self._channel(context, "COMM_NOQUOTE", "quote", "Quote channel is now ON.\r\n",
                             "Quote channel is now OFF.\r\n")

    def do_grats(self, context: Context):
        return self._channel(context, "COMM_NOGRATS", "grats", "Grats channel is now ON.\r\n",
                             "Grats channel is now OFF.\r\n")

    def do_gtell(self, context: Context):
        character = context.character
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        payload.setdefault("to_room",
                           f"{character.name} tells the group '{CommunicationsUtil.parse_argument(context.result, context.parameters)}'\r\n")
        payload["targets"] = room.player_targets(character)
        return payload

    def do_bug(self, context: Context):
        return self.interp_api.run_action(context, context.command.name)

    def do_typo(self, context: Context):
        return self.interp_api.run_action(context, context.command.name)

    def do_rent(self, context: Context):
        return self.interp_api.run_action(context, context.command.name)

    def do_save(self, context: Context):
        character = context.character
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload
        if self.character_service.save_character(character):
            return payload
        return self._render_message_key(context, "failed")

    def do_follow(self, context: Context):
        context.finish()
        return {"to_char": "Follow is not implemented yet.\r\n"}

    def do_order(self, context: Context):
        context.finish()
        return {"to_char": "Order is not implemented yet.\r\n"}

    def do_group(self, context: Context):
        context.finish()
        return {"to_char": "Group is not implemented yet.\r\n"}

    def do_split(self, context: Context):
        context.finish()
        return {"to_char": "Split is not implemented yet.\r\n"}

    def _channel(self, context: Context, off_flag: str, verb: str, _on_msg: str, _off_msg: str):
        character = context.character
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        if not text:
            is_off = CommunicationsUtil.has_comm(character, self.comm_flags, off_flag)
            CommunicationsUtil.set_comm(character, self.comm_flags, off_flag, not is_off)
            context.finish()
            return self._render_message_key(context, "enable" if is_off else "disable")

        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload

        CommunicationsUtil.set_comm(character, self.comm_flags, off_flag, False)
        channel_map = {
            "gossip": "COMM_NOGOSSIP",
            "auction": "COMM_NOAUCTION",
            "music": "COMM_NOMUSIC",
            "question": "COMM_NOQUESTION",
            "quote": "COMM_NOQUOTE",
            "grats": "COMM_NOGRATS",
        }
        targets = []
        for session in self.session_handler.get_playing_sessions():
            victim = session.character
            if victim is None or victim.id == character.id:
                continue
            if CommunicationsUtil.has_comm(victim, self.comm_flags, "COMM_QUIET"):
                continue
            if CommunicationsUtil.has_comm(victim, self.comm_flags, channel_map[verb]):
                continue
            targets.append(victim)

        payload["global_message"] = payload.pop("to_world", "")
        payload["global_targets"] = targets
        return payload

    def _deliver_tell(self, context: Context, victim, message: str) -> dict:
        character = context.character
        if character.context is None:
            character.context = {}
        if victim.context is None:
            victim.context = {}

        character.context["reply_to"] = victim.id
        victim.context["reply_to"] = character.id
        context.interp_tokens = {"t": victim.name, "s": message}

        payload = self._render_message_key(context, "default")
        payload["victim"] = victim
        self.communications_api.append_tell_buffer(victim, character, payload.get("to_victim", ""))
        if CommunicationsUtil.has_comm(victim, self.comm_flags, "COMM_AFK"):
            payload["to_char"] = payload.get("to_char", "") + self._render_message_key(context, "target_afk",
                                                                                       channel="to_char").get("to_char",
                                                                                                              "")
        return payload

    def _render_message_key(self, context: Context, message_key: str, channel: str = "", **tokens):
        return self.interp_api.render_message_key(context, message_key, channel=channel, **tokens)

    def _blocked_message(self, context: Context, message_key: str, channel: str = "", **tokens):
        payload = self._render_message_key(context, message_key, channel=channel, **tokens)
        payload["blocked"] = True
        return payload
