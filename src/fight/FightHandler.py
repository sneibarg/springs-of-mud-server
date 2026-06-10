import random

from typing import Any, Literal
from injector import inject

from api.GameApi import GameApi
from api.ItemApi import ItemApi
from api.CharacterApi import CharacterApi
from api.MobileApi import MobileApi
from fight.CombatEvent import CombatEvent
from game import GameData
from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from game.RandomNumberGenerator import RandomNumberGenerator
from item.EffectHandler import EffectHandler
from item.BodyForm import BodyForm
from item.BodyParts import BodyParts
from item.Item import Item
from player.Character import Character
from player.CharacterAdvancement import CharacterAdvancement
from skill.Ability import Ability
from server.LoggerFactory import LoggerFactory
from server.messaging.MessageBus import MessageBus
from util.GenericUtil import GenericUtil
from util.InfoUtil import InfoUtil
from util.ItemUtil import ItemUtil
from util.FightUtil import FightUtil
from util.SkillUtil import SkillUtil


class FightHandler:
    @inject
    def __init__(self, message_bus: MessageBus,
                 registry_service: RegistryService,
                 enum_provider: EnumProvider,
                 effect_handler: EffectHandler,
                 game_data: GameData):
        self.__name__ = "FightHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.combat_registry = registry_service.combat_registry
        self.area_registry = registry_service.area_registry
        self.room_registry = registry_service.room_registry
        self.item_registry = registry_service.item_registry
        self.mobile_registry = registry_service.mobile_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.effect_handler = effect_handler
        self.attacks = game_data.attacks
        self.rng = RandomNumberGenerator()
        self.PositionsEnum = enum_provider.get("positions")
        self.WellKnownObjectVnums = enum_provider.get("wellKnownObjectVnums")
        self.OffenseTypes = enum_provider.get("offenseTypes")
        self.AffectBits = enum_provider.get("affectedBy")
        self.ActBits = enum_provider.get("actBits")
        self.RoomFlags = enum_provider.get("roomFlags")
        self.WearFlags = enum_provider.get("wearFlags")
        self.ItemFlags = enum_provider.get("itemFlags")
        self.WeaponClass = enum_provider.get("weaponClass")
        self.WeaponTypes = enum_provider.get("weaponType")
        self.PlayerActBits = enum_provider.get("playerActBits")
        self.MobImmunity = CharacterApi.get_enum("mobImmunity")
        self.MobResistance = CharacterApi.get_enum("mobResistance")
        self.MobVulnerability = CharacterApi.get_enum("mobVulnerability")
        self.mobile_handler = None
        self.logger.info("Initialized FightHandler instance.")

    def set_mobile_handler(self, mobile_handler) -> None:
        self.mobile_handler = mobile_handler

    async def emit_round_payload(self, attacker, payload: dict) -> list:
        prompted: list = []
        if not isinstance(payload, dict):
            return prompted

        if payload.get("to_char") and not CharacterApi.is_npc(attacker):
            await self.message_bus.send_to_character(attacker.id, self.message_bus.text_to_message(payload["to_char"]))
            prompted.append(attacker)
        if payload.get("to_victim") and payload.get("victim") is not None and not CharacterApi.is_npc(
                payload["victim"]):
            await self.message_bus.send_to_character(payload["victim"].id,
                                                     self.message_bus.text_to_message(payload["to_victim"]))
            prompted.append(payload["victim"])
        if payload.get("to_room"):
            targets = payload.get("targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)
        return prompted

    def is_safe(self, attacker, victim, room=None) -> tuple[bool, str]:
        if attacker is None or victim is None:
            return True, "You cannot attack that.\r\n"

        if attacker is victim:
            return True, "You hit yourself. Ouch!\r\n"

        if room is not None and not self._entity_in_room(room, victim):
            return True, "They aren't here.\r\n"

        if attacker.room_id != victim.room_id:
            return True, "They aren't here.\r\n"

        if FightUtil.entity_position_value(victim) <= self.PositionsEnum.POS_DEAD.value:
            return True, "They are already dead.\r\n"

        if CharacterApi.is_set(room.room_flags, self.RoomFlags.ROOM_SAFE.value):
            return True, "Not in this room.\r\n"

        if CharacterApi.is_npc(victim):
            mob_act = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "act", 0), 0)
            protected_bits = ("ACT_TRAIN", "ACT_PRACTICE", "ACT_IS_HEALER", "ACT_IS_CHANGER")
            for bit_name in protected_bits:
                if CharacterApi.is_set(mob_act, CharacterApi.enum_bit(self.ActBits, bit_name)):
                    return True, "I don't think Mota would approve.\r\n"
            if not CharacterApi.is_npc(attacker) and CharacterApi.is_set(mob_act, CharacterApi.enum_bit(self.ActBits,
                                                                                                        "ACT_PET")):
                return True, "But they look so cute and cuddly...\r\n"

        if getattr(victim, "fighting", None) is not None and getattr(victim, "fighting", None) is not attacker:
            return True, "Kill stealing is not permitted.\r\n"

        # Keep this permissive for now; detailed PK and charm rules migrate next.
        return False, ""

    def is_safe_spell(self, attacker, victim, area: bool = False) -> bool:
        if attacker is None or victim is None:
            return True
        if area and victim is attacker:
            return True
        room = self._find_room_for_entity(attacker)
        safe, _message = self.is_safe(attacker, victim, room=room)
        return safe

    #  TO-DO
    def check_killer(self, attacker, victim) -> None:
        return

    def check_parry(self, attacker, victim) -> bool:
        if not CharacterApi.is_awake(victim):
            return False
        skill = self._defense_skill_percent(victim, "parry")
        if skill <= 0:
            return False

        stats = getattr(victim, "character_attributes", None)
        dex = GenericUtil.to_int(getattr(stats, "dexterity", 10), 10)
        chance = max(0, min(60, skill // 2 + dex // 4))
        return random.randint(1, 100) <= chance

    def check_shield_block(self, attacker, victim) -> bool:
        if not CharacterApi.is_awake(victim) or victim.equipped is None or not victim.equipped.is_shield_equipped():
            return False
        skill = self._defense_skill_percent(victim, "shield block")
        if skill <= 0:
            return False

        stats = getattr(victim, "character_attributes", None)
        dex = GenericUtil.to_int(getattr(stats, "dexterity", 10), 10)
        chance = max(0, min(50, skill // 2 + dex // 4))
        return random.randint(1, 100) <= chance

    def check_dodge(self, attacker, victim) -> bool:
        if not CharacterApi.is_awake(victim):
            return False
        skill = self._defense_skill_percent(victim, "dodge")
        if skill <= 0:
            return False

        stats = getattr(victim, "character_attributes", None)
        dex = GenericUtil.to_int(getattr(stats, "dexterity", 10), 10)
        chance = max(0, min(65, skill // 2 + dex // 3))
        return random.randint(1, 100) <= chance

    def update_pos(self, victim) -> None:
        hit = GenericUtil.to_int(getattr(victim, "hit", 0), 0)
        pos_stunned = int(getattr(getattr(self.PositionsEnum, "POS_STUNNED", 0), "value", getattr(self.PositionsEnum, "POS_STUNNED", 0)))
        pos_fighting = int(getattr(getattr(self.PositionsEnum, "POS_FIGHTING", pos_stunned), "value", getattr(self.PositionsEnum, "POS_FIGHTING", pos_stunned)))
        pos_standing = int(getattr(getattr(self.PositionsEnum, "POS_STANDING", pos_fighting), "value", getattr(self.PositionsEnum, "POS_STANDING", pos_fighting)))
        pos_dead = int(getattr(getattr(self.PositionsEnum, "POS_DEAD", 0), "value", getattr(self.PositionsEnum, "POS_DEAD", 0)))
        pos_mortal = int(getattr(getattr(self.PositionsEnum, "POS_MORTAL", pos_stunned), "value", getattr(self.PositionsEnum, "POS_MORTAL", pos_stunned)))
        pos_incap = int(getattr(getattr(self.PositionsEnum, "POS_INCAP", pos_stunned), "value", getattr(self.PositionsEnum, "POS_INCAP", pos_stunned)))

        if hit > 0:
            if FightUtil.entity_position_value(victim) <= pos_stunned:
                self._set_position(victim, pos_fighting if getattr(victim, "fighting", None) is not None else pos_standing)
            return

        if CharacterApi.is_npc(victim) or hit <= -11:
            self._set_position(victim, pos_dead)
            return
        if hit <= -6:
            self._set_position(victim, pos_mortal)
            return
        if hit <= -3:
            self._set_position(victim, pos_incap)
            return

        self._set_position(victim, pos_stunned)

    @staticmethod
    def _set_position(entity, position_value: int) -> None:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            attrs.position = position_value
            return
        setattr(entity, "position", position_value)

    def stop_fighting(self, combatant, both: bool = False) -> None:
        if combatant is None:
            return

        participants = [combatant]
        opponent = getattr(combatant, "fighting", None)
        if both and opponent is not None and opponent not in participants:
            participants.append(opponent)
        combatant_id = str(getattr(combatant, "id", "") or "")
        if both and combatant_id:
            for event in list(self.combat_registry.get_by_combatant(combatant_id)):
                room = self.room_registry.get_or_none(id=event.room_id)
                if room is None:
                    continue
                for entity_id in (event.attacker_id, event.defender_id):
                    entity = self._find_entity_in_room_by_id(room, entity_id)
                    if entity is None or entity in participants:
                        continue
                    if entity is combatant or getattr(entity, "fighting", None) is combatant:
                        participants.append(entity)

        for participant in participants:
            participant.fighting = None
            self._set_default_combat_position(participant)
            self.combat_registry.remove_by_combatant(str(getattr(participant, "id", "") or ""))

    def aggressive_entry_rounds(self, character, room=None) -> list[tuple[object, dict]]:
        room = room or self._find_room_for_entity(character)
        if character is None or room is None or CharacterApi.is_npc(character) or CharacterApi.is_immortal(character):
            return []

        area = self.area_registry.get_or_none(id=getattr(room, "area_id", ""))
        if area is not None and bool(getattr(area, "empty", False)):
            return []

        rounds: list[tuple[object, dict]] = []
        for aggressor in list(getattr(room, "mobiles", {}).values()):
            if aggressor is None or not self._should_aggress(aggressor, character, room):
                continue

            victim = self._select_aggressive_victim(aggressor, room)
            if self._start_aggressive_combat(aggressor, victim):
                continue

        return rounds

    def aggressive_room_rounds(self, room) -> list[tuple[object, dict]]:
        if room is None:
            return []

        area = self.area_registry.get_or_none(id=getattr(room, "area_id", ""))
        if area is not None and bool(getattr(area, "empty", False)):
            return []

        for aggressor in list(getattr(room, "mobiles", {}).values()):
            if aggressor is None:
                continue
            victim = self._select_aggressive_victim(aggressor, room)
            if victim is None or not self._should_aggress(aggressor, victim, room):
                continue
            self._start_aggressive_combat(aggressor, victim)

        return []

    def _start_aggressive_combat(self, aggressor, victim) -> bool:
        if aggressor is None or victim is None or aggressor is victim:
            return False
        if getattr(aggressor, "fighting", None) is not None:
            return False

        victim_fighting = getattr(victim, "fighting", None)
        if victim_fighting not in (None, aggressor):
            return False

        self._set_fighting(aggressor, victim)
        return getattr(aggressor, "fighting", None) is victim

    def dam_message(self, attacker, victim, dam: int, dt: str = "TYPE_HIT", immune: bool = False) -> dict:
        thresholds = [
            (0, "miss", "misses"),
            (4, "scratch", "scratches"),
            (8, "graze", "grazes"),
            (12, "hit", "hits"),
            (16, "injure", "injures"),
            (20, "wound", "wounds"),
            (24, "maul", "mauls"),
            (28, "decimate", "decimates"),
            (32, "devastate", "devastates"),
            (36, "maim", "maims"),
            (40, "MUTILATE", "MUTILATES"),
            (44, "DISEMBOWEL", "DISEMBOWELS"),
            (48, "DISMEMBER", "DISMEMBERS"),
            (52, "MASSACRE", "MASSACRES"),
            (56, "MANGLE", "MANGLES"),
            (60, "*** DEMOLISH ***", "*** DEMOLISHES ***"),
            (75, "*** DEVASTATE ***", "*** DEVASTATES ***"),
            (100, "=== OBLITERATE ===", "=== OBLITERATES ==="),
            (125, ">>> ANNIHILATE <<<", ">>> ANNIHILATES <<<"),
            (150, "<<< ERADICATE >>>", "<<< ERADICATES >>>"),
        ]
        vs, vp = "do UNSPEAKABLE things to", "does UNSPEAKABLE things to"
        for max_dam, s, p in thresholds:
            if dam <= max_dam:
                vs, vp = s, p
                break

        punct = "." if dam <= 24 else "!"
        attacker_name = self._combat_target_name(attacker)
        victim_name = self._combat_target_name(victim)

        if dt == "TYPE_HIT":
            if immune:
                to_char = f"You are unaffected by your attack.\r\n"
                to_victim = f"{attacker_name}'s attack is powerless against you.\r\n"
                to_room = f"{attacker_name}'s attack is powerless against {victim_name}!\r\n"
            else:
                to_char = f"You {vs} {victim_name}{punct}\r\n"
                to_victim = f"{attacker_name} {vp} you{punct}\r\n"
                to_room = f"{attacker_name} {vp} {victim_name}{punct}\r\n"
        else:
            noun = str(dt or "attack").replace("_", " ").lower()
            if noun in ("type undefined", "undefined", "type hit", "type undefined hit"):
                attack_noun = str(getattr(attacker, "dam_type", "") or "").strip().lower()
                noun = attack_noun if attack_noun and attack_noun != "none" else "punch"
            if immune:
                to_char = f"{victim_name} is unaffected by your {noun}!\r\n"
                to_victim = f"{attacker_name}'s {noun} is powerless against you.\r\n"
                to_room = f"{attacker_name}'s {noun} is powerless against {victim_name}!\r\n"
            else:
                to_char = f"Your {noun} {vp} {victim_name}{punct}\r\n"
                to_victim = f"{attacker_name}'s {noun} {vp} you{punct}\r\n"
                to_room = f"{attacker_name}'s {noun} {vp} {victim_name}{punct}\r\n"

        to_victim = self._sentence_case(to_victim)
        to_room = self._sentence_case(to_room)
        return {"to_char": to_char, "to_victim": to_victim, "to_room": to_room}

    def raw_kill(self, victim) -> None:
        room = self._find_room_for_entity(victim)
        self.stop_fighting(victim, both=True)

        if room is not None:
            self.death_cry(victim, room)
            self.make_corpse(victim, room)

        if CharacterApi.is_npc(victim):
            room.mobiles.pop(victim.id)
            proto = self.mobile_registry.get_or_none(vnum=victim.vnum)
            if proto is not None:
                proto.killed = GenericUtil.to_int(getattr(proto, "killed", 0), 0) + 1
            self.mobile_handler.record_mobile_kill(victim)
            return

        self._restore_player_after_death(victim, room)

    def death_cry(self, victim, room) -> None:
        if victim is None or room is None:
            return

        parts = self._entity_parts(victim)
        form = self._entity_form(victim)
        BodyParts.maybe_create_death_cry_part(victim, room, self.item_registry, self.WellKnownObjectVnums,
                                              form_flags=form, parts_flags=parts)

    def make_corpse(self, victim, room) -> None:
        vnum = self.WellKnownObjectVnums.OBJ_VNUM_CORPSE_PC.value if type(
            victim) is Character else self.WellKnownObjectVnums.OBJ_VNUM_CORPSE_NPC.value
        money, timer_max, timer_min = self._corpse_timer_and_money(victim)
        corpse = ItemUtil.create_object(self.item_registry.get(vnum=str(vnum)))
        corpse.timer = random.randint(timer_min, timer_max)
        corpse.level = GenericUtil.to_int(victim.level)
        corpse.cost = 0
        victim_name = self._corpse_name(victim)
        corpse.short_description = self._format_template(getattr(corpse, "short_description", ""), victim_name)
        corpse.long_description = self._format_template(getattr(corpse, "long_description", ""), victim_name)

        self._transfer_victim_property(corpse, room, victim)
        if money is not None:
            corpse.contains.append(money)
        room.add_item_to_room(corpse)

    def _transfer_victim_property(self, corpse: Item, room, victim):
        for item in victim.owned_items():
            self._prepare_loot_item(item)
            if self._is_floating_item(item):
                room.add_item_to_room(item)
            else:
                corpse.contains.append(item)

    def _corpse_timer_and_money(self, victim) -> tuple[Item | None, Literal[6, 40], Literal[3, 25]]:
        money = None
        if CharacterApi.is_npc(victim):
            timer_min, timer_max = 3, 6
            if victim.gold > 0:
                money = ItemUtil.create_money(victim.gold, victim.silver, self.item_registry, self.WellKnownObjectVnums)
                victim.gold = 0
                victim.silver = 0
        else:
            if victim.gold > 1 or victim.silver > 1:
                money = ItemUtil.create_money(victim.gold, victim.silver, self.item_registry, self.WellKnownObjectVnums)
                victim.gold -= victim.gold / 2
                victim.silver -= victim.silver / 2
            timer_min, timer_max = 25, 40
        return money, timer_max, timer_min

    def xp_compute(self, gch, victim, total_levels: int) -> int:
        if gch is None or victim is None:
            return 0

        gch_level = max(1, GenericUtil.to_int(getattr(gch, "level", 1), 1))
        victim_level = GenericUtil.to_int(getattr(victim, "level", 1), 1)
        level_range = victim_level - gch_level

        base_table = {
            -9: 1,
            -8: 2,
            -7: 5,
            -6: 9,
            -5: 11,
            -4: 22,
            -3: 33,
            -2: 50,
            -1: 66,
            0: 83,
            1: 99,
            2: 121,
            3: 143,
            4: 165,
        }
        base_exp = base_table.get(level_range, 0)
        if level_range > 4:
            base_exp = 160 + 20 * (level_range - 4)

        # Alignment adjustment follows ROM semantics.
        gch_align = gch.get_alignment()
        victim_align = victim.get_alignment()
        align = victim_align - gch_align

        act_bits = CharacterApi.get_enum("actBits")
        no_align_bit = CharacterApi.enum_bit(act_bits, "ACT_NOALIGN")
        victim_act = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "act", 0), 0)
        no_align = no_align_bit > 0 and CharacterApi.is_set(victim_act, no_align_bit)

        if not no_align:
            total = max(1, GenericUtil.to_int(total_levels, gch_level))
            if align > 500:
                change = ((align - 500) * base_exp // 500) * gch_level // total
                change = max(1, change)
                gch_align = max(-1000, gch_align - change)
            elif align < -500:
                change = ((-1 * align - 500) * base_exp // 500) * gch_level // total
                change = max(1, change)
                gch_align = min(1000, gch_align + change)
            else:
                change = (gch_align * base_exp // 500) * gch_level // total
                gch_align = gch_align - change
            gch.set_alignment(gch_align)

        if no_align:
            xp = base_exp
        elif gch_align > 500:
            if victim_align < -750:
                xp = (base_exp * 4) // 3
            elif victim_align < -500:
                xp = (base_exp * 5) // 4
            elif victim_align > 750:
                xp = base_exp // 4
            elif victim_align > 500:
                xp = base_exp // 2
            elif victim_align > 250:
                xp = (base_exp * 3) // 4
            else:
                xp = base_exp
        elif gch_align < -500:
            if victim_align > 750:
                xp = (base_exp * 5) // 4
            elif victim_align > 500:
                xp = (base_exp * 11) // 10
            elif victim_align < -750:
                xp = base_exp // 2
            elif victim_align < -500:
                xp = (base_exp * 3) // 4
            elif victim_align < -250:
                xp = (base_exp * 9) // 10
            else:
                xp = base_exp
        elif gch_align > 200:
            if victim_align < -500:
                xp = (base_exp * 6) // 5
            elif victim_align > 750:
                xp = base_exp // 2
            elif victim_align > 0:
                xp = (base_exp * 3) // 4
            else:
                xp = base_exp
        elif gch_align < -200:
            if victim_align > 500:
                xp = (base_exp * 6) // 5
            elif victim_align < -750:
                xp = base_exp // 2
            elif victim_align < 0:
                xp = (base_exp * 3) // 4
            else:
                xp = base_exp
        else:
            if victim_align > 500 or victim_align < -500:
                xp = (base_exp * 4) // 3
            elif -200 < victim_align < 200:
                xp = base_exp // 2
            else:
                xp = base_exp

        if gch_level < 6:
            xp = 10 * xp // (gch_level + 4)

        if gch_level > 35:
            xp = 15 * xp // (gch_level - 25)

        played = GenericUtil.to_int(getattr(gch, "played", 0), 0)
        logon = GenericUtil.to_int(getattr(gch, "logon", 0), 0)
        now_epoch = GenericUtil.to_int(getattr(gch, "current_time", 0), 0)
        if now_epoch <= 0:
            import time
            now_epoch = int(time.time())
        elapsed = played + max(0, now_epoch - logon) if logon > 0 else 0
        if elapsed > 0:
            time_per_level = (4 * (elapsed // 3600)) // gch_level
            time_per_level = max(2, min(12, time_per_level))
            if gch_level < 15:
                time_per_level = max(time_per_level, 15 - gch_level)
            xp = xp * time_per_level // 12

        low = max(0, xp * 3 // 4)
        high = max(low, xp * 5 // 4)
        xp = random.randint(low, high)

        total_levels = max(1, GenericUtil.to_int(total_levels, gch_level))
        xp = xp * gch_level // max(1, total_levels - 1)
        return max(0, xp)

    def damage(self, attacker, victim, dam: int, dt: str = "TYPE_HIT", dam_type: str = "NONE", show: bool = True,
               weapon_hit: bool = False) -> dict:
        if victim is None:
            self._error_payload()

        applied = max(0, GenericUtil.to_int(dam, 0))
        dam_type_name = FightUtil.normalize_damage_type_name(dam_type)

        self.logger.debug(f"Damage calculation 1: dam={dam}, applied={applied}, dam_type={dam_type}")
        if applied > 35:
            applied = (applied - 35) // 2 + 35
        if applied > 80:
            applied = (applied - 80) // 2 + 80

        self._set_fighting(attacker, victim)

        if applied > 1 and not CharacterApi.is_npc(victim):
            if GenericUtil.to_int(victim.status_flags.drunk, 0) > 10:
                applied = 9 * applied // 10

        if applied > 1 and CharacterApi.is_affected(victim, self.AffectBits.AFF_SANCTUARY):
            applied //= 2

        if applied > 1:
            protected = ((CharacterApi.is_affected(victim, self.AffectBits.AFF_PROTECT_EVIL) and CharacterApi.is_evil(
                attacker))
                         or (CharacterApi.is_affected(victim,
                                                      self.AffectBits.AFF_PROTECT_GOOD) and CharacterApi.is_good(
                        attacker)))
            if protected:
                applied -= applied // 4

        self.logger.debug(f"Damage calculation 2: dam={dam}, applied={applied}, dam_type={dam_type}")
        if weapon_hit and attacker is not None and victim is not attacker:
            if self.check_parry(attacker, victim) or self.check_dodge(attacker, victim) or self.check_shield_block(
                    attacker, victim):
                msg = self.dam_message(attacker, victim, 0, dt=dt, immune=False)
                msg["killed"] = False
                msg["xp_gain"] = 0
                msg["level_up_messages"] = ""
                self.logger.debug(f"Parry/Dodge/Shield Block: {msg['to_char']} {msg['to_victim']} {msg['to_room']}")
                return msg

        immunity = self._check_immunity(victim, dam_type_name)
        immune = immunity == "IS_IMMUNE"
        if immune:
            applied = 0
        elif immunity == "IS_RESISTANT":
            applied -= applied // 3
        elif immunity == "IS_VULNERABLE":
            applied += applied // 2

        if show:
            msg = self.dam_message(attacker, victim, applied, dt=dt, immune=immune)
        else:
            msg = {"to_char": "", "to_victim": "", "to_room": ""}

        if applied == 0:
            msg["killed"] = False
            msg["xp_gain"] = 0
            msg["level_up_messages"] = ""
            return msg

        original_hit = GenericUtil.to_int(getattr(victim, "hit", 0), 0)
        setattr(victim, "hit", original_hit - applied)
        self.update_pos(victim)

        killed = False
        xp_gain = 0
        advancement = None
        if FightUtil.entity_position_value(victim) <= int(self.PositionsEnum.POS_DEAD.value):
            killed = True
            xp_gain = 0
            if attacker is not None and not CharacterApi.is_npc(attacker) and CharacterApi.is_npc(victim):
                attacker_level = max(1, GenericUtil.to_int(getattr(attacker, "level", 1), 1))
                xp_gain = self.xp_compute(attacker, victim, attacker_level)
                advancement = CharacterAdvancement.gain_experience(attacker, xp_gain)
            self.raw_kill(victim)

        msg["killed"] = killed
        msg["xp_gain"] = xp_gain if killed else 0
        msg["level_up_messages"] = advancement.level_up_messages if advancement is not None else ""
        return msg

    def set_fighting(self, attacker: Any, defender: Any, room_id: str) -> CombatEvent | None:
        if attacker is None or defender is None:
            return None
        if getattr(attacker, "fighting", None) is not None:
            return None

        attacker.fighting = defender
        FightUtil.set_fighting_position(attacker, self.PositionsEnum)
        return self.combat_registry.upsert(getattr(attacker, "id", ""), getattr(defender, "id", ""), room_id)

    def _set_fighting(self, attacker, victim: Any | None):
        if attacker is not None and victim is not attacker:
            victim_fighting = getattr(victim, "fighting", None)
            attacker_fighting = getattr(attacker, "fighting", None)
            if FightUtil.entity_position_value(victim) > self.PositionsEnum.POS_STUNNED and victim_fighting is None:
                room = self._find_room_for_entity(victim)
                if room is not None:
                    self.set_fighting(victim, attacker, room.id)
            if FightUtil.entity_position_value(victim) > self.PositionsEnum.POS_STUNNED and attacker_fighting is None:
                room = self._find_room_for_entity(attacker) or self._find_room_for_entity(victim)
                if room is not None:
                    self.set_fighting(attacker, victim, room.id)

    def one_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        if victim is attacker or attacker is None or victim is None:
            return self._error_payload()

        if FightUtil.entity_position_value(victim) <= int(self.PositionsEnum.POS_DEAD.value):
            return self._error_payload()

        attacker_room = self.room_registry.get(id=attacker.room_id)
        victim_room = self.room_registry.get(id=victim.room_id)
        if attacker_room is None or victim_room is None or attacker_room.id != victim_room.id:
            return self._error_payload()

        weapon = self._wielded_weapon(attacker)
        attack_verb = self._attack_verb(attacker, dt)
        dam_type = self._attack_damage_type(attacker, dt, attack_verb)
        improve_skill = SkillUtil.active_melee_skill_name(weapon, self.WeaponClass)
        skill = self._weapon_skill_total(attacker, weapon)
        base_skill = max(0, skill - 20)
        thac0 = self._thac0(attacker, dt, skill)
        victim_ac = self._victim_ac_for_damage_type(victim, dam_type)
        if victim_ac < -15:
            victim_ac = (victim_ac + 15) // 5 - 15

        if not CharacterApi.can_see(attacker, victim, attacker_room):
            victim_ac -= 4
        if FightUtil.entity_position_value(victim) < self.PositionsEnum.POS_FIGHTING.value:
            victim_ac += 4
        if FightUtil.entity_position_value(victim) < self.PositionsEnum.POS_RESTING.value:
            victim_ac += 6

        roll = self._to_hit_roll()
        if roll == 0 or (roll != 19 and roll < thac0 - victim_ac):
            Ability.check_improve_by_name(attacker, improve_skill, False, 5)
            self.logger.info(
                f"Miss: {attacker.name}, dam: {0}, roll: {roll}, thac0: {thac0}, victim_ac: {victim_ac}, weapon: {getattr(weapon, 'name', None)}, dam_type: {dam_type}, skill_name: {improve_skill}, skill: {skill}, base_skill: {base_skill}")
            return self.damage(attacker, victim, 0, dt=attack_verb, dam_type=dam_type, weapon_hit=True)
        else:
            dam = self._attack_damage(attacker, victim=victim, dt=dt, weapon=weapon, skill=skill)
            Ability.check_improve_by_name(attacker, improve_skill, True, 5)
            self.logger.info(
                f"Hit: {attacker.name}, dam: {dam}, roll: {roll}, thac0: {thac0}, victim_ac: {victim_ac}, weapon: {getattr(weapon, 'name', None)}, dam_type: {dam_type}, skill_name: {improve_skill}, skill: {skill}, base_skill: {base_skill}")
            return self.damage(attacker, victim, dam, dt=attack_verb, dam_type=dam_type, weapon_hit=True)

    def mob_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        payload = self.one_hit(attacker, victim, dt=dt)

        if getattr(attacker, "fighting", None) is not victim:
            return payload

        room = self._find_room_for_entity(attacker)
        if room is not None and self._mob_has_off(attacker, "OFF_AREA_ATTACK"):
            for entity in room.people():
                if entity is victim:
                    continue
                if getattr(entity, "fighting", None) is attacker:
                    payload = self._merge_attack_payloads(payload, self.one_hit(attacker, entity, dt=dt))

        if CharacterApi.is_affected(attacker, CharacterApi.enum_bit(self.AffectBits, "AFF_HASTE")) or (
                self._mob_has_off(attacker, "OFF_FAST") and not CharacterApi.is_affected(attacker,
                                                                                         CharacterApi.enum_bit(
                                                                                             self.AffectBits,
                                                                                             "AFF_SLOW"))
        ):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        if getattr(attacker, "fighting", None) is not victim or self._is_backstab_attack(dt):
            return payload

        chance = self._skill_percent(attacker, "second attack") // 2
        if CharacterApi.is_affected(attacker,
                                    CharacterApi.enum_bit(self.AffectBits, "AFF_SLOW")) and not self._mob_has_off(
                attacker, "OFF_FAST"):
            chance //= 2
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))
            if getattr(attacker, "fighting", None) is not victim:
                return payload

        chance = self._skill_percent(attacker, "third attack") // 4
        if CharacterApi.is_affected(attacker,
                                    CharacterApi.enum_bit(self.AffectBits, "AFF_SLOW")) and not self._mob_has_off(
                attacker, "OFF_FAST"):
            chance = 0
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        return payload

    def multi_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        if attacker is None or victim is None:
            return self._error_payload()

        self._decrement_combat_timers(attacker)
        if FightUtil.entity_position_value(attacker) < self.PositionsEnum.POS_RESTING.value:
            return self._error_payload()

        if CharacterApi.is_npc(attacker):
            return self.mob_hit(attacker, victim, dt=dt)

        payload = self.one_hit(attacker, victim, dt=dt)
        if getattr(attacker, "fighting", None) is not victim:
            return payload

        if CharacterApi.is_affected(attacker, CharacterApi.enum_bit(self.AffectBits, self.AffectBits.AFF_HASTE.name)):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        if getattr(attacker, "fighting", None) is not victim or self._is_backstab_attack(dt):
            return payload

        chance = self._skill_percent(attacker, "second attack") // 2
        if CharacterApi.is_affected(attacker, CharacterApi.enum_bit(self.AffectBits, self.AffectBits.AFF_SLOW.name)):
            chance //= 2
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))
            if getattr(attacker, "fighting", None) is not victim:
                return payload

        chance = self._skill_percent(attacker, "third attack") // 4
        if CharacterApi.is_affected(attacker, CharacterApi.enum_bit(self.AffectBits, self.AffectBits.AFF_SLOW.name)):
            chance = 0
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        return payload

    # TO-DO
    def check_assist(self, attacker, victim) -> None:
        from mobile.Mobile import Mobile
        if type(attacker) is Mobile:
            return None
        room = self.room_registry.get(id=attacker.room_id)
        for char in room.people():
            if (not CharacterApi.is_npc(attacker) and
                    CharacterApi.is_npc(char) and
                    MobileApi.mobile_will_assist(char) and
                    char.level + 6 > victim.level):
                # questionable TO-DO: do_function->do_emote
                self.message_bus.send_to_room(self.message_bus.text_to_message(f"{char.name} screams and attacks!"),
                                              room.players_in_room())
                self.multi_hit(char, victim, dt="TYPE_UNDEFINED")
                continue
            if (not CharacterApi.is_npc(attacker) or
                    CharacterApi.is_affected(attacker, self.AffectBits.AFF_CHARM.value)):

                if ((not CharacterApi.is_npc(char) and CharacterApi.player_auto_assist(char)) or
                    CharacterApi.is_affected(char, self.AffectBits.AFF_CHARM.value)) and \
                        CharacterApi.is_same_group(attacker, char) and \
                        not self.is_safe(char, victim):
                    self.multi_hit(char, victim, dt="TYPE_UNDEFINED")
                continue
        return

    def build_round_payload(self, attacker, victim, room, result: dict, pre_corpse_ids=None) -> dict:
        attacker_id = str(getattr(attacker, "id", "") or "")
        victim_id = str(getattr(victim, "id", "") or "")
        targets = room.player_targets(attacker) if hasattr(room, "player_targets") else list(room.characters.values())
        payload = {
            "to_char": result.get("to_char", ""),
            "to_room": result.get("to_room", ""),
            "targets": [ch for ch in targets if str(getattr(ch, "id", "") or "") not in (attacker_id, victim_id)],
        }

        if not CharacterApi.is_npc(victim):
            payload["victim"] = victim
            payload["to_victim"] = result.get("to_victim", "")

        if not result.get("killed"):
            if not CharacterApi.is_npc(attacker) and CharacterApi.is_npc(victim):
                payload["to_char"] = self._append_condition_line(payload["to_char"], victim)
            # elif CharacterApi.is_npc(attacker) and not CharacterApi.is_npc(victim):
            #     payload["to_victim"] = self._append_condition_line(payload.get("to_victim", ""), attacker)

        if not result.get("killed"):
            return payload

        if not CharacterApi.is_npc(attacker):
            victim_name = self._combat_target_name(victim)
            payload["to_char"] = (payload["to_char"] or "") + f"{victim_name} is DEAD!!\r\n"
            xp_gain = int(result.get("xp_gain", 0) or 0)
            payload["to_char"] = (payload["to_char"] or "") + f"You receive {xp_gain} experience points.\r\n"
            payload["to_char"] = (payload["to_char"] or "") + str(result.get("level_up_messages", "") or "")
            payload["to_char"] = (payload["to_char"] or "") + f"You hear {victim_name}'s death cry.\r\n"

            corpse = self._find_latest_corpse(room, victim, pre_corpse_ids)
            if corpse is not None and self._player_act_enabled(attacker, "PLR_AUTOLOOT"):
                self._autoloot_corpse(attacker, corpse)

            if corpse is not None and self._player_act_enabled(attacker, "PLR_AUTOSAC"):
                if not (self._player_act_enabled(attacker, "PLR_AUTOLOOT") and list(
                        getattr(corpse, "contains", []) or [])):
                    sacrifice = self._autosacrifice_corpse(attacker, corpse, room)
                    if sacrifice is not None:
                        payload["to_char"] = (payload["to_char"] or "") + sacrifice.get("to_char", "")
                        payload["to_room"] = (payload["to_room"] or "") + sacrifice.get("to_room", "")

        return payload

    def _find_room_for_entity(self, entity):
        entity_id = getattr(entity, "id", "")
        if not entity_id:
            return None

        room_id = str(getattr(entity, "room_id", "") or "")
        if room_id:
            room = self.room_registry.get_or_none(id=room_id)
            if room is not None:
                return room

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            if entity_id in getattr(room, "characters", {}) or entity_id in getattr(room, "mobiles", {}):
                return room
        return None

    @staticmethod
    def _corpse_name(entity) -> str:
        if CharacterApi.is_npc(entity):
            return str(getattr(entity, "short_description", "") or getattr(entity, "name", "someone"))
        return str(getattr(entity, "name", "someone"))

    @staticmethod
    def _format_template(text: str, victim_name: str) -> str:
        raw = str(text or "")
        if "%s" in raw:
            try:
                return raw % victim_name
            except Exception:
                return raw.replace("%s", victim_name)
        return raw

    @staticmethod
    def _prepare_loot_item(item) -> None:
        item_type = str(getattr(item, "item_type", "") or "").lower()
        if "potion" in item_type:
            item.timer = random.randint(500, 1000)
        elif "scroll" in item_type:
            item.timer = random.randint(1000, 2500)

    def _entity_form(self, entity) -> int:
        if CharacterApi.is_npc(entity):
            form = getattr(getattr(entity, "status_flags", None), "form", None)
            if form is None:
                form = getattr(entity, "form", 0)
            return GenericUtil.to_int(form, 0)

        return int(BodyForm.default_player_form())

    def _entity_parts(self, entity) -> int:
        if CharacterApi.is_npc(entity):
            parts = getattr(getattr(entity, "status_flags", None), "parts", None)
            if parts is None:
                parts = getattr(entity, "parts", 0)
            return GenericUtil.to_int(parts, 0)

        return int(BodyParts.default_player_parts())

    @staticmethod
    def _is_floating_item(item) -> bool:
        wear_location_enum = CharacterApi.get_enum("wearLocation")
        wear_float = CharacterApi.enum_bit(wear_location_enum, "WEAR_FLOAT")

        wear_loc = GenericUtil.to_int(getattr(item, "wear_loc", -1), -1)
        if wear_float > 0 and wear_loc == wear_float:
            return True

        wear_location = str(getattr(item, "wear_location", "") or "").strip().upper()
        if wear_location == "WEAR_FLOAT":
            return True

        return False

    @staticmethod
    def _entity_in_room(room, entity) -> bool:
        entity_id = str(getattr(entity, "id", "") or "")
        if not entity_id:
            return False
        if entity_id in getattr(room, "characters", {}):
            return True
        if entity_id in getattr(room, "mobiles", {}):
            return True
        return False

    @staticmethod
    def _find_entity_in_room_by_id(room, entity_id: str):
        wanted = str(entity_id or "")
        if not wanted:
            return None
        if wanted in getattr(room, "characters", {}):
            return room.characters[wanted]
        if wanted in getattr(room, "mobiles", {}):
            return room.mobiles[wanted]
        return None

    def _player_act_enabled(self, character, flag_name: str) -> bool:
        if CharacterApi.is_npc(character):
            return False
        bit = CharacterApi.enum_bit(self.PlayerActBits, flag_name)
        if bit <= 0:
            return False
        return CharacterApi.is_set(character.status_flags.act, bit)

    @staticmethod
    def _find_latest_corpse(room, victim, pre_corpse_ids=None):
        if room is None:
            return None

        pre_corpse_ids = set(pre_corpse_ids or set())
        victim_name = FightHandler._combat_target_name(victim).lower()
        for item in reversed(list(room.contents.values())):
            item_type = str(getattr(item, "item_type", "") or "").lower()
            if "corpse" not in item_type:
                continue
            item_id = str(getattr(item, "id", "") or "")
            if item_id and item_id in pre_corpse_ids:
                continue
            short_desc = str(getattr(item, "short_description", "") or "").lower()
            if victim_name and victim_name in short_desc:
                return item
        return None

    @staticmethod
    def _combat_target_name(target) -> str:
        if target is None:
            return "someone"
        if CharacterApi.is_npc(target):
            return str(getattr(target, "short_description", "") or getattr(target, "name", "someone"))
        return str(getattr(target, "name", "someone"))

    @staticmethod
    def _sentence_case(text: str) -> str:
        raw = str(text or "")
        if not raw:
            return raw
        return raw[:1].upper() + raw[1:]

    @staticmethod
    def _append_condition_line(text: str, target) -> str:
        base = str(text or "")
        condition = InfoUtil.target_condition_line(target)
        if not condition:
            return base
        if base and not base.endswith("\r\n"):
            base += "\r\n"
        return base + condition + "\r\n"

    @staticmethod
    def _merge_attack_payloads(base: dict, extra: dict) -> dict:
        if not base:
            return dict(extra or {})
        if not extra:
            return base

        merged = dict(base)
        for key in ("to_char", "to_victim", "to_room"):
            left = str(merged.get(key, "") or "")
            right = str(extra.get(key, "") or "")
            merged[key] = left + right
        merged["killed"] = bool(merged.get("killed")) or bool(extra.get("killed"))
        merged["xp_gain"] = GenericUtil.to_int(merged.get("xp_gain", 0), 0) + GenericUtil.to_int(
            extra.get("xp_gain", 0), 0)
        return merged

    def _autoloot_corpse(self, character, corpse) -> None:
        remaining = []
        for item in list(getattr(corpse, "contains", []) or []):
            if ItemApi.item_takeable(item, self.WearFlags):
                character.add_item(item)
            else:
                remaining.append(item)
        corpse.contains = remaining

    def _autosacrifice_corpse(self, attacker, corpse, room) -> dict | None:
        if room is None or corpse is None or not Item.is_npc_corpse(corpse):
            return None

        if not ItemApi.item_takeable(corpse, self.WearFlags) or ItemApi.has_item_flag(corpse, self.ItemFlags,
                                                                                      "ITEM_NO_SAC"):
            return None

        room.remove_item_from_room(corpse)
        silver = ItemUtil.sacrifice_silver_value(corpse)
        attacker.silver = int(getattr(attacker, "silver", 0) or 0) + silver
        return {
            "to_char": ItemUtil.sacrifice_reward_message(silver),
            "to_room": f"{attacker.name} sacrifices {Item.short(corpse)} to Mota.\r\n",
        }

    @staticmethod
    def _is_backstab_attack(dt: str) -> bool:
        text = str(dt or "").strip().lower()
        return text == "backstab" or text == "gsn_backstab"

    @staticmethod
    def _decrement_combat_timers(entity) -> None:
        if CharacterApi.is_npc(entity):
            if hasattr(entity, "pulse_wait"):
                entity.pulse_wait = max(0, GenericUtil.to_int(getattr(entity, "pulse_wait", 0), 0) - 12)
            if hasattr(entity, "pulse_daze"):
                entity.pulse_daze = max(0, GenericUtil.to_int(getattr(entity, "pulse_daze", 0), 0) - 12)
            return

        status_flags = getattr(entity, "status_flags", None)
        if status_flags is None:
            return
        status_flags.pulse_wait = max(0, GenericUtil.to_int(getattr(status_flags, "pulse_wait", 0), 0) - 12)
        status_flags.pulse_daze = max(0, GenericUtil.to_int(getattr(status_flags, "pulse_daze", 0), 0) - 12)

    def _mob_has_off(self, entity, off_name: str) -> bool:
        bit = CharacterApi.enum_bit(self.OffenseTypes, off_name)
        if bit <= 0:
            return False
        return CharacterApi.is_set(entity.status_flags.off, bit)

    def _skill_percent(self, entity, skill_name: str) -> int:
        wanted = str(skill_name or "").strip().lower()
        if not wanted:
            return 0

        if not CharacterApi.is_npc(entity):
            return Character.learned_entry_level(
                Character.get_learned(entity, skill_name, visible_only=True, visible_fn=Ability.practice_visible)
            )

        level = entity.level
        if wanted == "second attack":
            is_warrior = self._mob_has_act(entity, self.ActBits, self.ActBits.ACT_WARRIOR.name)
            is_thief = self._mob_has_act(entity, self.ActBits, self.ActBits.ACT_THIEF.name)
            return max(0, min(100, 10 + 3 * level)) if (is_warrior or is_thief) else 0
        if wanted == "third attack":
            return max(0, min(100, 4 * level - 40)) if self._mob_has_act(entity, self.ActBits,
                                                                         self.ActBits.ACT_WARRIOR.name) else 0
        return 0

    def _defense_skill_percent(self, entity, skill_name: str) -> int:
        wanted = str(skill_name or "").strip().lower()
        if not wanted:
            return 0

        if not CharacterApi.is_npc(entity):
            return self._skill_percent(entity, wanted)

        level = max(0, GenericUtil.to_int(getattr(entity, "level", 0), 0))
        if wanted == "shield block":
            return max(0, min(100, 10 + 2 * level))
        if wanted == "dodge":
            return max(0, min(100, 2 * level)) if self._mob_has_off(entity, self.OffenseTypes.OFF_DODGE.name) else 0
        if wanted == "parry":
            return max(0, min(100, 2 * level)) if self._mob_has_off(entity, self.OffenseTypes.OFF_PARRY.name) else 0
        return 0

    @staticmethod
    def _mob_has_act(entity, act_bits, act_name: str) -> bool:
        bit = CharacterApi.enum_bit(act_bits, act_name)
        if bit <= 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(entity, "status_flags", None), "act", 0), 0)
        return CharacterApi.is_set(flags, bit)

    def _should_aggress(self, aggressor, witness, room) -> bool:
        if aggressor is None or witness is None or room is None:
            return False
        if not CharacterApi.is_npc(aggressor):
            return False
        if getattr(aggressor, "fighting", None) is not None:
            return False

        mob_act = aggressor.status_flags.act
        room_bits = room.room_flags
        if not CharacterApi.is_set(mob_act, CharacterApi.enum_bit(self.ActBits, self.ActBits.ACT_AGGRESSIVE.name)):
            return False
        if CharacterApi.enum_bit(self.RoomFlags, "ROOM_SAFE") and CharacterApi.is_set(room_bits, CharacterApi.enum_bit(
                self.RoomFlags, self.RoomFlags.ROOM_SAFE.name)):
            return False
        if CharacterApi.is_affected(aggressor, CharacterApi.enum_bit(self.AffectBits, self.AffectBits.AFF_CALM.name)):
            return False
        if MobileApi.mobile_is_charmed(aggressor):
            return False
        if not CharacterApi.is_awake(aggressor):
            return False
        if self._mob_has_act(aggressor, self.ActBits, self.ActBits.ACT_WIMPY.name) and CharacterApi.is_awake(witness):
            return False
        if not CharacterApi.can_see(aggressor, witness, room):
            return False
        if self.rng.number_bits(1) == 0:
            return False
        return True

    def _select_aggressive_victim(self, aggressor, room):
        if aggressor is None or room is None:
            return None

        act_bits = CharacterApi.get_enum("actBits")
        victim = None
        count = 0
        for candidate in list(getattr(room, "characters", {}).values()):
            if CharacterApi.is_npc(candidate):
                continue
            if CharacterApi.is_immortal(candidate):
                continue
            if getattr(candidate, "fighting", None) is not None and getattr(candidate, "fighting",
                                                                            None) is not aggressor:
                continue
            if aggressor.level < candidate.level - 5:
                continue
            if self._mob_has_act(aggressor, act_bits, self.ActBits.ACT_WIMPY.name) and CharacterApi.is_awake(candidate):
                continue
            if not CharacterApi.can_see(aggressor, candidate, room):
                continue
            if self.rng.number_range(0, count) == 0:
                victim = candidate
            count += 1
        return victim

    @staticmethod
    def _wielded_weapon(attacker):
        equipped = getattr(attacker, "equipped", None)
        weapon = getattr(equipped, "wielded", None) if equipped is not None else None
        if weapon is None:
            return None
        item_type = str(getattr(weapon, "item_type", "") or "").strip().lower()
        return weapon if item_type == "weapon" else None

    def _resolve_attack_token(self, raw_value) -> tuple[str, dict | str | None]:
        token = str(raw_value or "").strip().lower()
        if not token:
            return "", None

        attack = self.attacks.get(token)
        if attack is not None:
            return token, attack

        numeric = GenericUtil.to_int(token, None)
        if numeric is None:
            return token, None

        attack_names = list(self.attacks.keys())
        if 0 <= numeric < len(attack_names):
            resolved = attack_names[numeric]
            return resolved, self.attacks.get(resolved)
        return token, None

    def _attack_verb(self, attacker, dt: str) -> str:
        raw_dt = str(dt or "").strip()
        if raw_dt and raw_dt not in ("TYPE_HIT", "TYPE_UNDEFINED"):
            return raw_dt

        weapon = self._wielded_weapon(attacker)
        if weapon is not None:
            verb, _attack = self._resolve_attack_token(getattr(weapon, "value3", ""))
            if verb and verb != "0":
                return verb

        dam_type, _attack = self._resolve_attack_token(getattr(attacker, "dam_type", ""))
        if dam_type and dam_type not in ("none", "0"):
            return dam_type
        return "punch"

    def _attack_damage(self, attacker, victim=None, dt: str = "TYPE_HIT", weapon=None, skill: int | None = None) -> int:
        weapon = weapon or self._wielded_weapon(attacker)
        skill = self._weapon_skill_total(attacker, weapon) if skill is None else max(0, skill)

        if CharacterApi.is_npc(attacker) and weapon is None:
            damage_dice = getattr(attacker, "damage_dice", None)
            if damage_dice is not None:
                number = max(0, GenericUtil.to_int(getattr(damage_dice, "number", 0), 0))
                dtype = max(0, GenericUtil.to_int(getattr(damage_dice, "type", 0), 0))
                bonus = max(0, GenericUtil.to_int(getattr(damage_dice, "bonus", 0), 0))
                rolled = self.rng.dice(number, dtype) + bonus
                if rolled > 0:
                    return rolled

        if CharacterApi.is_npc(attacker) and weapon is None:
            level = max(1, GenericUtil.to_int(getattr(attacker, "level", 1), 1))
            return max(1, self.rng.number_range(level // 2, (level * 3) // 2))

        if weapon is not None:
            dice_count = max(1, GenericUtil.to_int(getattr(weapon, "value1", 1), 1))
            dice_size = max(1, GenericUtil.to_int(getattr(weapon, "value2", 1), 1))
            dam = self.rng.dice(dice_count, dice_size) * skill // 100

            equipped = getattr(attacker, "equipped", None)
            if equipped is not None and getattr(equipped, "shield", None) is None:
                dam = dam * 11 // 10

            if GameApi.is_set(getattr(weapon, "value4", 0), self.WeaponTypes.WEAPON_SHARP.value):
                percent = self.rng.number_percent()
                if percent <= skill // 8:
                    dam = 2 * dam + (dam * 2 * percent // 100)
        else:
            level = max(1, GenericUtil.to_int(getattr(attacker, "level", 1), 1))
            low = 1 + (4 * skill // 100)
            high = max(low, (2 * level // 3) * skill // 100)
            dam = self.rng.number_range(low, high)

        enhanced_skill = self._skill_percent(attacker, "enhanced damage")
        if enhanced_skill > 0:
            roll = self.rng.number_percent()
            if roll <= enhanced_skill:
                self._check_improve(attacker, "enhanced damage", True, 6)
                dam += 2 * (dam * roll // 300)

        if victim is not None:
            if not CharacterApi.is_awake(victim):
                dam *= 2
            elif FightUtil.entity_position_value(victim) < self.PositionsEnum.POS_FIGHTING.value:
                dam = dam * 3 // 2

        if self._is_backstab_attack(dt) and weapon is not None:
            is_dagger = self._weapon_skill_name(weapon) == "dagger"
            level = max(1, GenericUtil.to_int(getattr(attacker, "level", 1), 1))
            dam *= 2 + (level // 8 if is_dagger else level // 10)

        dam += self._current_damroll(attacker)
        return max(1, dam)

    def _attack_damage_type(self, attacker, raw_dt: str, attack_verb: str) -> str:
        source, attack = self._resolve_attack_token(attack_verb)
        if self._is_backstab_attack(raw_dt):
            weapon = self._wielded_weapon(attacker)
            if weapon is not None:
                source, attack = self._resolve_attack_token(getattr(weapon, "value3", ""))
            elif not source:
                source, attack = self._resolve_attack_token(getattr(attacker, "dam_type", ""))
        if not source or source in ("type_hit", "type_undefined", "type hit", "type undefined"):
            source, attack = self._resolve_attack_token(getattr(attacker, "dam_type", ""))

        if isinstance(attack, dict):
            damage_type = attack.get("damage_type", "DAM_BASH")
        elif isinstance(attack, str) and attack:
            damage_type = attack
        else:
            damage_type = "DAM_BASH"
        if str(damage_type).strip() == "-1":
            damage_type = "DAM_NONE"

        return FightUtil.normalize_damage_type_name(damage_type)

    def _weapon_skill_name(self, weapon) -> str:
        return SkillUtil.weapon_skill_name(weapon, self.WeaponClass)

    def _weapon_skill_total(self, attacker, weapon) -> int:
        skill_name = self._weapon_skill_name(weapon)
        if CharacterApi.is_npc(attacker):
            level = max(0, GenericUtil.to_int(getattr(attacker, "level", 0), 0))
            if not skill_name:
                skill = 3 * level
            elif skill_name == "hand to hand":
                skill = 40 + 2 * level
            else:
                skill = 40 + (5 * level) // 2
        else:
            if not skill_name:
                skill = 3 * attacker.level
            else:
                skill = self._skill_percent(attacker, skill_name)
        return 20 + max(0, min(100, skill))

    def _thac0(self, attacker, dt: str, skill: int) -> int:
        level = max(0, GenericUtil.to_int(getattr(attacker, "level", 0), 0))
        if CharacterApi.is_npc(attacker):
            thac0_00 = 20
            thac0_32 = -4
            if self._mob_has_act(attacker, self.ActBits, self.ActBits.ACT_WARRIOR.name):
                thac0_32 = -10
            elif self._mob_has_act(attacker, self.ActBits, self.ActBits.ACT_THIEF.name):
                thac0_32 = -4
            elif self._mob_has_act(attacker, self.ActBits, self.ActBits.ACT_CLERIC.name):
                thac0_32 = 2
            elif self._mob_has_act(attacker, self.ActBits, self.ActBits.ACT_MAGE.name):
                thac0_32 = 6
        else:
            thac0_00 = GenericUtil.to_int(attacker.character_class.thac000, 20)
            thac0_32 = GenericUtil.to_int(attacker.character_class.thac032, -4)

        thac0 = FightUtil.interpolate(level, thac0_00, thac0_32)
        if thac0 < 0:
            thac0 //= 2
        if thac0 < -5:
            thac0 = -5 + (thac0 + 5) // 2

        thac0 -= self._current_hitroll(attacker) * skill // 100
        thac0 += 5 * (100 - skill) // 100

        if self._is_backstab_attack(dt):
            thac0 -= 10 * (100 - self._skill_percent(attacker, "backstab")) // 100
        return thac0

    @staticmethod
    def _victim_ac_for_damage_type(victim, dam_type: str) -> int:
        armor = getattr(victim, "armor_class", None)
        if armor is None:
            return 0

        category = FightUtil.normalize_damage_type_name(dam_type)
        if category == "DAM_PIERCE":
            base = getattr(armor, "piercing", getattr(armor, "pierce", 0))
        elif category == "DAM_BASH":
            base = getattr(armor, "bashing", getattr(armor, "bash", 0))
        elif category == "DAM_SLASH":
            base = getattr(armor, "slashing", getattr(armor, "slash", 0))
        else:
            base = getattr(armor, "magic", getattr(armor, "exotic", 0))

        stats = getattr(victim, "character_attributes", None)
        dexterity = stats.dexterity
        defensive = GenericUtil.to_int(
            CharacterApi.get_attribute_bonus("dexterity", str(dexterity)).get("defensive", 0), 0)
        return (GenericUtil.to_int(base, 0) + defensive) // 10

    def _to_hit_roll(self) -> int:
        roll = 20
        while roll >= 20:
            roll = self.rng.number_bits(5)
        return roll

    def _check_improve(self, attacker, skill_name: str, success: bool, multiplier: int) -> None:
        Ability.check_improve_by_name(attacker, skill_name, success, multiplier)

    def _current_hitroll(self, entity) -> int:
        return self._strength_combat_bonus(entity, "tohit") + FightUtil.dynamic_combat_bonus(entity, "hit_roll",
                                                                                             "hitroll")

    def _current_damroll(self, entity) -> int:
        return self._strength_combat_bonus(entity, "todam") + FightUtil.dynamic_combat_bonus(entity, "dam_roll",
                                                                                             "damroll")

    @staticmethod
    def _strength_combat_bonus(entity, key: str) -> int:
        stats = getattr(entity, "character_attributes", None) or getattr(entity, "character_attributes", None)
        strength = GenericUtil.to_int(getattr(stats, "strength", 0), 0)
        return GenericUtil.to_int(CharacterApi.get_attribute_bonus("strength", str(strength)).get(key, 0), 0)

    def _check_immunity(self, victim, dam_type: str) -> str:
        dam_type_name = FightUtil.normalize_damage_type_name(dam_type)
        if dam_type_name == "DAM_NONE":
            return "IS_NORMAL"

        imm_flags = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "imm", 0), 0)
        res_flags = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "res", 0), 0)
        vuln_flags = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "vuln", 0), 0)
        bit_suffix = dam_type_name.replace("DAM_", "")
        imm_bit = CharacterApi.enum_bit(self.MobImmunity, f"IMM_{bit_suffix}")
        res_bit = CharacterApi.enum_bit(self.MobResistance, f"RES_{bit_suffix}")
        vuln_bit = CharacterApi.enum_bit(self.MobVulnerability, f"VULN_{bit_suffix}")

        default = self._default_immunity_type(dam_type_name, imm_flags, res_flags, vuln_flags)
        immune = None
        if imm_bit > 0 and CharacterApi.is_set(imm_flags, imm_bit):
            immune = "IS_IMMUNE"
        elif res_bit > 0 and CharacterApi.is_set(res_flags, res_bit):
            immune = "IS_RESISTANT"

        if vuln_bit > 0 and CharacterApi.is_set(vuln_flags, vuln_bit):
            if immune == "IS_IMMUNE":
                immune = "IS_RESISTANT"
            elif immune == "IS_RESISTANT":
                immune = "IS_NORMAL"
            else:
                immune = "IS_VULNERABLE"

        return immune or default

    def _default_immunity_type(self, dam_type_name: str, imm_flags: int, res_flags: int, vuln_flags: int) -> str:
        if dam_type_name in ("DAM_BASH", "DAM_PIERCE", "DAM_SLASH"):
            if CharacterApi.is_set(imm_flags, self.MobImmunity.IMM_WEAPON.value):
                default = "IS_IMMUNE"
            elif CharacterApi.is_set(res_flags, self.MobResistance.RES_WEAPON.value):
                default = "IS_RESISTANT"
            elif CharacterApi.is_set(vuln_flags, self.MobVulnerability.VULN_WEAPON.value):
                default = "IS_VULNERABLE"
            else:
                default = "IS_NORMAL"
        else:
            if CharacterApi.is_set(imm_flags, self.MobImmunity.IMM_MAGIC.value):
                default = "IS_IMMUNE"
            elif CharacterApi.is_set(res_flags, self.MobResistance.RES_MAGIC.value):
                default = "IS_RESISTANT"
            elif CharacterApi.is_set(vuln_flags, self.MobVulnerability.VULN_MAGIC.value):
                default = "IS_VULNERABLE"
            else:
                default = "IS_NORMAL"
        return default

    def _set_default_combat_position(self, entity) -> None:
        if CharacterApi.is_npc(entity):
            default_pos = GenericUtil.to_int(getattr(entity, "default_pos", self.PositionsEnum.POS_STANDING.value),
                                             self.PositionsEnum.POS_STANDING.value)
            self._set_position(entity, default_pos)
        else:
            self._set_position(entity, self.PositionsEnum.POS_STANDING.value)
        self.update_pos(entity)

    def _restore_player_after_death(self, victim, room) -> None:
        temple_room = self.room_registry.get_or_none(vnum="3001")
        if room is not None:
            room.characters.pop(str(getattr(victim, "id", "") or ""), None)

        for effect in list(self.effect_handler.ensure_effects(victim)):
            self.effect_handler.remove_effect(victim, effect)

        armor = getattr(victim, "armor_class", None)
        for field_name in ("piercing", "bashing", "slashing", "magic"):
            if armor is not None and hasattr(armor, field_name):
                setattr(armor, field_name, 100)

        positions_enum = CharacterApi.get_enum("positions")
        if hasattr(positions_enum, "POS_RESTING"):
            self._set_position(victim, int(positions_enum.POS_RESTING.value))

        victim.hit = max(1, GenericUtil.to_int(getattr(victim, "hit", 0), 0))
        victim.mana = max(1, GenericUtil.to_int(getattr(victim, "mana", 0), 0))
        victim.movement = max(1, GenericUtil.to_int(getattr(victim, "movement", 0), 0))

        destination_room = temple_room or room
        if destination_room is not None:
            destination_room.add_player_to_room(victim)
            victim.room_id = destination_room.id
            victim.area_id = getattr(destination_room, "area_id", getattr(victim, "area_id", ""))

    @staticmethod
    def _error_payload():
        return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}
