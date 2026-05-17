from __future__ import annotations

import random
from functools import lru_cache

from typing import Any
from injector import inject

from area.RoomRegistry import RoomRegistry
from fight.FightHandler import FightHandler
from fight.FightView import FightView
from game.action import ActionGuard, ActionDefinition, ActionPlan, MessageRef
from api.SkillApi import SkillApi
from skill.SkillRegistry import SkillRegistry
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from util.GenericUtil import GenericUtil
from util.FightUtil import FightUtil
from util.PlayerUtil import PlayerUtil


class FightApi:
    @inject
    def __init__(self, room_registry: RoomRegistry, skill_registry: SkillRegistry, skill_api: SkillApi, fight_handler: FightHandler):
        self.__name__ = "FightApi"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.room_registry = room_registry
        self.skill_registry = skill_registry
        self.skill_api = skill_api
        self.fight_handler = fight_handler

    def run_action(self, commands_handler, context):
        action_name = context.command.name
        view = self.build_fight_view(context)
        definition = self._fight_action_definition(view, action_name, require_executor=True)
        plan = self.evaluate_fight_action(view, definition)
        context.finish()
        return self.execute_fight_plan(context, commands_handler, view, plan)

    def evaluate_guards_only(self, context, *, skill_name: str | None = None, current_target_fallback: bool = False):
        view = self.build_fight_view(context, skill_name=skill_name, current_target_fallback=current_target_fallback)
        return self.evaluate_guards_only_view(view)

    def evaluate_guards_only_view(self, view: FightView):
        action_name = str(view.extra.get("command_name", "") or getattr(getattr(view, "command", None), "name", "") or "")
        definition = self._fight_action_definition(view, action_name, require_executor=False)
        plan = self.evaluate_fight_action(view, definition)
        if not plan.stop or not plan.messages:
            return None
        view.context.finish()
        room = view.room
        payload = self.render_plan_payload(
            view.context.command.payload,
            plan,
            victim=view.victim,
            targets=room.player_targets(view.actor) if room is not None else [],
        )
        payload["blocked"] = True
        payload["blocked_key"] = plan.messages[0].key
        return payload

    def build_fight_view(self, context, *, skill_name: str | None = None, current_target_fallback: bool = False) -> FightView:
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=context.character.room_id)
        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        victim = PlayerUtil.get_target(context.character, argument, room) if room is not None and argument else None
        if victim is None and current_target_fallback and not argument:
            victim = getattr(context.character, "fighting", None)
        weapon = getattr(getattr(context.character, "equipped", None), "wielded", None)
        skill = self.skill_registry.get_or_none(name=skill_name) if skill_name else self._resolve_action_skill(context.command.name, weapon)
        skill_percent = self.skill_api.get_rating(context.character, skill) if skill is not None else 0
        has_skill_access = True if skill is None else self._has_skill_access(context.character, skill)
        safe = False
        safe_message = ""
        if room is not None and victim is not None and victim is not context.character:
            safe, safe_message = self.fight_handler.is_safe(context.character, victim, room=room)
        return FightView(
            context=context,
            payload=context.command.payload,
            victim=victim,
            spell=None,
            skill=skill,
            extra={
                "command_name": context.command.name,
                "room": room,
                "argument": argument,
                "weapon": weapon,
                "skill_percent": skill_percent,
                "has_skill_access": has_skill_access,
                "safe": safe,
                "safe_message": safe_message,
            },
        )

    @staticmethod
    def evaluate_fight_action(view: FightView, definition: ActionDefinition[FightView]) -> ActionPlan:
        for guard in definition.guards:
            if guard.predicate(view):
                return ActionPlan(
                    stop=True,
                    messages=(
                        MessageRef(
                            channel="to_char",
                            key=guard.message_key,
                            fallback=view.safe_message or guard.fallback,
                            tokens=guard.token_factory(view),
                        ),
                    ),
                )
        return definition.plan_factory(view)

    def execute_fight_plan(self, context, fight_commands, view: FightView, plan: ActionPlan):
        if not plan.operation:
            room = view.room
            return self.render_plan_payload(
                view.context.command.payload,
                plan,
                victim=view.victim,
                targets=room.player_targets(context.character) if room is not None else [],
            )

        if plan.operation == "multi_hit":
            victim = view.victim
            room = view.room
            if getattr(view.actor, "fighting", None) is None:
                self.fight_handler.set_fighting(view.actor, victim, room.id)
            if getattr(victim, "fighting", None) is None:
                self.fight_handler.set_fighting(victim, view.actor, room.id)
            pre_corpse_ids = fight_commands._pre_corpse_ids(room)
            result = self.fight_handler.multi_hit(view.actor, victim, dt=plan.data.get("dt", "TYPE_UNDEFINED"))
            return self.fight_handler.build_round_payload(view.actor, victim, room, result, pre_corpse_ids)

        if plan.operation == "backstab":
            victim = view.victim
            room = view.room
            skill = view.skill
            fight_commands._set_wait(view.actor, fight_commands._skill_beats(skill, 12))
            pre_corpse_ids = fight_commands._pre_corpse_ids(room)
            skill_percent = max(1, GenericUtil.to_int(view.extra.get("skill_percent", 0), 0))
            success = random.randint(1, 100) <= skill_percent
            if not CharacterApi.is_awake(victim) and skill_percent >= 2:
                success = True

            if success:
                fight_commands._check_improve(view.actor, skill, True, 1)
                result = self.fight_handler.multi_hit(view.actor, victim, dt=plan.data.get("dt", "backstab"))
            else:
                fight_commands._check_improve(view.actor, skill, False, 1)
                result = self.fight_handler.damage(view.actor, victim, 0, dt=plan.data.get("dt", "backstab"))
            return self.fight_handler.build_round_payload(view.actor, victim, room, result, pre_corpse_ids)

        raise ValueError(f"Unknown fight executor: {plan.operation}")

    @staticmethod
    def render_plan_payload(payload_def, plan: ActionPlan, victim=None, targets=None) -> dict:
        payload: dict[str, Any] = {}
        for msg in plan.messages:
            text = payload_def.render(msg.channel, msg.key, msg.fallback, **msg.tokens)
            if not text:
                continue
            payload[msg.channel] = FightApi._ensure_message_break(text)
        if "to_victim" in payload and victim is not None:
            payload["victim"] = victim
        if "to_room" in payload and targets is not None:
            payload["targets"] = list(targets)
        return payload

    def _fight_action_definition(self, view: FightView, action_name: str, *, require_executor: bool) -> ActionDefinition[FightView]:
        skill = view.skill
        command_name = str(view.extra.get("command_name", "") or action_name).strip().lower()
        if skill is None:
            raise KeyError(f"No fight action definition for '{command_name}'")

        executor = str(getattr(skill, "fight_executor", "") or "").strip().lower()
        if require_executor and not executor:
            raise KeyError(f"Skill '{getattr(skill, 'name', command_name)}' does not define a fight executor")

        plan_data = dict(getattr(skill, "fight_plan", {}) or {})
        return ActionDefinition(
            name=str(getattr(skill, "name", "") or command_name),
            guards=self._build_checks(skill),
            plan_factory=(lambda _view: ActionPlan(operation=executor, data=dict(plan_data)))
            if executor else (lambda _view: ActionPlan(stop=False, data={"blocked": False})),
        )

    @staticmethod
    def _ensure_message_break(text: str) -> str:
        rendered = str(text or "")
        if rendered and not rendered.endswith("\r\n"):
            rendered += "\r\n"
        return rendered

    @staticmethod
    def _token_victim_name(view: FightView) -> dict[str, Any]:
        victim_name = ""
        if view.victim is not None:
            victim_name = str(getattr(view.victim, "name", "") or "")
        return {"victim_name": victim_name}

    @staticmethod
    def _is_weapon_wielded(view: FightView) -> bool:
        weapon = view.extra.get("weapon")
        return weapon is not None and str(getattr(weapon, "item_type", "") or "").strip().lower() == "weapon"

    @staticmethod
    def _target_too_hurt(view: FightView) -> bool:
        victim = view.victim
        if victim is None:
            return False
        return GenericUtil.to_int(getattr(victim, "hit", 0), 0) < max(1, GenericUtil.to_int(getattr(victim, "max_hit", 0), 0) // 3)

    @staticmethod
    def _has_affect(entity, affect_name: str) -> bool:
        if entity is None:
            return False
        return CharacterApi.is_affected_by_name(entity, CharacterApi.get_enum("affectedBy"), affect_name)

    @staticmethod
    def _has_effect_type(entity, effect_type: str) -> bool:
        wanted = str(effect_type or "").strip().lower()
        if not wanted or entity is None:
            return False
        for effect in list(getattr(entity, "effects", []) or []):
            if str(getattr(effect, "type", "") or "").strip().lower() == wanted:
                return True
        return False

    @staticmethod
    def _position_below(entity, pos_name: str) -> bool:
        if entity is None:
            return False
        return CharacterApi.position_value(entity) < CharacterApi.pos_value(pos_name)

    @staticmethod
    def _kill_steal_blocked(view: FightView) -> bool:
        victim = view.victim
        if victim is None:
            return False
        current = getattr(victim, "fighting", None)
        return CharacterApi.is_npc(victim) and current is not None and current is not view.actor

    def _resolve_action_skill(self, command_name: str, weapon) -> Any:
        if command_name in {"kill", "hit"}:
            skill_name = self._active_melee_skill_name(weapon)
            return self.skill_registry.get_or_none(name=skill_name)
        return self.skill_registry.get_or_none(name=command_name)

    def _active_melee_skill_name(self, weapon) -> str:
        if weapon is None:
            return "hand to hand"

        raw = getattr(weapon, "value0", None)
        token = str(raw or "").strip()
        weapon_class = CharacterApi.get_enum("weaponClass")
        numeric = GenericUtil.to_int(raw, None)
        if numeric is not None:
            for enum_name, skill_name in self.fight_handler.WeaponClass.__members__.items():
                member = getattr(weapon_class, enum_name, None)
                if member is not None and int(member.value) == numeric:
                    return skill_name
        upper_token = token.upper()
        if self.fight_handler.WeaponClass.__contains__(upper_token):
            return self.fight_handler.WeaponClass[upper_token]

        lowered = token.lower()
        if lowered in self.fight_handler.WeaponClass.__members__.values():
            return lowered
        return "hand to hand"

    def _build_checks(self, skill) -> tuple[ActionGuard[FightView], ...]:
        guards: list[ActionGuard[FightView]] = []
        for entry in list(getattr(skill, "guards", []) or []):
            predicate_src = str(entry.get("predicate", "") or "").strip()
            if not predicate_src:
                continue
            token_factory_src = str(entry.get("token_factory", "") or "").strip()
            guards.append(
                ActionGuard(
                    predicate=self._compile_lambda(predicate_src),
                    message_key=str(entry.get("message_key", "") or "").strip(),
                    fallback=str(entry.get("fallback", "") or ""),
                    token_factory=self._compile_lambda(token_factory_src) if token_factory_src else self._empty_tokens,
                )
            )
        return tuple(guards)

    @staticmethod
    def _empty_tokens(_view: FightView) -> dict[str, Any]:
        return {}

    @staticmethod
    @lru_cache(maxsize=256)
    def _compile_lambda(source: str):
        text = FightApi._normalize_view_expression(source)
        if not text:
            return FightApi._empty_tokens
        globals_dict = {"__builtins__": {}}
        globals_dict.update(FightApi._lambda_locals())
        func = eval(text, globals_dict, {})
        if not callable(func):
            raise TypeError(f"Fight check lambda must be callable: {text}")
        return func

    @staticmethod
    def _normalize_view_expression(source: str) -> str:
        text = str(source or "").strip()
        replacements = {
            "v.context.current_fighting": "v.current_fighting",
            "v.context.argument": "v.argument",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    @staticmethod
    def _lambda_locals() -> dict[str, Any]:
        return {
            "FightApi": FightApi,
            "CharacterApi": CharacterApi,
            "GenericUtil": GenericUtil,
            "kill_steal_blocked": FightApi._kill_steal_blocked,
            "is_weapon_wielded": FightApi._is_weapon_wielded,
            "target_too_hurt": FightApi._target_too_hurt,
            "has_affect": FightApi._has_affect,
            "has_effect_type": FightApi._has_effect_type,
            "position_below": FightApi._position_below,
            "victim_name_tokens": FightApi._token_victim_name,
            "bool": bool,
            "int": int,
            "getattr": getattr,
            "max": max,
            "min": min,
        }

    def _has_skill_access(self, character, skill) -> bool:
        if CharacterApi.is_npc(character):
            return True
        if skill is None:
            return False
        if GenericUtil.to_int(getattr(character, "level", 0), 0) < FightUtil.level_for_class(skill, character):
            return False
        return self.skill_api.get_rating(character, skill) > 0
