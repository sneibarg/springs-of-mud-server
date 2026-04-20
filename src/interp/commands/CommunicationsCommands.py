from __future__ import annotations

import random
from injector import inject

from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.CommunicationsUtil import CommunicationsUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from server.session.SessionHandler import SessionHandler


class CommunicationsCommands:
    POSES = [
        "strikes a heroic pose.",
        "looks around cautiously.",
        "smiles happily.",
        "yawns loudly.",
        "ponders the meaning of life.",
    ]

    @inject
    def __init__(self, registry_service: RegistryService, character_macros: CharacterMacros, session_handler: SessionHandler):
        self.__name__ = "CommunicationsCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.registry_service = registry_service
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.character_macros = character_macros
        self.session_handler = session_handler
        self.comm_flags = character_macros.enums.get("commFlags")

    def execute(self, character: Character, context: Context):
        name = (getattr(context.command, "name", "") or "").strip().lower()
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
            "qui": self.do_qui,
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
        return fn(character, context)

    def do_channels(self, character: Character, context: Context):
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
        if self.character_macros.is_immortal(character):
            lines.insert(8, f"god channel    {'OFF' if CommunicationsUtil.has_comm(character, self.comm_flags, 'COMM_NOWIZ') else 'ON'}")
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

    def do_deaf(self, character: Character, context: Context):
        enabled = CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_DEAF")
        CommunicationsUtil.set_comm(character, self.comm_flags, "COMM_DEAF", not enabled)
        context.finish()
        return {"to_char": "You can now hear tells again.\r\n" if enabled else "From now on, you won't hear tells.\r\n"}

    def do_quiet(self, character: Character, context: Context):
        enabled = CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_QUIET")
        CommunicationsUtil.set_comm(character, self.comm_flags, "COMM_QUIET", not enabled)
        context.finish()
        return {"to_char": "Quiet mode removed.\r\n" if enabled else "From now on, you will only hear says and emotes.\r\n"}

    def do_afk(self, character: Character, context: Context):
        enabled = CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_AFK")
        CommunicationsUtil.set_comm(character, self.comm_flags, "COMM_AFK", not enabled)
        context.finish()
        return {"to_char": "AFK mode removed. Type 'replay' to see tells.\r\n" if enabled else "You are now in AFK mode.\r\n"}

    def do_replay(self, character: Character, context: Context):
        history = (character.context or {}).get("tell_buffer", [])
        context.finish()
        if not history:
            return {"to_char": "You have no tells to replay.\r\n"}
        character.context["tell_buffer"] = []
        return {"to_char": "".join(history)}

    def do_say(self, character: Character, context: Context):
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        if not text:
            context.finish()
            return {"to_char": "Say what?\r\n"}
        room = self.room_registry.get_or_none(id=character.room_id)
        context.finish()
        return {
            "to_char": f"You say '{text}'\r\n",
            "to_room": f"{character.name} says '{text}'\r\n",
            "targets": self._room_targets(character, room),
        }

    def do_emote(self, character: Character, context: Context):
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOEMOTE"):
            context.finish()
            return {"to_char": "You can't show your emotions.\r\n"}
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        if not text:
            context.finish()
            return {"to_char": "Emote what?\r\n"}
        room = self.room_registry.get_or_none(id=character.room_id)
        context.finish()
        return {
            "to_char": f"{character.name} {text}\r\n",
            "to_room": f"{character.name} {text}\r\n",
            "targets": self._room_targets(character, room),
        }

    def do_pmote(self, character: Character, context: Context):
        # Minimal pass-through; per-target rewriting can be added in parity pass.
        return self.do_emote(character, context)

    def do_pose(self, character: Character, context: Context):
        room = self.room_registry.get_or_none(id=character.room_id)
        text = random.choice(self.POSES)
        context.finish()
        return {
            "to_char": f"You {text}\r\n",
            "to_room": f"{character.name} {text}\r\n",
            "targets": self._room_targets(character, room),
        }

    def do_tell(self, character: Character, context: Context):
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOTELL"):
            context.finish()
            return {"to_char": "Your message didn't get through.\r\n"}
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_QUIET"):
            context.finish()
            return {"to_char": "You must turn off quiet mode first.\r\n"}
        target_name, message = CommunicationsUtil.split_first(CommunicationsUtil.parse_argument(context.result, context.parameters))
        if not target_name or not message:
            context.finish()
            return {"to_char": "Tell whom what?\r\n"}
        victim = self._find_playing_character(target_name)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        if CommunicationsUtil.has_comm(victim, self.comm_flags, "COMM_DEAF") or CommunicationsUtil.has_comm(victim, self.comm_flags, "COMM_QUIET"):
            context.finish()
            return {"to_char": "That player is not receiving tells.\r\n"}
        if CommunicationsUtil.has_comm(victim, self.comm_flags, "COMM_NOTELL"):
            context.finish()
            return {"to_char": "That player is not receiving tells.\r\n"}
        (character.context or {}).update({"reply_to": victim.id})
        (victim.context or {}).update({"reply_to": character.id})
        to_sender = f"You tell {victim.name} '{message}'\r\n"
        to_victim = f"{character.name} tells you '{message}'\r\n"
        CommunicationsUtil.append_tell_buffer(victim, to_victim)
        context.finish()
        payload = {"to_char": to_sender, "to_victim": to_victim, "victim": victim}
        if CommunicationsUtil.has_comm(victim, self.comm_flags, "COMM_AFK"):
            payload["to_char"] += f"{victim.name} is AFK and may not reply.\r\n"
        return payload

    def do_reply(self, character: Character, context: Context):
        message = CommunicationsUtil.parse_argument(context.result, context.parameters)
        if not message:
            context.finish()
            return {"to_char": "Reply what?\r\n"}
        reply_to = (character.context or {}).get("reply_to", "")
        if not reply_to:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        victim = self.character_registry.get_or_none(id=reply_to)
        if victim is None:
            context.finish()
            return {"to_char": "They aren't here.\r\n"}
        context.result = f"{victim.name} {message}"
        context.parameters = []
        return self.do_tell(character, context)

    def do_shout(self, character: Character, context: Context):
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOSHOUT"):
            context.finish()
            return {"to_char": "You can't shout.\r\n"}
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_QUIET"):
            context.finish()
            return {"to_char": "You must turn off quiet mode first.\r\n"}
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        if not text:
            context.finish()
            return {"to_char": "Shout what?\r\n"}
        context.finish()
        return {"to_char": f"You shout '{text}'\r\n", "broadcast_message": f"{character.name} shouts '{text}'\r\n", "exclude_character_ids": [character.id]}

    def do_yell(self, character: Character, context: Context):
        if CommunicationsUtil.has_comm(character, self.comm_flags, "COMM_NOSHOUT"):
            context.finish()
            return {"to_char": "You can't yell.\r\n"}
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        if not text:
            context.finish()
            return {"to_char": "Yell what?\r\n"}
        targets = []
        for session in self.session_handler.get_playing_sessions():
            victim = session.character
            if victim is None or victim.id == character.id:
                continue
            if str(getattr(victim, "area_id", "")) == str(character.area_id):
                targets.append(victim)
        context.finish()
        return {"to_char": f"You yell '{text}'\r\n", "global_message": f"{character.name} yells '{text}'\r\n", "global_targets": targets}

    def do_gossip(self, character: Character, context: Context):
        return self._channel(character, context, "COMM_NOGOSSIP", "gossip", "Gossip channel is now ON.\r\n", "Gossip channel is now OFF.\r\n")

    def do_auction(self, character: Character, context: Context):
        return self._channel(character, context, "COMM_NOAUCTION", "auction", "Auction channel is now ON.\r\n", "Auction channel is now OFF.\r\n")

    def do_music(self, character: Character, context: Context):
        return self._channel(character, context, "COMM_NOMUSIC", "music", "Music channel is now ON.\r\n", "Music channel is now OFF.\r\n")

    def do_question(self, character: Character, context: Context):
        return self._channel(character, context, "COMM_NOQUESTION", "question", "Q/A channel is now ON.\r\n", "Q/A channel is now OFF.\r\n")

    def do_quote(self, character: Character, context: Context):
        return self._channel(character, context, "COMM_NOQUOTE", "quote", "Quote channel is now ON.\r\n", "Quote channel is now OFF.\r\n")

    def do_grats(self, character: Character, context: Context):
        return self._channel(character, context, "COMM_NOGRATS", "grats", "Grats channel is now ON.\r\n", "Grats channel is now OFF.\r\n")

    def do_gtell(self, character: Character, context: Context):
        # Group system parity can be refined once group mechanics are fully migrated.
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        if not text:
            context.finish()
            return {"to_char": "Tell your group what?\r\n"}
        room = self.room_registry.get_or_none(id=character.room_id)
        context.finish()
        return {"to_char": f"You tell your group '{text}'\r\n", "to_room": f"{character.name} tells the group '{text}'\r\n", "targets": self._room_targets(character, room)}

    def do_bug(self, character: Character, context: Context):
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        context.finish()
        if not text:
            return {"to_char": "Bug what?\r\n"}
        return {"to_char": "Bug noted.\r\n"}

    def do_typo(self, character: Character, context: Context):
        text = CommunicationsUtil.parse_argument(context.result, context.parameters)
        context.finish()
        if not text:
            return {"to_char": "Typo what?\r\n"}
        return {"to_char": "Typo noted.\r\n"}

    def do_rent(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "There is no rent here. Just save and quit.\r\n"}

    def do_qui(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "If you want to QUIT, you have to spell it out.\r\n"}

    def do_save(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Saving complete.\r\n"}

    def do_follow(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Follow is not implemented yet.\r\n"}

    def do_order(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Order is not implemented yet.\r\n"}

    def do_group(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Group is not implemented yet.\r\n"}

    def do_split(self, character: Character, context: Context):
        context.finish()
        return {"to_char": "Split is not implemented yet.\r\n"}

    def _channel(self, character: Character, context: Context, off_flag: str, verb: str, on_msg: str, off_msg: str):
        return self.character_macros.channel_payload(character, context, off_flag, verb, on_msg, off_msg, self.comm_flags, self.session_handler, CommunicationsUtil.parse_argument, CommunicationsUtil.has_comm, CommunicationsUtil.set_comm)

    def _room_targets(self, character: Character, room):
        return self.character_macros.room_targets(character, room)

    def _find_playing_character(self, name: str):
        return self.character_macros.find_playing_character(name, self.session_handler)
