from __future__ import annotations

import random
from functools import lru_cache

from typing import Any
from injector import inject

from area.RoomRegistry import RoomRegistry
from fight.FightHandler import FightHandler
from fight.FightView import FightView
from game.action import ActionCheck, ActionDefinition, ActionPlan, MessageRef
from skill.SkillApi import SkillApi
from skill.SkillRegistry import SkillRegistry
from player.CharacterMacros import CharacterMacros
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

    def run_action(self, commands_handler, character, context, action_name: str):
        view = self.build_fight_view(character, context, action_name)
        definition = self._fight_action_definition(view, action_name)
        plan = self.evaluate_fight_action(view, definition)
        context.finish()
        return self.execute_fight_plan(context, commands_handler, view, plan)

    def build_fight_view(self, context) -> FightView:
        character = context.character
        command_name = context.command.name
        room = context.room if context.room is not None else self.room_registry.get_or_none(id=character.room_id)
        argument = FightUtil.parse_action_argument(context.result, context.parameters)
        victim = PlayerUtil.get_target(character, argument, room) if room is not None and argument else None
        weapon = getattr(getattr(character, "equipped", None), "wielded", None)
        skill = self._resolve_action_skill(command_name, weapon)
        skill_percent = self.skill_api.get_rating(character, skill) if skill is not None else 0
        has_skill_access = True if skill is None else self._has_skill_access(character, skill)
        return FightView(
            actor=character,
            command=context.command,
            room=room,
            argument=argument,
            victim=victim,
            spell=None,
            skill=skill,
            extra={
                "command_name": command_name,
                "weapon": weapon,
                "skill_percent": skill_percent,
                "has_skill_access": has_skill_access,
            },
        )

    @staticmethod
    def evaluate_fight_action(view: FightView, definition: ActionDefinition[FightView]) -> ActionPlan:
        for check in definition.checks:
            if check.predicate(view):
                return ActionPlan(
                    stop=True,
                    messages=(
                        MessageRef(
                            channel="to_char",
                            key=check.message_key,
                            fallback=view.safe_message or check.fallback,
                            tokens=check.token_factory(view),
                        ),
                    ),
                )
        return definition.plan_factory(view)

    def execute_fight_plan(self, context, fight_commands, view: FightView, plan: ActionPlan):
        if not plan.operation:
            return self.render_plan_payload(
                view.context.command.payload,
                plan,
                victim=view.victim,
                targets=context.room.player_targets(context.character),
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
            if not CharacterMacros.is_awake(victim) and skill_percent >= 2:
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
            payload[msg.channel] = text
        if "to_victim" in payload and victim is not None:
            payload["victim"] = victim
        if "to_room" in payload and targets is not None:
            payload["targets"] = list(targets)
        return payload

    def _fight_action_definition(self, view: FightView, action_name: str) -> ActionDefinition[FightView]:
        skill = view.skill
        command_name = str(view.extra.get("command_name", "") or action_name).strip().lower()
        if skill is None:
            raise KeyError(f"No fight action definition for '{command_name}'")

        executor = str(getattr(skill, "fight_executor", "") or "").strip().lower()
        if not executor:
            raise KeyError(f"Skill '{getattr(skill, 'name', command_name)}' does not define a fight executor")

        plan_data = dict(getattr(skill, "fight_plan", {}) or {})
        return ActionDefinition(
            name=str(getattr(skill, "name", "") or command_name),
            checks=self._build_checks(skill),
            plan_factory=lambda _view: ActionPlan(operation=executor, data=dict(plan_data)),
        )

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
    def _kill_steal_blocked(view: FightView) -> bool:
        victim = view.victim
        if victim is None:
            return False
        current = getattr(victim, "fighting", None)
        return CharacterMacros.is_npc(victim) and current is not None and current is not view.actor

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
        weapon_class = CharacterMacros.get_enum("weaponClass")
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

    def _build_checks(self, skill) -> tuple[ActionCheck[FightView], ...]:
        checks: list[ActionCheck[FightView]] = []
        for entry in list(getattr(skill, "checks", []) or []):
            predicate_src = str(entry.get("predicate", "") or "").strip()
            if not predicate_src:
                continue
            token_factory_src = str(entry.get("token_factory", "") or "").strip()
            checks.append(
                ActionCheck(
                    predicate=self._compile_lambda(predicate_src),
                    message_key=str(entry.get("message_key", "") or "").strip(),
                    fallback=str(entry.get("fallback", "") or ""),
                    token_factory=self._compile_lambda(token_factory_src) if token_factory_src else self._empty_tokens,
                )
            )
        return tuple(checks)

    @staticmethod
    def _empty_tokens(_view: FightView) -> dict[str, Any]:
        return {}

    @staticmethod
    @lru_cache(maxsize=256)
    def _compile_lambda(source: str):
        text = str(source or "").strip()
        if not text:
            return FightApi._empty_tokens
        globals_dict = {"__builtins__": {}}
        globals_dict.update(FightApi._lambda_locals())
        func = eval(text, globals_dict, {})
        if not callable(func):
            raise TypeError(f"Fight check lambda must be callable: {text}")
        return func

    @staticmethod
    def _lambda_locals() -> dict[str, Any]:
        return {
            "FightApi": FightApi,
            "CharacterMacros": CharacterMacros,
            "GenericUtil": GenericUtil,
            "kill_steal_blocked": FightApi._kill_steal_blocked,
            "is_weapon_wielded": FightApi._is_weapon_wielded,
            "target_too_hurt": FightApi._target_too_hurt,
            "victim_name_tokens": FightApi._token_victim_name,
            "bool": bool,
            "int": int,
            "max": max,
            "min": min,
        }

    def _has_skill_access(self, character, skill) -> bool:
        if CharacterMacros.is_npc(character):
            return True
        if skill is None:
            return False
        if GenericUtil.to_int(getattr(character, "level", 0), 0) < FightUtil.level_for_class(skill, character):
            return False
        return self.skill_api.get_rating(character, skill) > 0
