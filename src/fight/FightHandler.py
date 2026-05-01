import random

from typing import List
from injector import inject

from area.RoomHelper import RoomHelper
from area.AreaRegistry import AreaRegistry
from area.RoomRegistry import RoomRegistry
from fight.CombatEvent import CombatEvent
from fight.CombatRegistry import CombatRegistry
from mobile import Mobile
from util.GenericUtil import GenericUtil
from game.RandomNumberGenerator import RandomNumberGenerator
from util.InfoUtil import InfoUtil
from mobile.MobileRegistry import MobileRegistry
from object.BodyForm import BodyForm
from object.BodyParts import BodyParts
from util.EffectUtil import EffectUtil
from object.ItemRegistry import ItemRegistry
from util.ItemUtil import ItemUtil
from util.ObjectUtil import ObjectUtils
from player.CharacterAdvancement import CharacterAdvancement
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from server.messaging.MessageBus import MessageBus


class FightHandler:
    @inject
    def __init__(
        self,
        message_bus: MessageBus,
        combat_registry: CombatRegistry,
        area_registry: AreaRegistry,
        room_registry: RoomRegistry,
        room_helper: RoomHelper,
        item_registry: ItemRegistry,
        mobile_registry: MobileRegistry,
    ):
        self.__name__ = "FightHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.message_bus = message_bus
        self.combat_registry = combat_registry
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.room_helper = room_helper
        self.item_registry = item_registry
        self.mobile_registry = mobile_registry
        self.rng = RandomNumberGenerator()
        self.PositionsEnum = None
        self.WellKnownObjectVnums = None
        self.OffenseTypes = None
        self.AffectBits = None
        self.mobile_handler = None
        self.logger.info("Initialized FightHandler instance.")

    def lazy_load(self):
        self.PositionsEnum = CharacterMacros.get_enum("positions")
        self.WellKnownObjectVnums = CharacterMacros.get_enum("wellKnownObjectVnums")
        self.OffenseTypes = CharacterMacros.get_enum("offenseTypes")
        self.AffectBits = CharacterMacros.get_enum("affectedBy")
        self.logger.info("Loaded FightHandler enums.")

    def set_mobile_handler(self, mobile_handler) -> None:
        self.mobile_handler = mobile_handler

    def get_combat_event_by_id(self, event_id: str) -> CombatEvent:
        return self.combat_registry.get_or_none(id=event_id)

    def get_combat_event_by_room(self, room_id: str) -> List[CombatEvent]:
        return self.combat_registry.get_by_room(room_id)

    @staticmethod
    def _entity_position_value(entity) -> int:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            return GenericUtil.to_int(getattr(attrs, "position", 0), 0)
        return GenericUtil.to_int(getattr(entity, "position", getattr(entity, "start_pos", 0)), 0)

    def is_safe(self, attacker, victim, room=None) -> tuple[bool, str]:
        if attacker is None or victim is None:
            return True, "You cannot attack that.\r\n"
        if attacker is victim:
            return True, "You hit yourself. Ouch!\r\n"

        if room is not None and not self._entity_in_room(room, victim):
            return True, "They aren't here.\r\n"
        if room is None and str(getattr(attacker, "room_id", "")) != str(getattr(victim, "room_id", "")):
            return True, "They aren't here.\r\n"

        if hasattr(self.PositionsEnum, "POS_DEAD"):
            if self._entity_position_value(victim) <= int(self.PositionsEnum.POS_DEAD.value):
                return True, "They are already dead.\r\n"

        room_flags = CharacterMacros.get_enum("roomFlags")
        if room is not None and hasattr(room_flags, "ROOM_SAFE"):
            if CharacterMacros.is_set(int(getattr(room, "room_flags", 0)), int(room_flags.ROOM_SAFE.value)):
                return True, "Not in this room.\r\n"

        if CharacterMacros.is_npc(victim):
            act_bits = CharacterMacros.get_enum("actBits")
            mob_act = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "act", 0), 0)
            protected_bits = ("ACT_TRAIN", "ACT_PRACTICE", "ACT_IS_HEALER", "ACT_IS_CHANGER")
            for bit_name in protected_bits:
                bit = CharacterMacros.enum_bit(act_bits, bit_name)
                if bit and CharacterMacros.is_set(mob_act, bit):
                    return True, "I don't think Mota would approve.\r\n"
            if not CharacterMacros.is_npc(attacker):
                pet_bit = CharacterMacros.enum_bit(act_bits, "ACT_PET")
                if pet_bit and CharacterMacros.is_set(mob_act, pet_bit):
                    return True, "But they look so cute and cuddly...\r\n"

        if getattr(victim, "fighting", None) is not None and getattr(victim, "fighting", None) is not attacker:
            return True, "Kill stealing is not permitted.\r\n"

        # Keep this permissive for now; detailed PK and charm rules migrate next.
        return False, ""

    def is_safe_spell(self, attacker, victim, area: bool = False) -> bool:
        safe, _ = self.is_safe(attacker, victim)
        return safe

    def check_killer(self, attacker, victim) -> None:
        # Placeholder for PLR_KILLER/PLR_THIEF semantics during deeper migration.
        return

    @staticmethod
    def check_parry(attacker, victim) -> bool:
        dex = GenericUtil.to_int(getattr(getattr(victim, "character_attributes", None), "dexterity", 10), 10)
        chance = max(0, min(25, dex // 2))
        return random.randint(1, 100) <= chance

    @staticmethod
    def check_shield_block(attacker, victim) -> bool:
        equipped = getattr(victim, "equipped", None)
        has_shield = equipped is not None and getattr(equipped, "shield", None) is not None
        if not has_shield:
            return False
        dex = GenericUtil.to_int(getattr(getattr(victim, "character_attributes", None), "dexterity", 10), 10)
        chance = max(0, min(20, dex // 2))
        return random.randint(1, 100) <= chance

    @staticmethod
    def check_dodge(attacker, victim) -> bool:
        dex = GenericUtil.to_int(getattr(getattr(victim, "character_attributes", None), "dexterity", 10), 10)
        chance = max(0, min(30, dex))
        return random.randint(1, 100) <= chance

    def update_pos(self, victim) -> None:
        hit = GenericUtil.to_int(getattr(victim, "hit", 0), 0)
        if hit > 0:
            return

        if hasattr(self.PositionsEnum, "POS_DEAD") and hit <= -11:
            self._set_position(victim, int(self.PositionsEnum.POS_DEAD.value))
            return
        if hasattr(self.PositionsEnum, "POS_MORTAL") and hit <= -6:
            self._set_position(victim, int(self.PositionsEnum.POS_MORTAL.value))
            return
        if hasattr(self.PositionsEnum, "POS_INCAP") and hit <= -3:
            self._set_position(victim, int(self.PositionsEnum.POS_INCAP.value))
            return
        if hasattr(self.PositionsEnum, "POS_STUNNED"):
            self._set_position(victim, int(self.PositionsEnum.POS_STUNNED.value))

    @staticmethod
    def _set_position(entity, position_value: int) -> None:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            attrs.position = position_value
            return
        setattr(entity, "position", position_value)

    def set_fighting(self, attacker, defender, room_id: str) -> CombatEvent | None:
        if attacker is None or defender is None:
            return None
        if getattr(attacker, "fighting", None) is not None:
            return None

        attacker.fighting = defender
        self._set_fighting_position(attacker)
        return self.combat_registry.upsert(getattr(attacker, "id", ""), getattr(defender, "id", ""), room_id)

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
        if character is None or room is None or CharacterMacros.is_npc(character) or CharacterMacros.is_immortal(character):
            return []

        area = self.area_registry.get_or_none(id=getattr(room, "area_id", ""))
        if area is not None and bool(getattr(area, "empty", False)):
            return []

        rounds: list[tuple[object, dict]] = []
        for aggressor in list(getattr(room, "mobiles", {}).values()):
            if aggressor is None or not self._should_aggress(aggressor, character, room):
                continue

            victim = self._select_aggressive_victim(aggressor, room)
            if victim is None:
                continue

            pre_corpse_ids = {
                str(getattr(item, "id", "") or "")
                for item in room.contents.values()
                if "corpse" in str(getattr(item, "item_type", "") or "").lower()
            }
            result = self.multi_hit(aggressor, victim, dt="TYPE_UNDEFINED")
            payload = self.build_round_payload(aggressor, victim, room, result, pre_corpse_ids)
            rounds.append((aggressor, payload))

        return rounds

    def aggressive_room_rounds(self, room) -> list[tuple[object, dict]]:
        if room is None:
            return []

        area = self.area_registry.get_or_none(id=getattr(room, "area_id", ""))
        if area is not None and bool(getattr(area, "empty", False)):
            return []

        rounds: list[tuple[object, dict]] = []
        for witness in room.characters.values():
            for aggressor in list(getattr(room, "mobiles", {}).values()):
                if aggressor is None:
                    continue
                if not self._should_aggress(aggressor, witness, room):
                    continue

                victim = self._select_aggressive_victim(aggressor, room)
                if victim is None:
                    continue

                pre_corpse_ids = {
                    str(getattr(item, "id", "") or "")
                    for item in room.contents.values()
                    if "corpse" in str(getattr(item, "item_type", "") or "").lower()
                }
                result = self.multi_hit(aggressor, victim, dt="TYPE_UNDEFINED")
                payload = self.build_round_payload(aggressor, victim, room, result, pre_corpse_ids)
                rounds.append((aggressor, payload))
        return rounds

    async def emit_round_payload(self, attacker, payload: dict) -> list:
        prompted: list = []
        if not isinstance(payload, dict):
            return prompted

        if payload.get("to_char") and not CharacterMacros.is_npc(attacker):
            await self.message_bus.send_to_character(attacker.id, self.message_bus.text_to_message(payload["to_char"]))
            prompted.append(attacker)
        if payload.get("to_victim") and payload.get("victim") is not None and not CharacterMacros.is_npc(payload["victim"]):
            await self.message_bus.send_to_character(payload["victim"].id, self.message_bus.text_to_message(payload["to_victim"]))
            prompted.append(payload["victim"])
        if payload.get("to_room"):
            targets = payload.get("targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)
        return prompted

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
        if victim is None:
            return

        room = self._find_room_for_entity(victim)
        self.stop_fighting(victim, both=True)

        if room is not None:
            self.death_cry(victim, room)
            self.make_corpse(victim, room)

        if CharacterMacros.is_npc(victim):
            if room is not None:
                room.mobiles.pop(str(getattr(victim, "id", "") or ""), None)

            proto = self.mobile_registry.get_or_none(vnum=str(getattr(victim, "vnum", "") or ""))
            if proto is not None:
                proto.killed = GenericUtil.to_int(getattr(proto, "killed", 0), 0) + 1
            if self.mobile_handler is not None:
                self.mobile_handler.record_mobile_kill(victim)
            return

        self._restore_player_after_death(victim, room)

    def death_cry(self, victim, room) -> None:
        if victim is None or room is None:
            return

        parts = self._entity_parts(victim)
        roll = random.randint(0, 15)
        body_part_vnum = None

        if roll == 2 and CharacterMacros.is_set(parts, int(BodyParts.PART_GUTS.value)):
            body_part_vnum = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_GUTS", None)
        elif roll == 3 and CharacterMacros.is_set(parts, int(BodyParts.PART_HEAD.value)):
            body_part_vnum = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_SEVERED_HEAD", None)
        elif roll == 4 and CharacterMacros.is_set(parts, int(BodyParts.PART_HEART.value)):
            body_part_vnum = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_TORN_HEART", None)
        elif roll == 5 and CharacterMacros.is_set(parts, int(BodyParts.PART_ARMS.value)):
            body_part_vnum = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_SLICED_ARM", None)
        elif roll == 6 and CharacterMacros.is_set(parts, int(BodyParts.PART_LEGS.value)):
            body_part_vnum = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_SLICED_LEG", None)
        elif roll == 7 and CharacterMacros.is_set(parts, int(BodyParts.PART_BRAINS.value)):
            body_part_vnum = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_BRAINS", None)

        if body_part_vnum is None:
            return

        proto = self.item_registry.get_or_none(vnum=str(int(body_part_vnum.value)))
        if proto is None:
            return

        part_item = ItemUtil.create_object(proto)
        part_item.timer = random.randint(4, 7)

        victim_name = self._corpse_name(victim)
        part_item.short_description = self._format_template(getattr(part_item, "short_description", ""), victim_name)
        part_item.long_description = self._format_template(getattr(part_item, "long_description", ""), victim_name)

        item_type = str(getattr(part_item, "item_type", "") or "").lower()
        form = self._entity_form(victim)
        if "food" in item_type:
            if CharacterMacros.is_set(form, int(BodyForm.FORM_POISON.value)):
                part_item.value3 = "1"
            elif not CharacterMacros.is_set(form, int(BodyForm.FORM_EDIBLE.value)):
                part_item.item_type = "trash"

        room.add_item_to_room(part_item)

    def make_corpse(self, victim, room) -> None:
        if victim is None or room is None:
            return

        money = None
        if CharacterMacros.is_npc(victim):
            corpse_vnum_member = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_CORPSE_NPC", None)
            timer_min, timer_max = 3, 6
            if victim.gold > 0:
                money = ItemUtil.create_money(victim.gold, victim.silver, self.item_registry, self.WellKnownObjectVnums)
                victim.gold = 0
                victim.silver = 0
        else:
            corpse_vnum_member = getattr(self.WellKnownObjectVnums, "OBJ_VNUM_CORPSE_PC", None)
            if victim.gold > 1 or victim.silver > 1:
                money = ItemUtil.create_money(victim.gold, victim.silver, self.item_registry, self.WellKnownObjectVnums)
                victim.gold -= victim.gold / 2
                victim.silver -= victim.silver / 2
            timer_min, timer_max = 25, 40

        if corpse_vnum_member is None:
            return

        corpse_proto = self.item_registry.get_or_none(vnum=str(int(corpse_vnum_member.value)))
        if corpse_proto is None:
            return

        corpse = ItemUtil.create_object(corpse_proto)
        corpse.timer = random.randint(timer_min, timer_max)
        corpse.level = GenericUtil.to_int(getattr(victim, "level", 0), 0)
        corpse.cost = 0

        victim_name = self._corpse_name(victim)
        corpse.short_description = self._format_template(getattr(corpse, "short_description", ""), victim_name)
        corpse.long_description = self._format_template(getattr(corpse, "long_description", ""), victim_name)

        for item in self._extract_owned_items(victim):
            self._prepare_loot_item(item)
            if self._is_floating_item(item):
                room.add_item_to_room(item)
            else:
                corpse.contains.append(item)

        if money is not None:
            corpse.contains.append(money)
        room.add_item_to_room(corpse)

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
        gch_align = self._get_alignment(gch)
        victim_align = self._get_alignment(victim)
        align = victim_align - gch_align

        act_bits = CharacterMacros.get_enum("actBits")
        no_align_bit = CharacterMacros.enum_bit(act_bits, "ACT_NOALIGN")
        victim_act = GenericUtil.to_int(getattr(getattr(victim, "status_flags", None), "act", 0), 0)
        no_align = no_align_bit > 0 and CharacterMacros.is_set(victim_act, no_align_bit)

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
            self._set_alignment(gch, gch_align)

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

    def damage(self, attacker, victim, dam: int, dt: str = "TYPE_HIT", dam_type: str = "NONE", show: bool = True) -> dict:
        if victim is None:
            return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        if attacker is not None and victim is not attacker:
            positions_enum = CharacterMacros.get_enum("positions")
            pos_stunned = int(getattr(positions_enum, "POS_STUNNED").value) if hasattr(positions_enum, "POS_STUNNED") else -1

            if self._entity_position_value(victim) > pos_stunned and getattr(victim, "fighting", None) is None:
                room = self._find_room_for_entity(victim)
                if room is not None:
                    self.set_fighting(victim, attacker, room.id)
            if self._entity_position_value(victim) > pos_stunned and getattr(attacker, "fighting", None) is None:
                room = self._find_room_for_entity(attacker) or self._find_room_for_entity(victim)
                if room is not None:
                    self.set_fighting(attacker, victim, room.id)

        original_hit = GenericUtil.to_int(getattr(victim, "hit", 0), 0)
        applied = max(0, GenericUtil.to_int(dam, 0))
        setattr(victim, "hit", original_hit - applied)
        self.update_pos(victim)

        killed = False
        xp_gain = 0
        advancement = None
        positions_enum = CharacterMacros.get_enum("positions")
        if hasattr(positions_enum, "POS_DEAD"):
            if self._entity_position_value(victim) <= int(positions_enum.POS_DEAD.value):
                killed = True
                xp_gain = 0
                if attacker is not None and not CharacterMacros.is_npc(attacker) and CharacterMacros.is_npc(victim):
                    attacker_level = max(1, GenericUtil.to_int(getattr(attacker, "level", 1), 1))
                    xp_gain = self.xp_compute(attacker, victim, attacker_level)
                    advancement = CharacterAdvancement.gain_experience(attacker, xp_gain)
                self.raw_kill(victim)

        msg = self.dam_message(attacker, victim, applied, dt=dt, immune=False)
        msg["killed"] = killed
        msg["xp_gain"] = xp_gain if killed else 0
        msg["level_up_messages"] = advancement.level_up_messages if advancement is not None else ""
        return msg

    def one_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        if attacker is None or victim is None:
            return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}
        if victim is attacker:
            return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        positions_enum = CharacterMacros.get_enum("positions")
        if hasattr(positions_enum, "POS_DEAD"):
            if self._entity_position_value(victim) <= int(positions_enum.POS_DEAD.value):
                return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        attacker_room = self._find_room_for_entity(attacker)
        victim_room = self._find_room_for_entity(victim)
        if attacker_room is None or victim_room is None or str(attacker_room.id) != str(victim_room.id):
            return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        attack_verb = self._attack_verb(attacker, dt)
        if self.check_dodge(attacker, victim) or self.check_parry(attacker, victim) or self.check_shield_block(attacker, victim):
            return self.damage(attacker, victim, 0, dt=attack_verb)

        dam = self._attack_damage(attacker)
        return self.damage(attacker, victim, dam, dt=attack_verb)

    def mob_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        payload = self.one_hit(attacker, victim, dt=dt)

        if getattr(attacker, "fighting", None) is not victim:
            return payload

        room = self._find_room_for_entity(attacker)
        if room is not None and self._mob_has_off(attacker, "OFF_AREA_ATTACK"):
            for entity in self._entities_in_room(room):
                if entity is victim:
                    continue
                if getattr(entity, "fighting", None) is attacker:
                    payload = self._merge_attack_payloads(payload, self.one_hit(attacker, entity, dt=dt))

        if self._entity_has_affect(attacker, "AFF_HASTE") or (
            self._mob_has_off(attacker, "OFF_FAST") and not self._entity_has_affect(attacker, "AFF_SLOW")
        ):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        if getattr(attacker, "fighting", None) is not victim or self._is_backstab_attack(dt):
            return payload

        chance = self._skill_percent(attacker, "second attack") // 2
        if self._entity_has_affect(attacker, "AFF_SLOW") and not self._mob_has_off(attacker, "OFF_FAST"):
            chance //= 2
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))
            if getattr(attacker, "fighting", None) is not victim:
                return payload

        chance = self._skill_percent(attacker, "third attack") // 4
        if self._entity_has_affect(attacker, "AFF_SLOW") and not self._mob_has_off(attacker, "OFF_FAST"):
            chance = 0
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        return payload

    def multi_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        if attacker is None or victim is None:
            return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        self._decrement_combat_timers(attacker)
        positions_enum = CharacterMacros.get_enum("positions")
        if hasattr(positions_enum, "POS_RESTING"):
            if self._entity_position_value(attacker) < int(positions_enum.POS_RESTING.value):
                return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        if CharacterMacros.is_npc(attacker):
            return self.mob_hit(attacker, victim, dt=dt)

        payload = self.one_hit(attacker, victim, dt=dt)
        if getattr(attacker, "fighting", None) is not victim:
            return payload

        if self._entity_has_affect(attacker, "AFF_HASTE"):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        if getattr(attacker, "fighting", None) is not victim or self._is_backstab_attack(dt):
            return payload

        chance = self._skill_percent(attacker, "second attack") // 2
        if self._entity_has_affect(attacker, "AFF_SLOW"):
            chance //= 2
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))
            if getattr(attacker, "fighting", None) is not victim:
                return payload

        chance = self._skill_percent(attacker, "third attack") // 4
        if self._entity_has_affect(attacker, "AFF_SLOW"):
            chance = 0
        if random.randint(1, 100) < max(0, chance):
            payload = self._merge_attack_payloads(payload, self.one_hit(attacker, victim, dt=dt))

        return payload

    # TO-DO
    def check_assist(self, attacker, victim) -> None:
        room = self.room_registry.get(id=attacker.room_id)
        for char in room.people():
            if (not CharacterMacros.is_npc(attacker) and
                    CharacterMacros.is_npc(char) and
                    CharacterMacros.mobile_will_assist(char) and
                    char.level + 6 > victim.level):
                # questionable TO-DO: do_function->do_emote
                self.message_bus.send_to_room(self.message_bus.text_to_message(f"{char.name} screams and attacks!"), room.players_in_room())
                self.multi_hit(char, victim, dt="TYPE_UNDEFINED")
                continue
            if (not CharacterMacros.is_npc(attacker) or
                    CharacterMacros.is_affected(attacker, self.AffectBits.AFF_CHARM.value)):

                if ((not CharacterMacros.is_npc(char) and CharacterMacros.player_auto_assist(char)) or
                    CharacterMacros.is_affected(char, self.AffectBits.AFF_CHARM.value)) and \
                        CharacterMacros.is_same_group(attacker, char) and \
                        not self.is_safe(char, victim):
                    self.multi_hit(char, victim, dt="TYPE_UNDEFINED")
                continue
        return

    def build_round_payload(self, attacker, victim, room, result: dict, pre_corpse_ids=None) -> dict:
        attacker_id = str(getattr(attacker, "id", "") or "")
        victim_id = str(getattr(victim, "id", "") or "")
        payload = {
            "to_char": result.get("to_char", ""),
            "to_room": result.get("to_room", ""),
            "targets": [ch for ch in room.characters.values() if ch.id not in (attacker_id, victim_id)],
        }

        if not CharacterMacros.is_npc(victim):
            payload["victim"] = victim
            payload["to_victim"] = result.get("to_victim", "")

        if not result.get("killed"):
            if not CharacterMacros.is_npc(attacker) and CharacterMacros.is_npc(victim):
                payload["to_char"] = self._append_condition_line(payload["to_char"], victim)
            elif CharacterMacros.is_npc(attacker) and not CharacterMacros.is_npc(victim):
                payload["to_victim"] = self._append_condition_line(payload.get("to_victim", ""), attacker)

        if not result.get("killed"):
            return payload

        if not CharacterMacros.is_npc(attacker):
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
                if not (self._player_act_enabled(attacker, "PLR_AUTOLOOT") and list(getattr(corpse, "contains", []) or [])):
                    sacrifice = self._autosacrifice_corpse(attacker, corpse, room)
                    if sacrifice is not None:
                        payload["to_char"] = (payload["to_char"] or "") + sacrifice.get("to_char", "")
                        payload["to_room"] = (payload["to_room"] or "") + sacrifice.get("to_room", "")

        return payload

    def _find_room_for_entity(self, entity):
        entity_id = str(getattr(entity, "id", "") or "")
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
        if CharacterMacros.is_npc(entity):
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
        if CharacterMacros.is_npc(entity):
            form = getattr(getattr(entity, "status_flags", None), "form", None)
            if form is None:
                form = getattr(entity, "form", 0)
            return GenericUtil.to_int(form, 0)

        return int(
            BodyForm.FORM_EDIBLE
            | BodyForm.FORM_SENTIENT
            | BodyForm.FORM_BIPED
            | BodyForm.FORM_MAMMAL
        )

    def _entity_parts(self, entity) -> int:
        if CharacterMacros.is_npc(entity):
            parts = getattr(getattr(entity, "status_flags", None), "parts", None)
            if parts is None:
                parts = getattr(entity, "parts", 0)
            return GenericUtil.to_int(parts, 0)

        return int(
            BodyParts.PART_HEAD
            | BodyParts.PART_ARMS
            | BodyParts.PART_LEGS
            | BodyParts.PART_HEART
            | BodyParts.PART_BRAINS
            | BodyParts.PART_GUTS
            | BodyParts.PART_HANDS
            | BodyParts.PART_FEET
            | BodyParts.PART_FINGERS
            | BodyParts.PART_EAR
            | BodyParts.PART_EYE
        )

    def _extract_owned_items(self, entity) -> list:
        items: list = []
        seen = set()

        bag_attr = "inventory" if CharacterMacros.is_npc(entity) else "loot"
        bag = getattr(entity, bag_attr, None)
        if bag is None:
            bag = []

        for item in list(bag):
            if item is None:
                continue
            key = id(item)
            if key in seen:
                continue
            seen.add(key)
            items.append(item)
            if item in bag:
                bag.remove(item)

        equipped = getattr(entity, "equipped", None)
        for slot, item in getattr(equipped, "__dict__", {}).items() if equipped is not None else []:
            if item is None:
                continue
            key = id(item)
            if key not in seen:
                seen.add(key)
                items.append(item)
            setattr(equipped, slot, None)

        return items

    @staticmethod
    def _is_floating_item(item) -> bool:
        wear_location_enum = CharacterMacros.get_enum("wearLocation")
        wear_float = CharacterMacros.enum_bit(wear_location_enum, "WEAR_FLOAT")

        wear_loc = GenericUtil.to_int(getattr(item, "wear_loc", -1), -1)
        if wear_float > 0 and wear_loc == wear_float:
            return True

        wear_location = str(getattr(item, "wear_location", "") or "").strip().upper()
        if wear_location == "WEAR_FLOAT":
            return True

        return False

    @staticmethod
    def _get_alignment(entity) -> int:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            return GenericUtil.to_int(getattr(attrs, "alignment", 0), 0)
        perm = getattr(entity, "perm_stat", None)
        if perm is not None:
            return GenericUtil.to_int(getattr(perm, "alignment", 0), 0)
        return GenericUtil.to_int(getattr(entity, "alignment", 0), 0)

    @staticmethod
    def _set_alignment(entity, value: int) -> None:
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            attrs.alignment = int(value)
            return
        perm = getattr(entity, "perm_stat", None)
        if perm is not None:
            perm.alignment = int(value)
            return
        setattr(entity, "alignment", int(value))

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

    @staticmethod
    def _player_act_enabled(character, flag_name: str) -> bool:
        if CharacterMacros.is_npc(character):
            return False
        player_bits = CharacterMacros.get_enum("playerActBits")
        bit = CharacterMacros.enum_bit(player_bits, flag_name)
        if bit <= 0:
            return False
        return CharacterMacros.is_set(CharacterMacros.get_act_flags(character), bit)

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
        if CharacterMacros.is_npc(target):
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
        merged["xp_gain"] = GenericUtil.to_int(merged.get("xp_gain", 0), 0) + GenericUtil.to_int(extra.get("xp_gain", 0), 0)
        return merged

    @staticmethod
    def _autoloot_corpse(character, corpse) -> None:
        try:
            wear_flags = CharacterMacros.get_enum("wearFlags")
        except RuntimeError:
            wear_flags = None

        remaining = []
        for item in list(getattr(corpse, "contains", []) or []):
            if ObjectUtils.item_takeable(item, wear_flags):
                ObjectUtils.add_to_inventory(character, item)
            else:
                remaining.append(item)
        corpse.contains = remaining

    @staticmethod
    def _autosacrifice_corpse(attacker, corpse, room) -> dict | None:
        if room is None or corpse is None or not ObjectUtils.is_npc_corpse(corpse):
            return None

        try:
            wear_flags = CharacterMacros.get_enum("wearFlags")
            item_flags = CharacterMacros.get_enum("itemFlags")
        except RuntimeError:
            wear_flags = None
            item_flags = None

        if not ObjectUtils.item_takeable(corpse, wear_flags) or ObjectUtils.is_nosac(corpse, item_flags):
            return None

        room.remove_item_from_room(corpse)
        silver = ObjectUtils.sacrifice_silver_value(corpse)
        attacker.silver = int(getattr(attacker, "silver", 0) or 0) + silver
        return {
            "to_char": ObjectUtils.sacrifice_reward_message(silver),
            "to_room": f"{attacker.name} sacrifices {ObjectUtils.short(corpse)} to Mota.\r\n",
        }

    @staticmethod
    def _is_backstab_attack(dt: str) -> bool:
        text = str(dt or "").strip().lower()
        return text == "backstab" or text == "gsn_backstab"

    @staticmethod
    def _entities_in_room(room) -> list:
        entities = []
        entities.extend(list(getattr(room, "characters", {}).values()))
        entities.extend(list(getattr(room, "mobiles", {}).values()))
        return entities

    @staticmethod
    def _decrement_combat_timers(entity) -> None:
        if CharacterMacros.is_npc(entity):
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

    @staticmethod
    def _entity_has_affect(entity, affect_name: str) -> bool:
        try:
            affect_bits = CharacterMacros.get_enum("affectedBy")
        except RuntimeError:
            return False
        bit = CharacterMacros.enum_bit(affect_bits, affect_name)
        if bit <= 0:
            return False
        return CharacterMacros.is_affected(entity, bit)

    @staticmethod
    def _mob_has_off(entity, off_name: str) -> bool:
        try:
            off_bits = CharacterMacros.get_enum("offenseTypes")
        except RuntimeError:
            return False
        bit = CharacterMacros.enum_bit(off_bits, off_name)
        if bit <= 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(entity, "status_flags", None), "off", 0), 0)
        return CharacterMacros.is_set(flags, bit)

    def _skill_percent(self, entity, skill_name: str) -> int:
        wanted = str(skill_name or "").strip().lower()
        if not wanted:
            return 0

        if not CharacterMacros.is_npc(entity):
            for skill in list(getattr(entity, "skills", []) or []):
                name = str(skill.get("name", "") or "").strip().lower()
                if name == wanted:
                    return max(0, min(100, GenericUtil.to_int(skill.get("level", 0), 0)))
            return 0

        level = max(0, GenericUtil.to_int(getattr(entity, "level", 0), 0))
        act_bits = CharacterMacros.get_enum("actBits")
        if wanted == "second attack":
            is_warrior = self._mob_has_act(entity, act_bits, "ACT_WARRIOR")
            is_thief = self._mob_has_act(entity, act_bits, "ACT_THIEF")
            return max(0, min(100, 10 + 3 * level)) if (is_warrior or is_thief) else 0
        if wanted == "third attack":
            return max(0, min(100, 4 * level - 40)) if self._mob_has_act(entity, act_bits, "ACT_WARRIOR") else 0
        return 0

    @staticmethod
    def _mob_has_act(entity, act_bits, act_name: str) -> bool:
        bit = CharacterMacros.enum_bit(act_bits, act_name)
        if bit <= 0:
            return False
        flags = GenericUtil.to_int(getattr(getattr(entity, "status_flags", None), "act", 0), 0)
        return CharacterMacros.is_set(flags, bit)

    def _should_aggress(self, aggressor, witness, room) -> bool:
        if aggressor is None or witness is None or room is None:
            return False
        if not CharacterMacros.is_npc(aggressor):
            return False

        act_bits = CharacterMacros.get_enum("actBits")
        room_flags = CharacterMacros.get_enum("roomFlags")
        mob_act = GenericUtil.to_int(getattr(getattr(aggressor, "status_flags", None), "act", 0), 0)
        room_bits = GenericUtil.to_int(getattr(room, "room_flags", 0), 0)

        if not self._mob_has_act(aggressor, act_bits, "ACT_AGGRESSIVE"):
            return False
        if CharacterMacros.enum_bit(room_flags, "ROOM_SAFE") and CharacterMacros.is_set(room_bits, CharacterMacros.enum_bit(room_flags, "ROOM_SAFE")):
            return False
        if self._entity_has_affect(aggressor, "AFF_CALM"):
            return False
        if getattr(aggressor, "fighting", None) is not None:
            return False
        if CharacterMacros.mobile_is_charmed(aggressor):
            return False
        if not CharacterMacros.is_awake(aggressor):
            return False
        if self._mob_has_act(aggressor, act_bits, "ACT_WIMPY") and CharacterMacros.is_awake(witness):
            return False
        if not CharacterMacros.can_see(aggressor, witness, self.room_helper):
            return False
        if self.rng.number_bits(1) == 0:
            return False
        return True

    def _select_aggressive_victim(self, aggressor, room):
        if aggressor is None or room is None:
            return None

        act_bits = CharacterMacros.get_enum("actBits")
        victim = None
        count = 0
        for candidate in list(getattr(room, "characters", {}).values()):
            if CharacterMacros.is_npc(candidate):
                continue
            if CharacterMacros.is_immortal(candidate):
                continue
            if GenericUtil.to_int(getattr(aggressor, "level", 0), 0) < GenericUtil.to_int(getattr(candidate, "level", 0), 0) - 5:
                continue
            if self._mob_has_act(aggressor, act_bits, "ACT_WIMPY") and CharacterMacros.is_awake(candidate):
                continue
            if not CharacterMacros.can_see(aggressor, candidate, self.room_helper):
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

    def _attack_verb(self, attacker, dt: str) -> str:
        raw_dt = str(dt or "").strip()
        if raw_dt and raw_dt not in ("TYPE_HIT", "TYPE_UNDEFINED"):
            return raw_dt

        weapon = self._wielded_weapon(attacker)
        if weapon is not None:
            verb = str(getattr(weapon, "value3", "") or "").strip().lower()
            if verb and verb != "0":
                return verb

        dam_type = str(getattr(attacker, "dam_type", "") or "").strip().lower()
        if dam_type and dam_type not in ("none", "0"):
            return dam_type
        return "punch"

    def _attack_damage(self, attacker) -> int:
        weapon = self._wielded_weapon(attacker)
        if weapon is not None:
            dice_count = max(1, GenericUtil.to_int(getattr(weapon, "value1", 1), 1))
            dice_size = max(1, GenericUtil.to_int(getattr(weapon, "value2", 1), 1))
            dam = sum(random.randint(1, dice_size) for _ in range(dice_count))
            strength = GenericUtil.to_int(getattr(getattr(attacker, "character_attributes", None), "strength", 10), 10)
            bonus = max(0, (strength - 10) // 4)
            return max(1, dam + bonus)

        level = GenericUtil.to_int(getattr(attacker, "level", 1), 1)
        strength = GenericUtil.to_int(getattr(getattr(attacker, "character_attributes", None), "strength", 10), 10)
        base = max(1, level // 2)
        bonus = max(0, (strength - 10) // 2)
        return random.randint(base, base + 4 + bonus)

    @staticmethod
    def _set_fighting_position(entity) -> None:
        positions_enum = CharacterMacros.get_enum("positions")
        if not hasattr(positions_enum, "POS_FIGHTING"):
            return
        fight_pos = int(positions_enum.POS_FIGHTING.value)
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            attrs.position = fight_pos
            return
        setattr(entity, "position", fight_pos)

    def _set_default_combat_position(self, entity) -> None:
        positions_enum = CharacterMacros.get_enum("positions")
        stand_pos = int(getattr(positions_enum, "POS_STANDING").value) if hasattr(positions_enum, "POS_STANDING") else 0
        if CharacterMacros.is_npc(entity):
            default_pos = GenericUtil.to_int(getattr(entity, "default_pos", stand_pos), stand_pos)
            self._set_position(entity, default_pos)
        else:
            self._set_position(entity, stand_pos)
        self.update_pos(entity)

    def _restore_player_after_death(self, victim, room) -> None:
        temple_room = self.room_registry.get_or_none(vnum="3001")
        if room is not None:
            room.characters.pop(str(getattr(victim, "id", "") or ""), None)

        for effect in list(EffectUtil.ensure_effects(victim)):
            EffectUtil.affect_remove(victim, effect)

        armor = getattr(victim, "armor_class", None)
        for field_name in ("piercing", "bashing", "slashing", "magic"):
            if armor is not None and hasattr(armor, field_name):
                setattr(armor, field_name, 100)

        positions_enum = CharacterMacros.get_enum("positions")
        if positions_enum is not None and hasattr(positions_enum, "POS_RESTING"):
            self._set_position(victim, int(positions_enum.POS_RESTING.value))

        victim.hit = max(1, GenericUtil.to_int(getattr(victim, "hit", 0), 0))
        victim.mana = max(1, GenericUtil.to_int(getattr(victim, "mana", 0), 0))
        victim.movement = max(1, GenericUtil.to_int(getattr(victim, "movement", 0), 0))

        destination_room = temple_room or room
        if destination_room is not None:
            destination_room.add_player_to_room(victim)
            victim.room_id = destination_room.id
            victim.area_id = getattr(destination_room, "area_id", getattr(victim, "area_id", ""))
