import asyncio
from enum import IntEnum

from injector import inject
from area.AreaHandler import AreaHandler
from combat.CombatRegistry import CombatRegistry
from combat.CombatHandler import FightHandler
from api.GameApi import GameApi
from game.EnumProvider import EnumProvider
from game.RandomNumberGenerator import RandomNumberGenerator
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from util.GenericUtil import GenericUtil
from game.RegistryService import RegistryService
from game.WeatherHandler import WeatherHandler
from mobile.MobileHandler import MobileHandler
from player.Character import Character
from api.CharacterApi import CharacterApi
from player.CharacterService import CharacterService
from server.messaging.MessageBus import MessageBus
from server.session.SessionHandler import SessionHandler
from skill.Ability import Ability
from util.DisplayUtil import DisplayUtil
from util.EffectUtil import EffectUtil


class UpdateHandler:
    @inject
    def __init__(self,
                 weather_handler: WeatherHandler,
                 area_handler: AreaHandler,
                 mobile_handler: MobileHandler,
                 fight_handler: FightHandler,
                 message_bus: MessageBus,
                 registry_service: RegistryService,
                 character_service: CharacterService,
                 session_handler: SessionHandler,
                 enum_provider: EnumProvider,
                 effect_handler: EffectHandler):
        self.weather_handler = weather_handler
        self.area_handler = area_handler
        self.mobile_handler = mobile_handler
        self.fight_handler = fight_handler
        self.message_bus = message_bus
        self.character_service = character_service
        self.session_handler = session_handler
        self.effect_handler = effect_handler
        self.character_registry = registry_service.character_registry
        self.area_registry = registry_service.area_registry
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.combat_registry: CombatRegistry = registry_service.combat_registry
        self.pulse_area = 0
        self.pulse_mobile = 0
        self.pulse_violence = 0
        self.pulse_point = 0
        self.pulse_music = 0  # maybe we skip migrating music
        self.save_cycle = 30
        self.save_number = 0
        self.enum_provider = enum_provider
        self.GameParametersEnum = enum_provider.get("gameParameters")
        self.PositionsEnum = enum_provider.get("positions")
        self.AffectedBits = enum_provider.get("affectedBy")
        self.ItemTypes = enum_provider.get("itemTypes")
        self.WearLocation = enum_provider.get("wearLocation")
        self.WearFlags = enum_provider.get("wearFlags")
        self.rng = RandomNumberGenerator()

    async def handle_updates(self):
        self.pulse_area -= 1
        self.pulse_mobile -= 1
        self.pulse_violence -= 1
        self.pulse_point -= 1
        self.pulse_music -= 1

        if self.pulse_area <= 0:
            self.pulse_area = self.GameParametersEnum.PULSE_AREA.value
            self.area_handler.area_update()
        if self.pulse_point <= 0:
            self.pulse_point = self.GameParametersEnum.PULSE_TICK.value
            await self.weather_handler.update()
            await self.char_update()
            await self.obj_update()
        if self.pulse_music <= 0:
            self.pulse_music = self.GameParametersEnum.PULSE_MUSIC.value
        if self.pulse_mobile <= 0:
            self.pulse_mobile = self.GameParametersEnum.PULSE_MOBILE.value
            await self.mobile_handler.mobile_update()
        if self.pulse_violence <= 0:
            self.pulse_violence = self.GameParametersEnum.PULSE_VIOLENCE.value
            self._refresh_combat_registry_from_world()
            await self._violence_update()
        await self._aggr_update()

    def _refresh_combat_registry_from_world(self):
        active_keys: set[tuple[str, str, str]] = set()

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for attacker in room.people():
                defender = getattr(attacker, "fighting", None)
                if defender is None:
                    continue
                attacker_id = str(getattr(attacker, "id", "") or "")
                defender_id = str(getattr(defender, "id", "") or "")
                if not attacker_id or not defender_id:
                    self.fight_handler.stop_fighting(attacker, both=False)
                    continue
                if room.find_entity_in_room(defender_id) is None:
                    self.fight_handler.stop_fighting(attacker, both=False)
                    continue
                key = (attacker_id, defender_id, str(room.id))
                active_keys.add(key)
                self.combat_registry.upsert(attacker_id, defender_id, room.id)

        self.combat_registry.retain_keys(active_keys)

    async def _violence_update(self):
        try:
            positions_enum = CharacterApi.get_enum("positions")
        except RuntimeError:
            positions_enum = self.PositionsEnum
        if positions_enum is None:
            return

        prompted_characters: dict[str, Character] = {}
        events = list(self.combat_registry.all_events())
        decorated_events = []
        for index, event in enumerate(events):
            room = self.room_registry.get_or_none(id=event.room_id)
            attacker = room.find_entity_in_room(event.attacker_id) if room is not None else None
            decorated_events.append((0 if (attacker is not None and CharacterApi.is_npc(attacker)) else 1, index, event))

        for _, _, event in sorted(decorated_events, key=lambda item: (item[0], item[1])):
            room = self.room_registry.get_or_none(id=event.room_id)
            if room is None:
                self.combat_registry.remove_by_id(event.id)
                continue

            attacker = room.find_entity_in_room(event.attacker_id)
            defender = room.find_entity_in_room(event.defender_id)
            if attacker is None or defender is None:
                self.combat_registry.remove_by_id(event.id)
                continue

            if not CharacterApi.is_awake(attacker):
                self.fight_handler.stop_fighting(attacker, both=False)
                continue

            # ROM combat.c parity: if awake and in same room then multi_hit(), else stop_fighting().
            if room.find_entity_in_room(event.defender_id) is None:
                self.fight_handler.stop_fighting(attacker, both=False)
                continue

            result = self.fight_handler.multi_hit(attacker, defender, dt="TYPE_UNDEFINED")
            payload = self.fight_handler.build_round_payload(attacker, defender, room, result)
            prompted = await self._emit_combat_payload(attacker, payload)
            prompted_characters.update({character.id: character for character in prompted})
            if getattr(attacker, "fighting", None) is not None:
                self.fight_handler.check_assist(attacker, defender)

        for character in prompted_characters.values():
            room = self.room_registry.get_or_none(id=character.room_id)
            area = self.area_registry.get_or_none(id=getattr(room, "area_id", getattr(character, "area_id", ""))) if room is not None else self.area_registry.get_or_none(id=character.area_id)
            if room is not None and area is not None:
                await self.message_bus.send_prompt(character, area, room)

    async def _emit_combat_payload(self, attacker, payload: dict) -> list[Character]:
        prompted: list[Character] = []
        if not isinstance(payload, dict):
            return prompted
        payload["to_char"] = f"{payload.get('to_char', '')}{Ability.take_improve_messages(attacker)}"
        victim = payload.get("victim")
        if victim is not None:
            payload["to_victim"] = f"{payload.get('to_victim', '')}{Ability.take_improve_messages(victim)}"

        if payload.get("to_char") and not CharacterApi.is_npc(attacker):
            await self.message_bus.send_to_character(attacker.id, self.message_bus.text_to_message(payload["to_char"]))
            prompted.append(attacker)
        if payload.get("to_victim") and payload.get("victim") is not None and not CharacterApi.is_npc(payload["victim"]):
            await self.message_bus.send_to_character(payload["victim"].id, self.message_bus.text_to_message(payload["to_victim"]))
            prompted.append(payload["victim"])
        if payload.get("to_room"):
            targets = payload.get("targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)
                prompted.extend(target for target in targets if not CharacterApi.is_npc(target))
        return prompted

    async def _aggr_update(self):
        prompted_characters: dict[str, Character] = {}
        for room in self.room_registry.all_rooms():
            if room is None:
                continue

            for attacker, payload in self.fight_handler.aggressive_room_rounds(room):
                prompted = await self.fight_handler.emit_round_payload(attacker, payload)
                prompted_characters.update({victim.id: victim for victim in prompted})

        for character in prompted_characters.values():
            room = self.room_registry.get_or_none(id=character.room_id)
            area = self.area_registry.get_or_none(id=getattr(room, "area_id", getattr(character, "area_id", ""))) if room is not None else self.area_registry.get_or_none(id=character.area_id)
            if room is not None and area is not None:
                await self.message_bus.send_prompt(character, area, room)

    async def char_update(self):
        if self.PositionsEnum is None:
            return

        self._advance_save_counter()
        pos_stunned = self.PositionsEnum.POS_STUNNED.value
        for ch in self._active_player_characters():
            attrs = getattr(ch, "character_attributes", None)
            if attrs is None:
                continue
            room = self._room_for_entity(ch)
            pos = GenericUtil.to_int(getattr(attrs, "position", 0), 0)
            if pos >= pos_stunned:
                self._tick_regen(ch, room)
                if pos == pos_stunned:
                    self.fight_handler.update_pos(ch)
                await self._flush_improve_messages(ch)
            await self._tick_light_source(ch, room)
            await self._tick_conditions(ch)
            await self._tick_effects(ch)
            await self._tick_rom_status_effects(ch, room)

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for mob in room.mobiles.values():
                pos = GenericUtil.to_int(getattr(mob, "position", getattr(mob, "start_pos", 0)), 0)
                if pos >= pos_stunned:
                    self._tick_regen(mob, room)
                    if pos == pos_stunned:
                        self.fight_handler.update_pos(mob)
                await self._tick_effects(mob)
                await self._tick_rom_status_effects(mob, room)

        await self._autosave_due_characters()

    async def obj_update(self):
        if self.ItemTypes is None:
            return

        for item in self._all_world_items():
            await self._tick_item_effects(item)
            timer = GenericUtil.to_int(getattr(item, "timer", -1), -1)
            if timer <= 0:
                continue
            timer -= 1
            item.timer = timer
            if timer > 0:
                continue
            await self._expire_world_item(item)

    def _advance_save_counter(self) -> None:
        self.save_number += 1
        if self.save_number >= self.save_cycle:
            self.save_number = 0

    async def _autosave_due_characters(self) -> None:
        due = [
            character for character in self._active_player_characters()
            if self._autosave_bucket(character.id) == self.save_number
        ]
        if not due:
            return

        await asyncio.gather(*[
            asyncio.to_thread(self.character_service.save_character, character)
            for character in due
        ])

    def _active_player_characters(self) -> list[Character]:
        active: list[Character] = []
        seen: set[str] = set()
        for session in self.session_handler.get_playing_sessions():
            character = getattr(session, "character", None)
            if not isinstance(character, Character):
                continue
            character_id = str(getattr(character, "id", "") or "")
            if not character_id or character_id in seen:
                continue
            seen.add(character_id)
            active.append(character)
        return active

    def _autosave_bucket(self, character_id: str) -> int:
        if self.save_cycle <= 0:
            return 0
        return sum(str(character_id).encode("utf-8")) % self.save_cycle

    async def _tick_conditions(self, entity) -> None:
        if not isinstance(entity, Character):
            return
        if CharacterApi.is_npc(entity) or CharacterApi.is_immortal(entity):
            return

        await self._gain_condition(entity, "drunk", -1)
        await self._gain_condition(entity, "thirst", -1)
        await self._gain_condition(entity, "hunger", -2 if self._is_large_race(entity) else -1)

    async def _gain_condition(self, character: Character, condition_name: str, value: int) -> None:
        if value == 0:
            return

        status_flags = getattr(character, "status_flags", None)
        if status_flags is None or not hasattr(status_flags, condition_name):
            return

        current = GenericUtil.to_int(getattr(status_flags, condition_name, -1), -1)
        if current == -1:
            return

        updated = max(0, min(48, current + value))
        setattr(status_flags, condition_name, updated)
        if updated != 0:
            return

        message = None
        if condition_name == "hunger":
            message = "You are hungry.\r\n"
        elif condition_name == "thirst":
            message = "You are thirsty.\r\n"
        elif condition_name == "drunk" and current != 0:
            message = "You are sober.\r\n"

        if message:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    def _is_large_race(self, character: Character) -> bool:
        race = getattr(character, "character_race", None)
        raw_size = getattr(race, "size", getattr(character, "size", None))
        if raw_size is None:
            return False

        try:
            size_enum = CharacterApi.get_enum("size")
        except RuntimeError:
            size_enum = None

        if isinstance(raw_size, str):
            normalized = raw_size.strip().upper()
            if size_enum is not None and normalized in size_enum.__members__:
                raw_size = size_enum[normalized].value
            else:
                return normalized in {"SIZE_LARGE", "SIZE_HUGE", "SIZE_GIANT"}

        size_value = GenericUtil.to_int(raw_size, None)
        if size_value is None:
            return False

        if size_enum is not None:
            return size_value > int(size_enum.SIZE_MEDIUM.value)
        return size_value >= 3

    async def _tick_light_source(self, character: Character, room) -> None:
        if CharacterApi.is_npc(character) or CharacterApi.is_immortal(character):
            return

        equipped = getattr(character, "equipped", None)
        light = getattr(equipped, "light", None) if equipped is not None else None
        if light is None:
            return
        if str(getattr(light, "item_type", "") or "").strip().upper() not in {"ITEM_LIGHT", "LIGHT"}:
            return

        remaining = GenericUtil.to_int(getattr(light, "value2", 0), 0)
        if remaining <= 0:
            return

        remaining -= 1
        setattr(light, "value2", str(remaining))
        if remaining == 0 and room is not None:
            room.light = max(0, GenericUtil.to_int(getattr(room, "light", 0), 0) - 1)
            item_name = light.display_name()
            await self._send_to_room_except(room, character, f"{item_name} goes out.\r\n")
            await self._send_to_entity(character, f"{item_name} flickers and goes out.\r\n")
            setattr(equipped, "light", None)
        elif remaining <= 5 and room is not None:
            await self._send_to_entity(character, f"{light.display_name()} flickers.\r\n")

    def _room_for_entity(self, entity):
        room_id = str(getattr(entity, "room_id", "") or "")
        if not room_id:
            return None
        return self.room_registry.get_or_none(id=room_id)

    def _tick_regen(self, entity, room=None):
        max_hit = GenericUtil.to_int(getattr(entity, "max_hit", 0), 0)
        max_mana = GenericUtil.to_int(getattr(entity, "max_mana", 0), 0)
        max_move = GenericUtil.to_int(getattr(entity, "max_movement", 0), 0)

        hit = GenericUtil.to_int(getattr(entity, "hit", 0), 0)
        mana = GenericUtil.to_int(getattr(entity, "mana", 0), 0)
        move = GenericUtil.to_int(getattr(entity, "movement", 0), 0)

        if hit < max_hit:
            setattr(entity, "hit", min(max_hit, hit + self.hit_gain(entity, room)))
        if mana < max_mana:
            setattr(entity, "mana", min(max_mana, mana + self.mana_gain(entity, room)))
        if move < max_move:
            setattr(entity, "movement", min(max_move, move + self.move_gain(entity, room)))

    def hit_gain(self, entity, room=None) -> int:
        if room is None:
            return 0

        max_hit = GenericUtil.to_int(getattr(entity, "max_hit", 0), 0)
        hit = GenericUtil.to_int(getattr(entity, "hit", 0), 0)
        if hit >= max_hit:
            return 0

        level = GenericUtil.to_int(getattr(entity, "level", 0), 0)
        position = self._position_value(entity)
        if CharacterApi.is_npc(entity):
            gain = 5 + level
            if self._is_affected(entity, "AFF_REGENERATION"):
                gain *= 2
            if position == self._pos_value("POS_SLEEPING"):
                gain = 3 * gain // 2
            elif position == self._pos_value("POS_RESTING"):
                pass
            elif position == self._pos_value("POS_FIGHTING"):
                gain //= 3
            else:
                gain //= 2
        else:
            attrs = getattr(entity, "character_attributes", None)
            constitution = GenericUtil.to_int(getattr(attrs, "constitution", 0), 0)
            gain = max(3, constitution - 3 + level // 2)
            gain += GenericUtil.to_int(getattr(getattr(entity, "character_class", None), "hp_max", 10), 10) - 10
            number = self.rng.number_percent()
            if number < self._skill_percent(entity, "fast healing"):
                gain += number * gain // 100
                if hit < max_hit:
                    Ability.check_improve_by_name(entity, "fast healing", True, 8)

            if position == self._pos_value("POS_SLEEPING"):
                pass
            elif position == self._pos_value("POS_RESTING"):
                gain //= 2
            elif position == self._pos_value("POS_FIGHTING"):
                gain //= 6
            else:
                gain //= 4

            if entity.condition_value("hunger") == 0:
                gain //= 2
            if entity.condition_value("thirst") == 0:
                gain //= 2

        gain = gain * GenericUtil.to_int(getattr(room, "heal_rate", 100), 100) // 100
        gain = self._apply_furniture_regen_rate(entity, gain, "value3")
        gain = self._apply_regen_affect_penalties(entity, gain)
        return min(gain, max_hit - hit)

    def mana_gain(self, entity, room=None) -> int:
        if room is None:
            return 0

        max_mana = GenericUtil.to_int(getattr(entity, "max_mana", 0), 0)
        mana = GenericUtil.to_int(getattr(entity, "mana", 0), 0)
        if mana >= max_mana:
            return 0

        level = GenericUtil.to_int(getattr(entity, "level", 0), 0)
        position = self._position_value(entity)
        if CharacterApi.is_npc(entity):
            gain = 5 + level
            if position == self._pos_value("POS_SLEEPING"):
                gain = 3 * gain // 2
            elif position == self._pos_value("POS_RESTING"):
                pass
            elif position == self._pos_value("POS_FIGHTING"):
                gain //= 3
            else:
                gain //= 2
        else:
            attrs = getattr(entity, "character_attributes", None)
            wisdom = GenericUtil.to_int(getattr(attrs, "wisdom", 0), 0)
            intelligence = GenericUtil.to_int(getattr(attrs, "intelligence", 0), 0)
            gain = (wisdom + intelligence + level) // 2
            number = self.rng.number_percent()
            if number < self._skill_percent(entity, "meditation"):
                gain += number * gain // 100
                if mana < max_mana:
                    Ability.check_improve_by_name(entity, "meditation", True, 8)

            if not bool(getattr(getattr(entity, "character_class", None), "mana_gain", True)):
                gain //= 2

            if position == self._pos_value("POS_SLEEPING"):
                pass
            elif position == self._pos_value("POS_RESTING"):
                gain //= 2
            elif position == self._pos_value("POS_FIGHTING"):
                gain //= 6
            else:
                gain //= 4

            if entity.condition_value("hunger") == 0:
                gain //= 2
            if entity.condition_value("thirst") == 0:
                gain //= 2

        gain = gain * GenericUtil.to_int(getattr(room, "mana_rate", 100), 100) // 100
        gain = self._apply_furniture_regen_rate(entity, gain, "value4")
        gain = self._apply_regen_affect_penalties(entity, gain)
        return min(gain, max_mana - mana)

    def move_gain(self, entity, room=None) -> int:
        if room is None:
            return 0

        max_move = GenericUtil.to_int(getattr(entity, "max_movement", 0), 0)
        move = GenericUtil.to_int(getattr(entity, "movement", 0), 0)
        if move >= max_move:
            return 0

        level = GenericUtil.to_int(getattr(entity, "level", 0), 0)
        position = self._position_value(entity)
        if CharacterApi.is_npc(entity):
            gain = level
        else:
            attrs = getattr(entity, "character_attributes", None)
            dexterity = GenericUtil.to_int(getattr(attrs, "dexterity", 0), 0)
            gain = max(15, level)
            if position == self._pos_value("POS_SLEEPING"):
                gain += dexterity
            elif position == self._pos_value("POS_RESTING"):
                gain += dexterity // 2

            if entity.condition_value("hunger") == 0:
                gain //= 2
            if entity.condition_value("thirst") == 0:
                gain //= 2

        gain = gain * GenericUtil.to_int(getattr(room, "heal_rate", 100), 100) // 100
        gain = self._apply_furniture_regen_rate(entity, gain, "value3")
        gain = self._apply_regen_affect_penalties(entity, gain)
        return min(gain, max_move - move)

    def _apply_regen_affect_penalties(self, entity, gain: int) -> int:
        if self._is_affected(entity, "AFF_POISON"):
            gain //= 4
        if self._is_affected(entity, "AFF_PLAGUE"):
            gain //= 8
        if self._is_affected(entity, "AFF_HASTE") or self._is_affected(entity, "AFF_SLOW"):
            gain //= 2
        return gain

    @staticmethod
    def _apply_furniture_regen_rate(entity, gain: int, field_name: str) -> int:
        furniture = getattr(entity, "on", None)
        if furniture is None:
            return gain
        if str(getattr(furniture, "item_type", "") or "").strip().upper() not in {"ITEM_FURNITURE", "FURNITURE"}:
            return gain
        return gain * GenericUtil.to_int(getattr(furniture, field_name, 100), 100) // 100

    def _is_affected(self, entity, bit_name: str) -> bool:
        if self.AffectedBits is None:
            return False
        bit = CharacterApi.enum_bit(self.AffectedBits, bit_name)
        if bit <= 0:
            return False
        status_flags = getattr(entity, "status_flags", None)
        return CharacterApi.is_set(GameApi.flags_to_int(getattr(status_flags, "affected_by", 0)), bit)

    async def _flush_improve_messages(self, character: Character) -> None:
        messages = Ability.take_improve_messages(character)
        if messages:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(messages))

    async def _tick_rom_status_effects(self, entity, room=None) -> None:
        if entity is None:
            return
        room = room or self._room_for_entity(entity)

        if self._is_affected(entity, "AFF_PLAGUE"):
            await self._tick_plague(entity, room)
            return

        if self._is_affected(entity, "AFF_POISON") and not self._is_affected(entity, "AFF_SLOW"):
            poison = self._find_effect(entity, "spell.poison", "poison", bit_name="AFF_POISON")
            if poison is not None:
                await self._send_effect_payload(poison, "tick", entity, room)
                damage = GenericUtil.to_int(getattr(poison, "level", 0), 0) // 10 + 1
                self._apply_periodic_damage(entity, damage)
            return

        position = self._position_value(entity)
        if position == self._pos_value("POS_INCAP"):
            if self.rng.number_range(0, 1) == 0:
                self._apply_periodic_damage(entity, 1)
            return
        if position == self._pos_value("POS_MORTAL"):
            self._apply_periodic_damage(entity, 1)

    async def _tick_plague(self, entity, room) -> None:
        if room is None:
            return

        plague = self._find_effect(entity, "spell.plague", "plague", bit_name="AFF_PLAGUE")
        if plague is None:
            self._set_affected(entity, "AFF_PLAGUE", False)
            return

        await self._send_effect_payload(plague, "tick", entity, room)

        plague_level = GenericUtil.to_int(getattr(plague, "level", 0), 0)
        if plague_level == 1:
            return

        spread = Effect(
            where="TO_AFFECTS",
            type=getattr(plague, "type", "spell.plague"),
            level=plague_level - 1,
            duration=self.rng.number_range(1, max(1, 2 * (plague_level - 1))),
            location="APPLY_STR",
            modifier=-5,
            bitvector="AFF_PLAGUE",
            apply_to="char",
        )

        for victim in room.people():
            if victim is entity:
                continue
            if CharacterApi.is_immortal(victim):
                continue
            if self._is_affected(victim, "AFF_PLAGUE"):
                continue
            if self.rng.number_bits(4) != 0:
                continue
            if EffectUtil.saves_spell(GenericUtil.to_int(spread.level, 0) - 2, victim, 0):
                continue

            await self._send_effect_payload(spread, "spread", victim, room)
            self.effect_handler.affect_join(victim, spread)

        damage = min(GenericUtil.to_int(getattr(entity, "level", 0), 0), plague_level // 5 + 1)
        setattr(entity, "mana", GenericUtil.to_int(getattr(entity, "mana", 0), 0) - damage)
        setattr(entity, "movement", GenericUtil.to_int(getattr(entity, "movement", 0), 0) - damage)
        self._apply_periodic_damage(entity, damage)

    def _apply_periodic_damage(self, entity, damage: int) -> None:
        damage = max(0, GenericUtil.to_int(damage, 0))
        if damage <= 0:
            return
        setattr(entity, "hit", GenericUtil.to_int(getattr(entity, "hit", 0), 0) - damage)
        self.fight_handler.update_pos(entity)
        if self._position_value(entity) <= self._pos_value("POS_DEAD"):
            self.fight_handler.raw_kill(entity)

    def _find_effect(self, entity, *type_names: str, bit_name: str = ""):
        wanted_types = {str(type_name or "").strip().lower() for type_name in type_names if str(type_name or "").strip()}
        bit = CharacterApi.enum_bit(self.AffectedBits, bit_name) if bit_name else 0
        for effect in list(getattr(entity, "effects", []) or []):
            effect_type = str(getattr(effect, "type", "") or "").strip().lower()
            if effect_type in wanted_types:
                return effect
            if bit > 0 and self._effect_has_bit(effect, bit_name, bit):
                return effect
        return None

    @staticmethod
    def _effect_has_bit(effect, bit_name: str, bit: int) -> bool:
        raw = getattr(effect, "bitvector", 0)
        if str(raw or "").strip().upper() == str(bit_name or "").strip().upper():
            return True
        return GameApi.flags_to_int(raw) == bit

    def _set_affected(self, entity, bit_name: str, enabled: bool) -> None:
        if self.AffectedBits is None:
            return
        bit = CharacterApi.enum_bit(self.AffectedBits, bit_name)
        if bit <= 0:
            return
        status_flags = getattr(entity, "status_flags", None)
        if status_flags is None:
            return
        raw = GameApi.flags_to_int(getattr(status_flags, "affected_by", 0))
        updated = GameApi.set_bit(raw, bit) if enabled else GameApi.unset_bit(raw, bit)
        if hasattr(status_flags, "assign_bitfield"):
            status_flags.assign_bitfield("affected_by", updated)
        else:
            setattr(status_flags, "affected_by", updated)

    async def _send_effect_payload(self, effect, key: str, entity, room) -> None:
        await self._send_to_room_except(room, entity, self._effect_payload(effect, "to_room", key, entity))
        await self._send_to_entity(entity, self._effect_payload(effect, "to_victim", key, entity))

    def _effect_payload(self, effect, channel: str, key: str, entity) -> str:
        ability = self._effect_ability(effect)
        render = getattr(ability, "message", None)
        if not callable(render):
            return ""
        return render(
            channel,
            key,
            victim=entity.display_name(),
            possessive=getattr(entity, "his_her", lambda: "its")(),
        )

    def _effect_ability(self, effect):
        effect_type = getattr(effect, "type", effect)
        candidates = {
            str(value or "").strip().lower()
            for value in (
                effect_type,
                str(effect_type or "").replace("spell.", ""),
                str(effect_type or "").replace("skill.", ""),
            )
            if str(value or "").strip()
        }
        if not candidates:
            return None

        for registry, method_name in ((self.spell_registry, "all_spells"), (self.skill_registry, "all_skills")):
            method = getattr(registry, method_name, None)
            if not callable(method):
                continue
            try:
                entries = list(method() or [])
            except TypeError:
                continue
            for entry in entries:
                names = {
                    str(getattr(entry, "handler_id", "") or "").strip().lower(),
                    str(getattr(entry, "name", "") or "").strip().lower(),
                    str(getattr(entry, "id", "") or "").strip().lower(),
                }
                if candidates & names:
                    return entry
        return None

    async def _send_to_entity(self, entity, text: str) -> None:
        if entity is None or CharacterApi.is_npc(entity) or not text:
            return
        await self.message_bus.send_to_character(entity.id, self.message_bus.text_to_message(text))

    async def _send_to_room_except(self, room, excluded, text: str) -> None:
        if room is None or not text:
            return
        targets = [
            player for player in room.players_in_room()
            if str(getattr(player, "id", "") or "") != str(getattr(excluded, "id", "") or "")
        ]
        if targets:
            await self.message_bus.send_to_room(self.message_bus.text_to_message(text), targets)

    def _position_value(self, entity) -> int:
        attrs = getattr(entity, "character_attributes", None)
        raw = getattr(attrs, "position", None) if attrs is not None else None
        if raw is None:
            raw = getattr(entity, "position", getattr(entity, "start_pos", self._pos_value("POS_STANDING")))
        if isinstance(raw, str):
            name = raw.strip().upper()
            if name and not name.startswith("POS_"):
                name = f"POS_{name}"
            value = self._pos_value(name)
            if value >= 0:
                return value
        return GenericUtil.to_int(raw, self._pos_value("POS_STANDING"))

    def _pos_value(self, name: str) -> int:
        if self.PositionsEnum is None or name not in self.PositionsEnum.__members__:
            return -1
        return int(self.PositionsEnum[name].value)

    @staticmethod
    def _skill_percent(entity, skill_name: str) -> int:
        if CharacterApi.is_npc(entity):
            return 0
        return Character.learned_entry_level(Character.get_learned(entity, skill_name, collection_name="skills"))

    def _all_world_items(self):
        seen = set()
        items = []

        def walk_item(item):
            if item is None:
                return
            key = id(item)
            if key in seen:
                return
            seen.add(key)
            items.append(item)
            for child in list(getattr(item, "contains", []) or []):
                walk_item(child)

        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for obj in room.contents.values():
                walk_item(obj)
            for ch in room.characters.values():
                for obj in list(getattr(ch, "loot", []) or []):
                    walk_item(obj)
                equipped = getattr(ch, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    walk_item(obj)
            for mob in room.mobiles.values():
                for obj in list(getattr(mob, "inventory", []) or []):
                    walk_item(obj)
                equipped = getattr(mob, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    walk_item(obj)

        return items

    async def _expire_world_item(self, item):
        item_type = str(getattr(item, "item_type", "") or "").upper()
        is_pc_corpse = self.ItemTypes is not None and item_type in [self.ItemTypes.ITEM_CORPSE_PC.name]
        is_float = (
            self.WearLocation is not None
            and GenericUtil.to_int(getattr(item, "wear_loc", -1), -1) in [self.WearLocation.WEAR_FLOAT.value]
        )

        location = self._locate_item(item)
        if location is None:
            return

        parent_kind = location["kind"]
        parent = location["parent"]
        container = location["container"]
        room = location.get("room")

        message = self._decay_message(item, is_float=is_float)
        await self._emit_item_decay_message(message, item, parent_kind, parent, room, is_float)

        contents = list(getattr(item, "contains", []) or [])
        if (is_pc_corpse or is_float) and contents:
            for child in contents:
                self._move_child_from_expiring_item(child, parent_kind, parent, container, room)
            item.contains = []

        self._remove_item_at_location(item, parent_kind, parent, container)

    def _move_child_from_expiring_item(self, child, parent_kind: str, parent, container, room):
        if parent_kind == "room":
            parent.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child
            return
        if parent_kind == "char_loot":
            parent.loot.append(child)
            return
        if parent_kind == "mob_inventory":
            parent.inventory.append(child)
            return
        if parent_kind == "item_contains":
            container.append(child)
            return
        if parent_kind == "char_equipped":
            holder = room or self.room_registry.get_or_none(id=getattr(parent, "room_id", ""))
            if holder is not None:
                holder.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child
            return
        if parent_kind == "mob_equipped":
            holder = room
            if holder is not None:
                holder.contents[getattr(child, "id", GenericUtil.generate_mongo_id())] = child

    @staticmethod
    def _remove_item_at_location(item, parent_kind: str, parent, container):
        if parent_kind == "room":
            parent.contents.pop(getattr(item, "id", ""), None)
            return
        if parent_kind == "char_loot":
            if item in parent.loot:
                parent.loot.remove(item)
            return
        if parent_kind == "mob_inventory":
            if item in parent.inventory:
                parent.inventory.remove(item)
            return
        if parent_kind == "item_contains":
            if item in container:
                container.remove(item)
            return
        if parent_kind in ["char_equipped", "mob_equipped"]:
            equipped = getattr(parent, "equipped", None)
            if equipped is None:
                return
            for slot, equipped_item in getattr(equipped, "__dict__", {}).items():
                if equipped_item is item:
                    setattr(equipped, slot, None)
                    break

    def _locate_item(self, target):
        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for obj in room.contents.values():
                if obj is target:
                    return {"kind": "room", "parent": room, "container": None, "room": room}
                found = self._locate_in_contains(target, obj.contains, room)
                if found is not None:
                    return found

            for ch in room.characters.values():
                for obj in list(getattr(ch, "loot", []) or []):
                    if obj is target:
                        return {"kind": "char_loot", "parent": ch, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains, room)
                    if found is not None:
                        return found

                equipped = getattr(ch, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    if obj is target:
                        return {"kind": "char_equipped", "parent": ch, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains if obj is not None else [], room)
                    if found is not None:
                        return found

            for mob in room.mobiles.values():
                for obj in list(getattr(mob, "inventory", []) or []):
                    if obj is target:
                        return {"kind": "mob_inventory", "parent": mob, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains, room)
                    if found is not None:
                        return found

                equipped = getattr(mob, "equipped", None)
                for obj in getattr(equipped, "__dict__", {}).values() if equipped is not None else []:
                    if obj is target:
                        return {"kind": "mob_equipped", "parent": mob, "container": None, "room": room}
                    found = self._locate_in_contains(target, obj.contains if obj is not None else [], room)
                    if found is not None:
                        return found
        return None

    def _locate_in_contains(self, target, container, room):
        for obj in list(container or []):
            if obj is target:
                return {"kind": "item_contains", "parent": None, "container": container, "room": room}
            found = self._locate_in_contains(target, getattr(obj, "contains", []), room)
            if found is not None:
                return found
        return None

    async def _tick_effects(self, entity):
        result = self.effect_handler.tick_effects(entity)
        if type(entity) is not Character:
            return
        for effect in result.expired_effects:
            msg_off = self._lookup_effect_message(getattr(effect, "type", ""), "msg_off")
            if msg_off:
                await self.message_bus.send_to_character(entity.id, self.message_bus.text_to_message(f"{msg_off}\r\n"))

    async def _tick_item_effects(self, item):
        result = self.effect_handler.tick_effects(item)
        for effect in result.expired_effects:
            msg_obj = self._lookup_effect_message(getattr(effect, "type", ""), "msg_obj")
            if msg_obj:
                await self._emit_obj_effect_message(item, msg_obj)

    def _lookup_effect_message(self, effect_type, field_name: str) -> str:
        ability = self._effect_ability(effect_type)
        render = getattr(ability, "message", None)
        if not callable(render):
            return ""
        return DisplayUtil.display_effect_message(render("to_char", field_name))

    async def _emit_obj_effect_message(self, item, message: str):
        location = self._locate_item(item)
        if location is None:
            return

        parent_kind = location["kind"]
        parent = location["parent"]
        room = location.get("room")
        text = self._format_item_message(message, item)
        if not text:
            return

        if parent_kind in ["char_loot", "char_equipped"]:
            await self.message_bus.send_to_character(parent.id, self.message_bus.text_to_message(text + "\r\n"))
            return
        if room is not None:
            in_room = room.players_in_room()
            message = self.message_bus.text_to_message(text + "\r\n")
            await self.message_bus.send_to_room(message, in_room)

    def _decay_message(self, item, is_float: bool) -> str:
        item_type = str(getattr(item, "item_type", "") or "").upper()
        if self.ItemTypes is None:
            return "$p crumbles into dust."
        if item_type in [self.ItemTypes.ITEM_FOUNTAIN.name]:
            return "$p dries up."
        if item_type in [self.ItemTypes.ITEM_CORPSE_NPC.name, self.ItemTypes.ITEM_CORPSE_PC.name]:
            return "$p decays into dust."
        if item_type in [self.ItemTypes.ITEM_FOOD.name]:
            return "$p decomposes."
        if item_type in [self.ItemTypes.ITEM_POTION.name]:
            return "$p has evaporated from disuse."
        if item_type in [self.ItemTypes.ITEM_PORTAL.name]:
            return "$p fades out of existence."
        if item_type in [self.ItemTypes.ITEM_CONTAINER.name]:
            if self._can_wear_float(item):
                if list(getattr(item, "contains", []) or []):
                    return "$p flickers and vanishes, spilling its contents on the floor."
                return "$p flickers and vanishes."
            return "$p crumbles into dust."
        return "$p crumbles into dust."

    def _can_wear_float(self, item) -> bool:
        if self.WearFlags is None or not hasattr(self.WearFlags, "ITEM_WEAR_FLOAT"):
            return False
        wear_raw = GameApi.flags_to_int(getattr(item, "wear_flags", 0))
        return GameApi.is_set(wear_raw, self.WearFlags.ITEM_WEAR_FLOAT.value)

    async def _emit_item_decay_message(self, message: str, item, parent_kind: str, parent, room, is_float: bool):
        text = self._format_item_message(message, item)
        if not text:
            return

        message = self.message_bus.text_to_message(text + "\r\n")
        if parent_kind in ["char_loot", "char_equipped"]:
            await self.message_bus.send_to_character(parent.id, self.message_bus.text_to_message(text + "\r\n"))
            in_room = room.players_in_room()
            if is_float and room is not None:
                await self.message_bus.send_to_room(message, in_room)
            return
        if room is not None:
            in_room = room.players_in_room()
            await self.message_bus.send_to_room(message, in_room)

    @staticmethod
    def _format_item_message(message: str, item) -> str:
        item_name = str(getattr(item, "short_description", "") or getattr(item, "name", "something"))
        return str(message or "").replace("$p", item_name)
