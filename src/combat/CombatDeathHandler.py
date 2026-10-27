from __future__ import annotations

import random

from injector import inject
from api.CharacterApi import CharacterApi
from api.ItemApi import ItemApi
from game.GameData import GameData
from game.GamePayload import GamePayload
from game.RegistryService import RegistryService
from interp.Context import Context
from interp.commands.Object import Object
from player.CharacterAdvancement import CharacterAdvancement
from util.CommunicationsUtil import CommunicationsUtil
from util.GenericUtil import GenericUtil


class CombatDeathHandler:
    """Death consequences and content-owned notices shared by combat callers."""

    @inject
    def __init__(self, game_data: GameData, registry_service: RegistryService, object_commands: Object):
        self.payload = GamePayload.from_json(game_data.death_rules.get("payload", {}))
        self.registry = registry_service
        self.object_commands = object_commands

    def text(self, channel, key, **tokens):
        key = next(iter(GenericUtil.camel_to_snake_case({key: ""})))
        return CommunicationsUtil.ensure_message_break(self.payload.render(channel, key, **tokens))

    def room_notice(self, room, key, victim, **tokens):
        return {"to_room": self.text("to_room", key, victim=str(getattr(victim, "short_description", "") or victim.name), **tokens),
                "targets": room.player_targets(victim)}

    def item_transfer(self, item, floating, victim, room, flags):
        notices = []
        item.extra_flags = ItemApi.flags_to_int(getattr(item, "extra_flags", 0))
        has = lambda name: ItemApi.has_item_flag(item, flags, name)
        if has("ITEM_ROT_DEATH") and not floating:
            item.timer = random.randint(5, 10)
            item.extra_flags = CharacterApi.unset_bit(item.extra_flags, CharacterApi.enum_bit(flags, "ITEM_ROT_DEATH"))
        item.extra_flags = CharacterApi.unset_bit(getattr(item, "extra_flags", 0), CharacterApi.enum_bit(flags, "ITEM_VIS_DEATH"))
        if has("ITEM_INVENTORY"):
            self.discard(item)
            return False, notices
        if floating:
            if has("ITEM_ROT_DEATH"):
                contents = list(getattr(item, "contains", []) or [])
                notices.append(self.room_notice(room, "evaporatesContents" if contents else "evaporates", victim,
                                                item=str(getattr(item, "short_description", "") or item.name)))
                item.contains = []
                for child in contents:
                    room.add_item_to_room(child)
                self.discard(item)
                return False, notices
            notices.append(self.room_notice(room, "falls", victim, item=str(getattr(item, "short_description", "") or item.name)))
        return True, notices

    def wounds(self, attacker, victim, room, damage, position):
        result = []
        key = {"POS_MORTAL": "mortal", "POS_INCAP": "incap", "POS_STUNNED": "stunned", "POS_DEAD": "dead"}.get(position)
        if key:
            result.append(self.room_notice(room, key, victim))
            if not CharacterApi.is_npc(victim):
                result.append({"victim": victim, "to_victim": self.text("to_victim", key)})
        elif not CharacterApi.is_npc(victim):
            if damage > victim.max_hit // 4:
                result.append({"victim": victim, "to_victim": self.text("to_victim", "hurt")})
            if victim.hit < victim.max_hit // 4:
                result.append({"victim": victim, "to_victim": self.text("to_victim", "bleeding")})
        return result

    def penalty(self, attacker, victim, room):
        if not CharacterApi.is_npc(victim):
            attrs = victim.character_attributes
            total_xp = GenericUtil.to_int(attrs.accumulated_experience, 0)
            level_floor = GenericUtil.to_int(attrs.experience_per_level, 0) * GenericUtil.to_int(victim.level, 0)
            if total_xp > level_floor:
                CharacterAdvancement.gain_experience(
                    victim, GenericUtil.trunc_div(2 * (level_floor - total_xp), 3) + 50)
        victim_name = str(getattr(victim, "short_description", "") or victim.name)
        killer = str(getattr(attacker, "short_description", "") or attacker.name)
        return {"to_wiznet": self.text("to_wiznet", "death", victim=victim_name, killer=killer,
                                      room=getattr(room, "name", ""), vnum=getattr(room, "vnum", "")),
                "wiznet_actor": None, "wiznet_flag": "WIZ_MOBDEATHS" if CharacterApi.is_npc(victim) else "WIZ_DEATHS"}

    def cry(self, victim, room, roll, parts, body_parts):
        key = "cry"
        mapping = {2: ("PART_GUTS", "guts"), 3: ("PART_HEAD", "head"), 4: ("PART_HEART", "heart"),
                   5: ("PART_ARMS", "arm"), 6: ("PART_LEGS", "leg"), 7: ("PART_BRAINS", "brains")}
        if roll == 0:
            key = "ground"
        elif roll == 1:
            key = "blood"
        elif roll in mapping and body_parts.has(parts, body_parts.value(mapping[roll][0])):
            key = mapping[roll][1]
        notices = [self.room_notice(room, key, victim)]
        for exit in list(getattr(room, "exits", []) or []):
            if not 0 <= GenericUtil.to_int(getattr(exit, "direction", 0), 0) <= 5:
                continue
            destination = self.registry.room_registry.get_or_none(id=getattr(exit, "to_room_id", ""))
            if destination is None:
                destination = self.registry.room_registry.get_or_none(vnum=str(getattr(exit, "to_room_vnum", "")))
            if destination is not None and destination is not room:
                notices.append(self.room_notice(destination, "npcCry" if CharacterApi.is_npc(victim) else "playerCry", victim))
        return notices

    def auto_get(self, actor, corpse, room, *, money_only=False):
        command = self.registry.interp_registry.get_or_none(name="get")
        if command is None:
            return []
        context = Context(character=actor, command=command, room=room)
        results = []
        for item in list(corpse.contains):
            if money_only and str(getattr(item, "item_type", "")).lower() != "money":
                continue
            if ItemApi.can_see_object(room, actor, item):
                results.append(self.object_commands._get_one(actor, room, context, item, corpse))
        return results

    def auto_loot(self, combat, actor, victim, room, pre_corpse_ids):
        if CharacterApi.is_npc(actor) or room is None:
            return []
        corpse = combat._find_latest_corpse(room, victim, pre_corpse_ids)
        if corpse is None or "corpse_npc" not in str(getattr(corpse, "item_type", "")).lower() or not ItemApi.can_see_object(room, actor, corpse):
            return []
        results = []
        autoloot = combat._player_act_enabled(actor, "PLR_AUTOLOOT")
        if autoloot:
            results.extend(self.auto_get(actor, corpse, room))
        elif combat._player_act_enabled(actor, "PLR_AUTOGOLD"):
            results.extend(self.auto_get(actor, corpse, room, money_only=True))
        if combat._player_act_enabled(actor, "PLR_AUTOSAC") and not (autoloot and corpse.contains):
            sacrifice = combat._autosacrifice_corpse(actor, corpse, room)
            if sacrifice:
                sacrifice["targets"] = room.player_targets(actor)
                results.append(sacrifice)
        return results

    @staticmethod
    def cleanup_flags(attacker, victim, flags):
        if attacker is victim or CharacterApi.is_npc(attacker) or CharacterApi.is_npc(victim):
            return
        guild = str(getattr(attacker, "guild", "") or "").lower()
        if guild not in {"independent", "loner"} and guild == str(getattr(victim, "guild", "") or "").lower():
            return
        killer = CharacterApi.enum_bit(flags, "PLR_KILLER")
        bit = killer if CharacterApi.is_set(victim.status_flags.act, killer) else CharacterApi.enum_bit(flags, "PLR_THIEF")
        CharacterApi.unset_act_flags(victim, bit)

    @classmethod
    def discard(cls, item):
        # Live objects are owned by containers, not the prototype registry.
        for child in list(getattr(item, "contains", []) or []):
            cls.discard(child)
        item.contains = []
