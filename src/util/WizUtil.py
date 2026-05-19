from __future__ import annotations

import re
from typing import Any

from api.CharacterApi import CharacterApi
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil


class WizUtil:
    @staticmethod
    def argument_text(raw_result: Any, parameters: list[str] | None) -> str:
        if isinstance(raw_result, str) and raw_result.strip():
            return raw_result.strip()
        return " ".join(parameters or []).strip()

    @staticmethod
    def split_argument(argument: str) -> tuple[str, str]:
        arg, rest = InterpUtil.one_argument(argument or "")
        return arg, rest.strip()

    @staticmethod
    def name_matches(query: str, candidate: str) -> bool:
        q = (query or "").strip().lower()
        c = (candidate or "").strip().lower()
        if not q or not c:
            return False
        return c == q or c.startswith(q)

    @staticmethod
    def room_of_entity(room_registry, entity):
        if room_registry is None or entity is None:
            return None
        return room_registry.get_or_none(id=getattr(entity, "room_id", ""))

    @staticmethod
    def move_entity(room_registry, entity, to_room):
        if room_registry is None or entity is None or to_room is None:
            return None
        from_room = WizUtil.room_of_entity(room_registry, entity)
        if from_room is not None:
            if CharacterApi.is_npc(entity):
                from_room.remove_mobile_from_room(entity)
            else:
                from_room.remove_player_from_room(entity)
        if CharacterApi.is_npc(entity):
            to_room.add_mobile_to_room(entity)
        else:
            to_room.add_player_to_room(entity)
        entity.room_id = to_room.id
        entity.area_id = to_room.area_id
        return from_room

    @staticmethod
    def room_targets(room, actor) -> list:
        if room is None:
            return []
        return room.player_targets(actor) if not CharacterApi.is_npc(actor) else room.players_in_room()

    @staticmethod
    def display_name(entity) -> str:
        if entity is None:
            return ""
        if CharacterApi.is_npc(entity):
            return str(getattr(entity, "short_description", "") or getattr(entity, "name", "") or "")
        return str(getattr(entity, "name", "") or "")

    @staticmethod
    def find_world_entity(character_registry, room_registry, query: str, *, include_players: bool = True, include_mobiles: bool = True):
        wanted = (query or "").strip().lower()
        if not wanted:
            return None
        if include_players and character_registry is not None:
            for character in character_registry.all_characters():
                if WizUtil.name_matches(wanted, getattr(character, "name", "")):
                    return character
        if include_mobiles and room_registry is not None:
            for room in room_registry.all_rooms():
                if room is None:
                    continue
                for mobile in room.mobiles.values():
                    names = [
                        str(getattr(mobile, "name", "") or ""),
                        str(getattr(mobile, "short_description", "") or ""),
                    ]
                    if any(WizUtil.name_matches(wanted, name) for name in names):
                        return mobile
        return None

    @staticmethod
    def find_world_item(character_registry, room_registry, query: str):
        wanted = (query or "").strip().lower()
        if not wanted:
            return None
        if character_registry is not None:
            for character in character_registry.all_characters():
                for item in list(getattr(character, "loot", []) or []):
                    if WizUtil.name_matches(wanted, getattr(item, "name", "")):
                        return item
                    found = WizUtil._find_nested_item(item, wanted)
                    if found is not None:
                        return found
        if room_registry is not None:
            for room in room_registry.all_rooms():
                for item in room.contents.values():
                    if WizUtil.name_matches(wanted, getattr(item, "name", "")):
                        return item
                    found = WizUtil._find_nested_item(item, wanted)
                    if found is not None:
                        return found
        return None

    @staticmethod
    def _find_nested_item(item, wanted: str):
        for child in list(getattr(item, "contains", []) or []):
            if WizUtil.name_matches(wanted, getattr(child, "name", "")):
                return child
            found = WizUtil._find_nested_item(child, wanted)
            if found is not None:
                return found
        return None

    @staticmethod
    def count_extra_descriptions(obj) -> int:
        if obj is None:
            return 0
        count = 1 if getattr(obj, "extra_description", None) else 0
        for item in list(getattr(obj, "contains", []) or []):
            count += WizUtil.count_extra_descriptions(item)
        return count

    @staticmethod
    def count_active_effects(registry_service) -> int:
        count = 0
        for character in list(registry_service.character_registry.all_characters() or []):
            count += len(list(getattr(character, "effects", []) or []))
        for room in list(registry_service.room_registry.all_rooms() or []):
            for mobile in list(getattr(room, "mobiles", {}).values()):
                count += len(list(getattr(mobile, "effects", []) or []))
            for item in list(getattr(room, "contents", {}).values()):
                count += len(list(getattr(item, "effects", []) or []))
        return count

    @staticmethod
    def personalize_smote(text: str, viewer_name: str) -> str:
        if not text or not viewer_name:
            return text
        pattern = re.compile(re.escape(viewer_name), re.IGNORECASE)
        match = pattern.search(text)
        if match is None:
            return text

        start, end = match.span()
        rewritten = text[:start] + "you"
        idx = end
        if idx < len(text) and text[idx:idx + 2] == "'s":
            rewritten += "r"
            idx += 2
        elif idx < len(text) and text[idx] == "s":
            idx += 1
        rewritten += text[idx:]
        return rewritten

    @staticmethod
    def can_clone_object(actor, obj) -> bool:
        game_parameters = CharacterApi.get_enum("gameParameters")
        trust = CharacterApi.get_trust(actor)
        level = GenericUtil.to_int(getattr(obj, "level", 0), 0)
        cost = GenericUtil.to_int(getattr(obj, "cost", 0), 0)
        return (
            trust >= game_parameters.GOD.value
            or (trust >= game_parameters.IMMORTAL.value and level <= 20 and cost <= 1000)
            or (trust >= game_parameters.DEMI.value and level <= 10 and cost <= 500)
            or (trust >= game_parameters.ANGEL.value and level <= 5 and cost <= 250)
            or (trust >= game_parameters.AVATAR.value and level == 0 and cost <= 100)
        )

    @staticmethod
    def can_clone_mobile(actor, mob) -> bool:
        game_parameters = CharacterApi.get_enum("gameParameters")
        trust = CharacterApi.get_trust(actor)
        level = GenericUtil.to_int(getattr(mob, "level", 0), 0)
        return (
            trust >= game_parameters.GOD.value
            or (trust >= game_parameters.IMMORTAL.value and level <= 20)
            or (trust >= game_parameters.DEMI.value and level <= 10)
            or (trust >= game_parameters.ANGEL.value and level <= 5)
            or (trust >= game_parameters.AVATAR.value and level <= 0)
        )
