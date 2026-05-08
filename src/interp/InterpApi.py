from __future__ import annotations

from dataclasses import fields
from functools import lru_cache
from typing import Any
from injector import inject

from game.action import ActionCheck, ActionDefinition, ActionPlan, MessageRef
from interp.InterpView import InterpView
from game.GamePayload import GamePayload
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil


class InterpApi:
    @inject
    def __init__(self):
        self.__name__ = "InterpApi"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def run_action(self, context, action_name: str):
        view = self.build_interp_view(context)
        definition = self._interp_action_definition(view, action_name)
        plan = self.evaluate_interp_action(view, definition)
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
                return ActionPlan(
                    stop=True,
                    messages=(
                        MessageRef(
                            channel=check.channel,
                            key=check.message_key,
                            fallback=check.fallback,
                            tokens=check.token_factory(view),
                        ),
                    ),
                    data={"blocked": True},
                )
        return definition.plan_factory(view)

    def execute_interp_plan(self, view: InterpView, plan: ActionPlan):
        payload = self.render_plan_payload(view.payload, plan)
        payload.update(dict(plan.data or {}))
        return payload

    def render_plan_payload(self, payload_def, plan: ActionPlan) -> dict:
        payload: dict[str, Any] = {}
        for msg in plan.messages:
            text = payload_def.render(msg.channel, msg.key, msg.fallback, **msg.tokens)
            if not text:
                continue
            payload[msg.channel] = InterpApi._ensure_message_break(text)
        self.logger.debug(f"Plan payload: {payload}")
        return payload

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
                    channel=str(entry.get("channel", "to_char") or "to_char").strip(),
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
    def _default_tokens(view: InterpView) -> dict[str, Any]:
        actor = getattr(view.context, "character", None)
        return {"c": str(getattr(actor, "name", "") or "")}

    @staticmethod
    def _empty_tokens(_view: InterpView) -> dict[str, Any]:
        return {}

    @staticmethod
    @lru_cache(maxsize=256)
    def _compile_lambda(source: str):
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
    def _lambda_locals() -> dict[str, Any]:
        return {
            "InterpApi": InterpApi,
            "CharacterMacros": CharacterMacros,
            "GenericUtil": GenericUtil,
            "bool": bool,
            "int": int,
            "max": max,
            "min": min,
        }
