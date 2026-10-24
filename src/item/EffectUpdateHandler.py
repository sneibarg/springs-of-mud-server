from injector import inject
from api.CharacterApi import CharacterApi
from combat.CombatHandler import FightHandler
from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from game.RandomNumberGenerator import RandomNumberGenerator
from item.Effect import Effect
from item.EffectHandler import EffectHandler
from player.Character import Character
from server.messaging.MessageBus import MessageBus
from util.DisplayUtil import DisplayUtil
from util.EffectUtil import EffectUtil
from util.GenericUtil import GenericUtil


class EffectUpdateHandler:
    """Coordinate periodic effects, their source payloads, and cross-entity consequences."""

    @inject
    def __init__(self, registry_service: RegistryService, enum_provider: EnumProvider,
                 effect_handler: EffectHandler, fight_handler: FightHandler, message_bus: MessageBus):
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.effect_handler = effect_handler
        self.fight_handler = fight_handler
        self.message_bus = message_bus
        self.PositionsEnum = enum_provider.get("positions")
        self.AffectedBits = enum_provider.get("affectedBy")
        self.rng = RandomNumberGenerator()

    def expired_messages(self, entity, field_name):
        result = self.effect_handler.tick_effects(entity)
        return [message for effect in result.expired_effects
                if (message := self._lookup_effect_message(getattr(effect, "type", ""), field_name))]

    async def tick_status_effects(self, entity, room=None) -> None:
        if entity is None:
            return
        room = room or self.room_registry.get_or_none(id=getattr(entity, 'room_id', ''))

        if entity.is_affected(self.AffectedBits, "AFF_PLAGUE"):
            await self._tick_plague(entity, room)
            return

        if entity.is_affected(self.AffectedBits, "AFF_POISON") and not entity.is_affected(self.AffectedBits, "AFF_SLOW"):
            poison = entity.find_effect("spell.poison", "poison", affected_bits=self.AffectedBits, bit_name="AFF_POISON")
            if poison is not None:
                await self._send_effect_payload(poison, "tick", entity, room)
                damage = GenericUtil.to_int(getattr(poison, "level", 0), 0) // 10 + 1
                self.fight_handler.apply_periodic_damage(entity, damage)
            return

        position = entity.position_value(self.PositionsEnum)
        if position == self._pos_value("POS_INCAP"):
            if self.rng.number_range(0, 1) == 0:
                self.fight_handler.apply_periodic_damage(entity, 1)
            return
        if position == self._pos_value("POS_MORTAL"):
            self.fight_handler.apply_periodic_damage(entity, 1)

    async def _tick_plague(self, entity, room) -> None:
        if room is None:
            return

        plague = entity.find_effect("spell.plague", "plague", affected_bits=self.AffectedBits, bit_name="AFF_PLAGUE")
        if plague is None:
            entity.set_affected(self.AffectedBits, "AFF_PLAGUE", False)
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
            if victim.is_affected(self.AffectedBits, "AFF_PLAGUE"):
                continue
            if self.rng.number_bits(4) != 0:
                continue
            if EffectUtil.saves_spell(GenericUtil.to_int(spread.level, 0) - 2, victim, "DAM_DISEASE",
                                      immunity=self.fight_handler._check_immunity):
                continue

            await self._send_effect_payload(spread, "spread", victim, room)
            self.effect_handler.affect_join(victim, spread)

        damage = min(GenericUtil.to_int(getattr(entity, "level", 0), 0), plague_level // 5 + 1)
        setattr(entity, "mana", GenericUtil.to_int(getattr(entity, "mana", 0), 0) - damage)
        setattr(entity, "movement", GenericUtil.to_int(getattr(entity, "movement", 0), 0) - damage)
        self.fight_handler.apply_periodic_damage(entity, damage)

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

    def _pos_value(self, name: str) -> int:
        if self.PositionsEnum is None or name not in self.PositionsEnum.__members__:
            return -1
        return int(self.PositionsEnum[name].value)

    async def tick_effects(self, entity):
        result = self.effect_handler.tick_effects(entity)
        if type(entity) is not Character:
            return
        for effect in result.expired_effects:
            msg_off = self._lookup_effect_message(getattr(effect, "type", ""), "msg_off")
            if msg_off:
                await self.message_bus.send_to_character(entity.id, self.message_bus.text_to_message(f"{msg_off}\r\n"))

    def _lookup_effect_message(self, effect_type, field_name: str) -> str:
        ability = self._effect_ability(effect_type)
        render = getattr(ability, "message", None)
        if not callable(render):
            return ""
        return DisplayUtil.display_effect_message(render("to_char", field_name))

