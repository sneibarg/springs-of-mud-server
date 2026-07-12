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
from util.GenericUtil import GenericUtil


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
        return {"to_char": missed_tells}

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
        character = context.character
        view = self.interp_api.build_interp_view(context)
        target = self.communications_api.follow_target(view)
        context.follow_target = target
        if target is not None:
            context.interp_tokens = self.communications_api.follow_target_tokens(view)
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload

        if target == character:
            previous = self._stop_following(character)
            context.finish()
            return {} if previous is None else self._follow_payload(context, "stop", previous)

        self._clear_nofollow(character)
        payload["victim"] = target
        if not self._can_receive_follow_notice(context, target, character):
            payload.pop("to_victim", None)
        if getattr(character, "master", None) is not None:
            previous = self._stop_following(character)
            if previous is not None:
                character.master = target
                context.finish()
                return {"payloads": [self._follow_payload(context, "stop", previous), payload]}

        character.master = target
        character.leader = None
        context.finish()
        return payload

    def do_order(self, context: Context):
        view = self.interp_api.build_interp_view(context)
        context.interp_tokens = self.communications_api.order_tokens(view)
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload

        targets = self.communications_api.order_targets(view)
        if not targets:
            return self._blocked_message(context, "no_followers")

        game_params = CharacterApi.get_enum("gameParameters")
        pulse_violence = CharacterApi.enum_bit(game_params, "PULSE_VIOLENCE") if game_params is not None else 12
        status_flags = getattr(context.character, "status_flags", None)
        if status_flags is not None:
            status_flags.pulse_wait = max(GenericUtil.to_int(getattr(status_flags, "pulse_wait", 0), 0), pulse_violence or 12)

        _target, command_text, _command = self.communications_api.order_args(view)
        context.finish()
        return {
            "ordered_commands": [{"victim": target, "command": command_text} for target in targets],
            "order_message_key": "ordered",
            "to_char": payload.get("to_char", ""),
        }

    def do_group(self, context: Context):
        if not CommunicationsUtil.parse_argument(context.result, context.parameters):
            context.finish()
            return {"to_char": self._group_listing(context)}

        view = self.interp_api.build_interp_view(context)
        context.interp_tokens = self.communications_api.group_target_tokens(view)
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            if payload.get("to_victim") and not payload.get("victim"):
                payload["victim"] = self.communications_api.group_target(view)
            return payload

        character = context.character
        victim = self.communications_api.group_target(view)
        if CharacterApi.is_same_group(victim, character) and victim != character:
            victim.leader = None
            return self._group_payload(context, "removal", victim)

        victim.leader = character
        return self._group_payload(context, "addition", victim)

    def do_split(self, context: Context):
        view = self.interp_api.build_interp_view(context)
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload

        character = context.character
        amounts = self.communications_api.split_amounts(view)
        shares = self.communications_api.split_shares(view)
        members = self.communications_api.split_members(view)

        character.silver = GenericUtil.to_int(getattr(character, "silver", 0), 0) - amounts["silver"] + shares["silver"] + shares["extra_silver"]
        character.gold = GenericUtil.to_int(getattr(character, "gold", 0), 0) - amounts["gold"] + shares["gold"] + shares["extra_gold"]

        to_char = ""
        if shares["silver"] > 0:
            to_char += self._render_message_key(
                context,
                "split_silver_coins_share",
                channel="to_char",
                amount_silver=amounts["silver"],
                share_silver=shares["silver"] + shares["extra_silver"],
            ).get("to_char", "")
        if shares["gold"] > 0:
            to_char += self._render_message_key(
                context,
                "split_gold_coins_share",
                channel="to_char",
                amount_gold=amounts["gold"],
                share_gold=shares["gold"] + shares["extra_gold"],
            ).get("to_char", "")

        victim_message_key = "split_silver_victim"
        if shares["gold"] > 0 and shares["silver"] == 0:
            victim_message_key = "split_gold_victim"
        elif shares["gold"] > 0 and shares["silver"] > 0:
            victim_message_key = "split_both_victim"

        target_messages = []
        for member in members:
            if member == character:
                continue
            member.gold = GenericUtil.to_int(getattr(member, "gold", 0), 0) + shares["gold"]
            member.silver = GenericUtil.to_int(getattr(member, "silver", 0), 0) + shares["silver"]
            target_messages.append({
                "id": getattr(member, "id", ""),
                "text": self._render_message_key(
                    context,
                    victim_message_key,
                    channel="to_victim",
                    amount_silver=amounts["silver"],
                    amount_gold=amounts["gold"],
                    share_silver=shares["silver"],
                    share_gold=shares["gold"],
                ).get("to_victim", ""),
            })

        context.finish()
        return {"to_char": to_char, "target_messages": target_messages}

    def _group_listing(self, context: Context) -> str:
        view = self.interp_api.build_interp_view(context)
        character = context.character
        leader = getattr(character, "leader", None) or character
        lines = [f"{self._display_name(leader)}'s group:"]
        for member in self.communications_api.group_members(view):
            lines.append(self._group_member_line(member))
        return "\r\n".join(lines) + "\r\n"

    def _group_member_line(self, member) -> str:
        class_name = "Mob" if CharacterApi.is_npc(member) else self._class_who_name(member)
        attrs = getattr(member, "character_attributes", None)
        exp = GenericUtil.to_int(getattr(attrs, "experience", getattr(member, "experience", 0)), 0)
        return (
            f"[{GenericUtil.to_int(getattr(member, 'level', 0), 0):2d} {class_name}] "
            f"{self._display_name(member).capitalize():<16} "
            f"{GenericUtil.to_int(getattr(member, 'hit', 0), 0):4d}/{GenericUtil.to_int(getattr(member, 'max_hit', 0), 0):4d} hp "
            f"{GenericUtil.to_int(getattr(member, 'mana', 0), 0):4d}/{GenericUtil.to_int(getattr(member, 'max_mana', 0), 0):4d} mana "
            f"{GenericUtil.to_int(getattr(member, 'movement', 0), 0):4d}/{GenericUtil.to_int(getattr(member, 'max_movement', 0), 0):4d} mv "
            f"{exp:5d} xp"
        )

    @staticmethod
    def _class_who_name(member) -> str:
        character_class = getattr(member, "character_class", None)
        who = getattr(character_class, "who_name", None)
        if who:
            return str(who)
        name = str(getattr(character_class, "name", "") or "")
        return name[:3].capitalize() if name else "Mob"

    @staticmethod
    def _display_name(member) -> str:
        return str(getattr(member, "name", "") or getattr(member, "short_description", "") or "someone")

    def _group_payload(self, context: Context, message_key: str, victim) -> dict:
        actor_sex = str(getattr(context.character, "sex", "") or "").strip().lower()
        s_poss = "his" if actor_sex in ("1", "male", "m") else "her" if actor_sex in ("2", "female", "f") else "its"
        m_pronoun = "him" if actor_sex in ("1", "male", "m") else "her" if actor_sex in ("2", "female", "f") else "it"
        context.interp_tokens = {
            "t": self._display_name(victim),
            "m": self._display_name(context.character),
            "s_poss": s_poss,
            "m_pronoun": m_pronoun,
        }
        payload = self._render_message_key(context, message_key)
        payload["victim"] = victim
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=getattr(context.character, "room_id", ""))
        targets = []
        if room is not None:
            targets = [
                target for target in list((getattr(room, "characters", {}) or {}).values())
                if target not in (context.character, victim)
            ]
        payload["targets"] = targets
        context.finish()
        return payload

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

    def _clear_nofollow(self, character) -> None:
        bit = CharacterApi.enum_bit(CharacterApi.get_enum("playerActBits"), "PLR_NOFOLLOW")
        if bit:
            CharacterApi.unset_act_flags(character, bit)
        if getattr(character, "character_flags", None) is not None:
            character.character_flags.no_follow = False

    @staticmethod
    def _stop_following(character):
        previous = getattr(character, "master", None)
        character.master = None
        return previous

    def _follow_payload(self, context: Context, message_key: str, victim) -> dict:
        context.interp_tokens = {"t": getattr(victim, "name", "")}
        payload = self._render_message_key(context, message_key)
        payload["victim"] = victim
        if not self._can_receive_follow_notice(context, victim, context.character):
            payload.pop("to_victim", None)
        return payload

    def _can_receive_follow_notice(self, context: Context, viewer, character) -> bool:
        room = context.room
        if room is None:
            room = self.room_registry.get_or_none(id=getattr(character, "room_id", ""))
        try:
            return CharacterApi.can_see(viewer, character, room)
        except (AttributeError, TypeError):
            return True
