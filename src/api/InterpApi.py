from __future__ import annotations

from dataclasses import fields
from functools import lru_cache
from typing import Any, Callable
from injector import inject

from game.action import ActionGuard, ActionDefinition, ActionPlan, MessageRef
from interp.InterpView import InterpView
from api.CommunicationsApi import CommunicationsApi
from api.MovementApi import MovementApi
from api.ItemApi import ItemApi
from api.WizApi import WizApi
from api.CharacterApi import CharacterApi
from game.GamePayload import GamePayload
from server.LoggerFactory import LoggerFactory
from util.AreaUtil import AreaUtil
from util.CommunicationsUtil import CommunicationsUtil
from util.FightUtil import FightUtil
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil
from util.ItemUtil import ItemUtil
from util.MovementUtil import MovementUtil
from util.WizUtil import WizUtil
from item.Item import Item


class InterpApi:
    @inject
    def __init__(self):
        self.__name__ = "InterpApi"
        self.logger = LoggerFactory.get_logger(self.__name__)

    def run_action(self, context, action_name: str) -> dict[str, Any] | None:
        view = self.build_interp_view(context)
        definition = self._interp_action_definition(view, action_name)
        plan = self.evaluate_interp_action(view, definition)
        context.finish()
        return self.execute_interp_plan(view, plan)

    def evaluate_guards_only(self, context, action_name: str):
        view = self.build_interp_view(context)
        definition = self._interp_check_definition(view, action_name)
        plan = self.evaluate_interp_action(view, definition)
        if not bool((plan.data or {}).get("blocked")):
            return None
        context.finish()
        payload = self.render_plan_payload(view.payload, plan)
        payload.update(dict(plan.data or {}))
        if plan.messages:
            payload["blocked_key"] = plan.messages[0].key
        return payload

    @staticmethod
    def build_interp_view(context) -> InterpView:
        payload = getattr(getattr(context, "command", None), "payload", None)
        return InterpView(context=context, payload=GamePayload.from_json(payload))

    @staticmethod
    def evaluate_interp_action(view: InterpView, definition: ActionDefinition[InterpView]) -> ActionPlan:
        for index, guard in enumerate(definition.guards):
            print(f"Checking guard #{index+1} of {len(definition.guards)}; predicate: {view.context.command.guards[index]}")
            if guard.predicate(view):
                tokens = InterpApi._default_tokens(view)
                tokens.update(dict(guard.token_factory(view) or {}))
                return ActionPlan(
                    stop=True,
                    messages=tuple(InterpApi._message_refs_for_key(view.payload, guard.message_key, tokens=tokens, fallback=guard.fallback, channel=guard.channel)),
                    data={"blocked": True},
                )
        return definition.plan_factory(view)

    def execute_interp_plan(self, view: InterpView, plan: ActionPlan) -> dict[str, Any] | None:
        payload = self.render_plan_payload(view.payload, plan)
        payload.update(dict(plan.data or {}))
        return payload

    def render_plan_payload(self, payload_def: GamePayload, plan: ActionPlan) -> dict:
        payload: dict[str, Any] = {}
        for msg in plan.messages:
            text = payload_def.render(msg.channel, msg.key, msg.fallback, **msg.tokens)
            if not text:
                continue
            payload[msg.channel] = CommunicationsUtil.ensure_message_break(text)
        self.logger.debug(f"Rendered plan payload: {payload}")
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

    def _build_guards(self, command) -> tuple[ActionGuard[InterpView], ...]:
        guards: list[ActionGuard[InterpView]] = []
        for entry in list(getattr(command, "guards", []) or []):
            predicate_src = str(entry.get("predicate", "") or "").strip()
            if not predicate_src:
                continue
            token_factory_src = str(entry.get("token_factory", "") or "").strip()
            guards.append(
                ActionGuard(
                    predicate=self._compile_lambda(predicate_src),
                    channel=str(entry.get("channel", "") or "").strip(),
                    message_key=str(entry.get("message_key", "") or "").strip(),
                    fallback=str(entry.get("fallback", "") or ""),
                    token_factory=self._compile_lambda(token_factory_src) if token_factory_src else self._empty_tokens,
                )
            )
        return tuple(guards)

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
        argument = InterpUtil.argument_text(view)
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

        globals_dict = InterpApi._lambda_locals()
        func = eval(text, globals_dict)
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
            "InterpApi.tell_target(": "CommunicationsApi.tell_target(",
            "InterpApi.tell_target_tokens(": "CommunicationsApi.tell_target_tokens(",
            "InterpApi.tell_target_blocks_tells(": "CommunicationsApi.tell_target_blocks_tells(",
            "InterpApi.reply_target(": "CommunicationsApi.reply_target(",
            "InterpApi.reply_target_tokens(": "CommunicationsApi.reply_target_tokens(",
            "InterpApi.reply_target_blocks_tells(": "CommunicationsApi.reply_target_blocks_tells(",
            "not (v.context.character.context or {}).get('tell_buffer', [])": "not CommunicationsApi.has_buffered_tells(v.context.character)",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def _interp_action_definition(self, view: InterpView, action_name: str) -> ActionDefinition[InterpView]:
        command = view.context.command
        command_name = str(getattr(command, "name", "") or action_name).strip().lower()
        if command is None:
            raise KeyError(f"No interp action definition for '{command_name}'")

        return ActionDefinition(
            name=str(getattr(command, "name", "") or command_name),
            guards=self._build_guards(command),
            plan_factory=self._default_plan,
        )

    def _interp_check_definition(self, view: InterpView, action_name: str) -> ActionDefinition[InterpView]:
        command = view.context.command
        command_name = str(getattr(command, "name", "") or action_name).strip().lower()
        if command is None:
            raise KeyError(f"No interp action definition for '{command_name}'")

        return ActionDefinition(
            name=str(getattr(command, "name", "") or command_name),
            guards=self._build_guards(command),
            plan_factory=lambda _view: ActionPlan(stop=False, data={"blocked": False}),
        )

    @staticmethod
    def _lambda_locals() -> dict[str, Any]:
        return {
            "__builtins__": __builtins__,
            "InterpApi": InterpApi,
            "CharacterApi": CharacterApi,
            "CommunicationsUtil": CommunicationsUtil,
            "GenericUtil": GenericUtil,
            "MovementUtil": MovementUtil,
            "InterpUtil": InterpUtil,
            "FightUtil": FightUtil,
            "MovementApi": MovementApi,
            "CommunicationsApi": CommunicationsApi,
            "ItemApi": ItemApi,
            "Item": Item,
            "ItemUtil": ItemUtil,
            "AreaUtil": AreaUtil,
            "WizApi": WizApi,
            "WizUtil": WizUtil,
            "bool": bool,
            "int": int,
            "getattr": getattr,
            "max": max,
            "min": min,
            "len": len
        }
