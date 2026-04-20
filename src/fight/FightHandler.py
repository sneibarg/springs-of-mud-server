import random

from typing import List
from injector import inject

from area.RoomRegistry import RoomRegistry
from fight.CombatEvent import CombatEvent
from fight.CombatRegistry import CombatRegistry
from game.GenericUtil import GenericUtil
from mobile.MobileRegistry import MobileRegistry
from object.BodyForm import BodyForm
from object.BodyParts import BodyParts
from object.ItemRegistry import ItemRegistry
from object.ItemUtil import ItemUtil
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory
from server.messaging.MessageBus import MessageBus


class FightHandler:
    @inject
    def __init__(
        self,
        message_bus: MessageBus,
        combat_registry: CombatRegistry,
        room_registry: RoomRegistry,
        item_registry: ItemRegistry,
        mobile_registry: MobileRegistry,
    ):
        self.__name__ = "FightHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.message_bus = message_bus
        self.combat_registry = combat_registry
        self.room_registry = room_registry
        self.item_registry = item_registry
        self.mobile_registry = mobile_registry
        self.logger.info("Initialized FightHandler instance.")

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

        # Explicit enum usage for clarity.
        positions_enum = CharacterMacros.get_enum("positions")
        if hasattr(positions_enum, "POS_DEAD"):
            if self._entity_position_value(victim) <= int(positions_enum.POS_DEAD.value):
                return True, "They are already dead.\r\n"

        room_flags = CharacterMacros.get_enum("roomFlags")
        if room is not None and hasattr(room_flags, "ROOM_SAFE"):
            if CharacterMacros.is_set(int(getattr(room, "room_flags", 0)), int(room_flags.ROOM_SAFE.value)):
                return True, "Not in this room.\r\n"

        if CharacterMacros.is_npc(victim):
            act_bits = CharacterMacros.get_enum("actBits")
            mob_act = GenericUtil.to_int(getattr(getattr(victim, "mobile_flags", None), "act", 0), 0)
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
        positions_enum = CharacterMacros.get_enum("positions")
        hit = GenericUtil.to_int(getattr(victim, "hit", 0), 0)
        if hit > 0:
            return

        if hasattr(positions_enum, "POS_DEAD") and hit <= -11:
            self._set_position(victim, int(positions_enum.POS_DEAD.value))
            return
        if hasattr(positions_enum, "POS_MORTAL") and hit <= -6:
            self._set_position(victim, int(positions_enum.POS_MORTAL.value))
            return
        if hasattr(positions_enum, "POS_INCAP") and hit <= -3:
            self._set_position(victim, int(positions_enum.POS_INCAP.value))
            return
        if hasattr(positions_enum, "POS_STUNNED"):
            self._set_position(victim, int(positions_enum.POS_STUNNED.value))

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

        counterpart = getattr(combatant, "fighting", None)
        combatant.fighting = None
        self._set_standing_position(combatant)
        self.combat_registry.remove_by_combatant(getattr(combatant, "id", ""))

        if both and counterpart is not None and getattr(counterpart, "fighting", None) is combatant:
            counterpart.fighting = None
            self._set_standing_position(counterpart)
            self.combat_registry.remove_by_combatant(getattr(counterpart, "id", ""))

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
        attacker_name = getattr(attacker, "name", "Someone")
        victim_name = getattr(victim, "name", "someone")
        if CharacterMacros.is_npc(victim):
            victim_name = getattr(victim, "short_description", victim_name)

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

        return {"to_char": to_char, "to_victim": to_victim, "to_room": to_room}

    def raw_kill(self, victim) -> None:
        if victim is None:
            return

        room = self._find_room_for_entity(victim)
        self.stop_fighting(victim, both=True)

        positions_enum = CharacterMacros.get_enum("positions")
        if positions_enum is not None and hasattr(positions_enum, "POS_DEAD"):
            self._set_position(victim, int(positions_enum.POS_DEAD.value))

        if room is not None:
            self.death_cry(victim, room)
            self.make_corpse(victim, room)

        if CharacterMacros.is_npc(victim):
            if room is not None:
                room.mobiles.pop(str(getattr(victim, "id", "") or ""), None)

            proto = self.mobile_registry.get_or_none(vnum=str(getattr(victim, "vnum", "") or ""))
            if proto is not None:
                proto.count = max(0, GenericUtil.to_int(getattr(proto, "count", 0), 0) - 1)

    def death_cry(self, victim, room) -> None:
        if victim is None or room is None:
            return

        well_known = CharacterMacros.get_enum("wellKnownObjectVnums")
        parts = self._entity_parts(victim)
        roll = random.randint(0, 15)
        body_part_vnum = None

        if roll == 2 and CharacterMacros.is_set(parts, int(BodyParts.PART_GUTS.value)):
            body_part_vnum = getattr(well_known, "OBJ_VNUM_GUTS", None)
        elif roll == 3 and CharacterMacros.is_set(parts, int(BodyParts.PART_HEAD.value)):
            body_part_vnum = getattr(well_known, "OBJ_VNUM_SEVERED_HEAD", None)
        elif roll == 4 and CharacterMacros.is_set(parts, int(BodyParts.PART_HEART.value)):
            body_part_vnum = getattr(well_known, "OBJ_VNUM_TORN_HEART", None)
        elif roll == 5 and CharacterMacros.is_set(parts, int(BodyParts.PART_ARMS.value)):
            body_part_vnum = getattr(well_known, "OBJ_VNUM_SLICED_ARM", None)
        elif roll == 6 and CharacterMacros.is_set(parts, int(BodyParts.PART_LEGS.value)):
            body_part_vnum = getattr(well_known, "OBJ_VNUM_SLICED_LEG", None)
        elif roll == 7 and CharacterMacros.is_set(parts, int(BodyParts.PART_BRAINS.value)):
            body_part_vnum = getattr(well_known, "OBJ_VNUM_BRAINS", None)

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

        well_known = CharacterMacros.get_enum("wellKnownObjectVnums")
        if CharacterMacros.is_npc(victim):
            corpse_vnum_member = getattr(well_known, "OBJ_VNUM_CORPSE_NPC", None)
            timer_min, timer_max = 3, 6
        else:
            corpse_vnum_member = getattr(well_known, "OBJ_VNUM_CORPSE_PC", None)
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
        victim_act = GenericUtil.to_int(getattr(getattr(victim, "mobile_flags", None), "act", 0), 0)
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

        original_hit = GenericUtil.to_int(getattr(victim, "hit", 0), 0)
        applied = max(0, GenericUtil.to_int(dam, 0))
        setattr(victim, "hit", original_hit - applied)
        self.update_pos(victim)

        killed = False
        xp_gain = 0
        positions_enum = CharacterMacros.get_enum("positions")
        if hasattr(positions_enum, "POS_DEAD"):
            if self._entity_position_value(victim) <= int(positions_enum.POS_DEAD.value):
                killed = True
                xp_gain = 0
                if attacker is not None and not CharacterMacros.is_npc(attacker) and CharacterMacros.is_npc(victim):
                    attacker_level = max(1, GenericUtil.to_int(getattr(attacker, "level", 1), 1))
                    xp_gain = self.xp_compute(attacker, victim, attacker_level)
                    attacker.experience = GenericUtil.to_int(getattr(attacker, "experience", 0), 0) + xp_gain
                self.raw_kill(victim)

        msg = self.dam_message(attacker, victim, applied, dt=dt, immune=False)
        msg["killed"] = killed
        msg["xp_gain"] = xp_gain if killed else 0
        return msg

    def one_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        if attacker is None or victim is None:
            return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        if self.check_dodge(attacker, victim) or self.check_parry(attacker, victim) or self.check_shield_block(attacker, victim):
            return self.damage(attacker, victim, 0, dt=dt)

        level = GenericUtil.to_int(getattr(attacker, "level", 1), 1)
        strength = GenericUtil.to_int(getattr(getattr(attacker, "character_attributes", None), "strength", 10), 10)
        base = max(1, level // 2)
        bonus = max(0, (strength - 10) // 2)
        dam = random.randint(base, base + 4 + bonus)
        return self.damage(attacker, victim, dam, dt=dt)

    def mob_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        return self.one_hit(attacker, victim, dt=dt)

    def multi_hit(self, attacker, victim, dt: str = "TYPE_HIT") -> dict:
        if attacker is None or victim is None:
            return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        positions_enum = CharacterMacros.get_enum("positions")
        if hasattr(positions_enum, "POS_RESTING"):
            if self._entity_position_value(attacker) < int(positions_enum.POS_RESTING.value):
                return {"to_char": "", "to_victim": "", "to_room": "", "killed": False}

        if CharacterMacros.is_npc(attacker):
            return self.mob_hit(attacker, victim, dt=dt)
        return self.one_hit(attacker, victim, dt=dt)

    def check_assist(self, attacker, victim) -> None:
        # Placeholder for ROM assist logic migration.
        return

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
            form = getattr(getattr(entity, "mobile_flags", None), "form", None)
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
            parts = getattr(getattr(entity, "mobile_flags", None), "parts", None)
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

    @staticmethod
    def _set_standing_position(entity) -> None:
        positions_enum = CharacterMacros.get_enum("positions")
        if not hasattr(positions_enum, "POS_STANDING"):
            return
        stand_pos = int(positions_enum.POS_STANDING.value)
        attrs = getattr(entity, "character_attributes", None)
        if attrs is not None:
            attrs.position = stand_pos
            return
        setattr(entity, "position", stand_pos)
