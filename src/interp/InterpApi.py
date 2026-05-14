from __future__ import annotations

from dataclasses import fields
from functools import lru_cache
from typing import Any, Callable
from injector import inject

from game.action import ActionCheck, ActionDefinition, ActionPlan, MessageRef
from interp.InterpView import InterpView
from game.GamePayload import GamePayload
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from util.CommunicationsUtil import CommunicationsUtil
from util.GenericUtil import GenericUtil


class InterpApi:
    @inject
    def __init__(self):
        self.__name__ = "InterpApi"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def run_action(self, context, action_name: str):
        view = self.build_interp_view(context)
        self.logger.info(f"View payload: {view.context.command.payload}")
        definition = self._interp_action_definition(view, action_name)
        self.logger.info(f"Definition: {definition}")
        plan = self.evaluate_interp_action(view, definition)
        self.logger.info(f"Plan: {plan}")
        context.finish()
        return self.execute_interp_plan(view, plan)

    @staticmethod
    def build_interp_view(context) -> InterpView:
        payload = getattr(getattr(context, "command", None), "payload", None)
        return InterpView(context=context, payload=GamePayload.from_json(payload))

    @staticmethod
    def evaluate_interp_action(view: InterpView, definition: ActionDefinition[InterpView]) -> ActionPlan:
        for check in definition.checks:
            if check.predicate(view):
                tokens = InterpApi._default_tokens(view)
                tokens.update(dict(check.token_factory(view) or {}))
                return ActionPlan(
                    stop=True,
                    messages=tuple(InterpApi._message_refs_for_key(view.payload, check.message_key, tokens=tokens, fallback=check.fallback, channel=check.channel)),
                    data={"blocked": True},
                )
        return definition.plan_factory(view)

    def execute_interp_plan(self, view: InterpView, plan: ActionPlan):
        payload = self.render_plan_payload(view.payload, plan)
        payload.update(dict(plan.data or {}))
        return payload

    def render_plan_payload(self, payload_def: GamePayload, plan: ActionPlan) -> dict:
        payload: dict[str, Any] = {}
        self.logger.info(f"Plan: {plan}")
        for msg in plan.messages:
            text = payload_def.render(msg.channel, msg.key, msg.fallback, **msg.tokens)
            if not text:
                continue
            payload[msg.channel] = InterpApi._ensure_message_break(text)
        self.logger.debug(f"Plan payload: {payload}")
        return payload

    def render_message_key(self, context, message_key: str, channel: str = "", fallback: str = "", **tokens) -> dict:
        view = self.build_interp_view(context)
        self.logger.info(f"View payload: {view.context.command.payload}")
        merged_tokens = self._default_tokens(view)
        merged_tokens.update(tokens)
        plan = ActionPlan(
            messages=tuple(self._message_refs_for_key(view.payload, message_key, tokens=merged_tokens, fallback=fallback, channel=channel)),
            data={},
        )
        return self.render_plan_payload(view.payload, plan)

    def _interp_action_definition(self, view: InterpView, action_name: str) -> ActionDefinition[InterpView]:
        command = view.context.command
        command_name = str(getattr(command, "name", "") or action_name).strip().lower()
        if command is None:
            raise KeyError(f"No interp action definition for '{command_name}'")

        return ActionDefinition(
            name=str(getattr(command, "name", "") or command_name),
            checks=self._build_checks(command),
            plan_factory=self._default_plan,
        )

    def _build_checks(self, command) -> tuple[ActionCheck[InterpView], ...]:
        checks: list[ActionCheck[InterpView]] = []
        for entry in list(getattr(command, "checks", []) or []):
            predicate_src = str(entry.get("predicate", "") or "").strip()
            if not predicate_src:
                continue
            token_factory_src = str(entry.get("token_factory", "") or "").strip()
            checks.append(
                ActionCheck(
                    predicate=self._compile_lambda(predicate_src),
                    channel=str(entry.get("channel", "") or "").strip(),
                    message_key=str(entry.get("message_key", "") or "").strip(),
                    fallback=str(entry.get("fallback", "") or ""),
                    token_factory=self._compile_lambda(token_factory_src) if token_factory_src else self._empty_tokens,
                )
            )
        return tuple(checks)

    @staticmethod
    def _ensure_message_break(text: str) -> str:
        rendered = str(text or "")
        if rendered and not rendered.endswith("\r\n"):
            rendered += "\r\n"
        return rendered

    @staticmethod
    def _default_plan(view: InterpView) -> ActionPlan:
        messages = tuple(InterpApi._default_message_refs(view))
        return ActionPlan(messages=messages, data={"blocked": False})

    @staticmethod
    def _default_message_refs(view: InterpView) -> list[MessageRef]:
        payload = view.payload or GamePayload()
        tokens = InterpApi._default_tokens(view)
        refs: list[MessageRef] = []
        for field_info in fields(payload):
            channel = str(field_info.name)
            table = getattr(payload, channel, {}) or {}
            if "default" not in table:
                continue
            refs.append(MessageRef(channel=channel, key="default", tokens=dict(tokens)))
        return refs

    @staticmethod
    def _message_refs_for_key(payload: GamePayload | None, message_key: str, *, tokens: dict[str, Any], fallback: str = "", channel: str = "") -> list[MessageRef]:
        payload = payload or GamePayload()
        channels = InterpApi._channels_for_message_key(payload, message_key, channel=channel)
        return [MessageRef(channel=name, key=message_key, fallback=fallback, tokens=dict(tokens)) for name in channels]

    @staticmethod
    def _channels_for_message_key(payload: GamePayload, message_key: str, *, channel: str = "") -> list[str]:
        if channel:
            return [channel]

        channels: list[str] = []
        for field_info in fields(payload):
            field_name = str(field_info.name)
            table = getattr(payload, field_name, {}) or {}
            if message_key in table:
                channels.append(field_name)
        return channels

    @staticmethod
    def _default_tokens(view: InterpView) -> dict[str, Any]:
        actor = getattr(view.context, "character", None)
        argument = InterpApi.argument_text(view)
        target, message = CommunicationsUtil.split_first(argument)
        tokens = {
            "c": str(getattr(actor, "name", "") or ""),
            "s": message or argument,
            "e": argument,
            "t": target or argument,
            "v": target or argument,
        }
        tokens.update(dict(getattr(view.context, "interp_tokens", {}) or {}))
        return tokens

    @staticmethod
    def _empty_tokens(_view: InterpView) -> dict[str, Any]:
        return {}

    @staticmethod
    @lru_cache(maxsize=256)
    def _compile_lambda(source: str) -> type[Callable]:
        text = InterpApi._normalize_view_expression(source)
        if not text:
            return InterpApi._empty_tokens
        globals_dict = {"__builtins__": {}}
        globals_dict.update(InterpApi._lambda_locals())
        func = eval(text, globals_dict, {})
        if not callable(func):
            raise TypeError(f"Interp check lambda must be callable: {text}")
        return func

    @staticmethod
    def _normalize_view_expression(source: str) -> str:
        text = str(source or "").strip()
        replacements = {
            "v.argument": "v.context.argument",
            "v.room": "v.context.room",
            "v.command": "v.context.command",
            "v.current_fighting": "v.context.character.fighting",
            "v.position": "v.context.character.character_attributes.position",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    @staticmethod
    def argument_text(view: InterpView) -> str:
        context = view.context
        result = getattr(context, "result", "")
        text = (result if isinstance(result, str) else "").strip()
        if text:
            return text
        return " ".join(getattr(context, "parameters", []) or []).strip()

    @staticmethod
    def tell_target_name(view: InterpView) -> str:
        context = view.context
        override = str(getattr(context, "tell_target_name", "") or "").strip()
        if override:
            return override
        target, _message = CommunicationsUtil.split_first(InterpApi.argument_text(view))
        return target

    @staticmethod
    def tell_target(view: InterpView):
        context = view.context
        override = getattr(context, "tell_target", None)
        if override is not None:
            return override

        player_handler = InterpApi._player_handler(view)
        communications = getattr(player_handler, "communications_commands", None)
        if communications is None or not hasattr(communications, "_find_playing_character"):
            return None
        return communications._find_playing_character(InterpApi.tell_target_name(view))

    @staticmethod
    def tell_target_tokens(view: InterpView) -> dict[str, Any]:
        return InterpApi._target_tokens(InterpApi.tell_target(view), fallback_name=InterpApi.tell_target_name(view))

    @staticmethod
    def tell_target_blocks_tells(view: InterpView) -> bool:
        return InterpApi._target_blocks_tells(InterpApi.tell_target(view))

    @staticmethod
    def reply_target_id(view: InterpView):
        return (getattr(view.context.character, "context", {}) or {}).get("reply_to", "")

    @staticmethod
    def reply_target(view: InterpView):
        context = view.context
        override = getattr(context, "reply_target", None)
        if override is not None:
            return override

        target_id = InterpApi.reply_target_id(view)
        if not target_id:
            return None

        player_handler = InterpApi._player_handler(view)
        registry = getattr(player_handler, "character_registry", None)
        if registry is None:
            communications = getattr(player_handler, "communications_commands", None)
            registry = getattr(communications, "character_registry", None)
        if registry is None or not hasattr(registry, "get_or_none"):
            return None
        return registry.get_or_none(id=target_id)

    @staticmethod
    def reply_target_tokens(view: InterpView) -> dict[str, Any]:
        return InterpApi._target_tokens(InterpApi.reply_target(view))

    @staticmethod
    def reply_target_blocks_tells(view: InterpView) -> bool:
        return InterpApi._target_blocks_tells(InterpApi.reply_target(view))

    @staticmethod
    def _player_handler(view: InterpView):
        context = getattr(view, "context", None)
        if context is None or not hasattr(context, "player_handler"):
            return None
        return context.player_handler()

    @staticmethod
    def _target_tokens(target, fallback_name: str = "") -> dict[str, Any]:
        name = str(getattr(target, "name", "") or fallback_name or "")
        if not name:
            return {}
        return {"t": name, "v": name}

    @staticmethod
    def _target_blocks_tells(target) -> bool:
        if target is None:
            return False
        comm_flags = CharacterMacros.get_enum("commFlags")
        return any(
            CommunicationsUtil.has_comm(target, comm_flags, flag)
            for flag in ("COMM_DEAF", "COMM_QUIET", "COMM_NOTELL")
        )

    @staticmethod
    def _lambda_locals() -> dict[str, Any]:
        return {
            "InterpApi": InterpApi,
            "CharacterMacros": CharacterMacros,
            "CommunicationsUtil": CommunicationsUtil,
            "GenericUtil": GenericUtil,
            "bool": bool,
            "int": int,
            "max": max,
            "min": min,
        }
