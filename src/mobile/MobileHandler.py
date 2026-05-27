import inspect

from injector import inject
from area.AreaRegistry import AreaRegistry
from area.RoomRegistry import RoomRegistry
from area.ShopRegistry import ShopRegistry
from game.EnumProvider import EnumProvider
from util.GenericUtil import GenericUtil
from game.RandomNumberGenerator import RandomNumberGenerator
from game.RegistryService import RegistryService
from game.WeatherHandler import WeatherHandler
from fight.FightHandler import FightHandler
from item.EffectHandler import EffectHandler
from mobile.Mobile import Mobile
from mobile.KillTable import KillTable
from api.MobileApi import MobileApi, MobileContext
from player.Character import Character
from api.CharacterApi import CharacterApi
from server.LoggerFactory import LoggerFactory
from server.messaging import MessageBus
from api.SpellApi import SpellApi


class MobileHandler:
    @inject
    def __init__(self,
                 message_bus: MessageBus,
                 registry_service: RegistryService,
                 area_registry: AreaRegistry,
                 room_registry: RoomRegistry,
                 shop_registry: ShopRegistry,
                 fight_handler: FightHandler,
                 weather_handler: WeatherHandler,
                 enum_provider: EnumProvider,
                 effect_handler: EffectHandler):
        self.__name__ = "MobileHandler"
        self.message_bus = message_bus
        self.registry_service = registry_service
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.shop_registry = shop_registry
        self.fight_handler = fight_handler
        self.weather_handler = weather_handler
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = registry_service.spell_registry
        self.special_registry = registry_service.special_registry
        self.logger = LoggerFactory.get_logger(__name__)
        self.rng = RandomNumberGenerator()
        self.effect_handler = effect_handler
        self.spell_api = SpellApi(effect_handler=effect_handler)
        self.act_bits = enum_provider.get("actBits")
        self.affected_bits = enum_provider.get("affectedBy")
        self.positions = enum_provider.get("positions")
        self.room_flags = enum_provider.get("roomFlags")
        self.exit_flags = enum_provider.get("exitFlags")
        self.wear_flags = enum_provider.get("wearFlags")
        self._special_library_cache = None
        self.kill_table: dict[int, KillTable] = {}
        self.rebuild_kill_table()

    def rebuild_kill_table(self) -> None:
        kill_table: dict[int, KillTable] = {}
        for mob in list(self.registry_service.mobile_registry.all_mobiles() or []):
            level = max(0, min(GenericUtil.to_int(getattr(mob, "level", 0), 0), 100))
            entry = kill_table.setdefault(level, KillTable())
            entry.number += 1
        self.kill_table = kill_table

    def record_mobile_kill(self, mob) -> None:
        if mob is None:
            return
        if not self.kill_table:
            self.rebuild_kill_table()
        level = max(0, min(GenericUtil.to_int(getattr(mob, "level", 0), 0), 100))
        entry = self.kill_table.setdefault(level, KillTable())
        entry.killed += 1

    async def print_mobiles_in_room(self, character: Character):
        room = self.room_registry.get_or_none(id=getattr(character, "room_id", ""))
        message = room.get_mobiles_in_room(character)
        if message:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    async def mobile_update(self):
        if self.act_bits is None:
            self.logger.warning("Act bits not initialized, skipping mobile update")
            return

        snapshots = []
        for room in self.room_registry.all_rooms():
            if room is None:
                continue
            for mob in list(room.mobiles.values()):
                snapshots.append((room, mob))
        self.logger.debug(f"mobile_update starting with {len(snapshots)} mobile snapshot(s)")

        for room, mob in snapshots:
            self.logger.debug(f"mobile_update evaluating {self._actor_label(mob)} from snapshot room {self._room_label(room)}")
            room = self._resolve_room_for_mobile(room, mob)
            if mob is None or room is None or getattr(mob, "id", None) not in room.mobiles:
                self.logger.debug(f"mobile_update skipping snapshot because mob or resolved room is invalid: mob={self._actor_label(mob)}, room={self._room_label(room)}")
                continue
            if MobileApi.mobile_is_charmed(mob):
                self.logger.debug(f"mobile_update skipping {self._actor_label(mob)} in {self._room_label(room)} because it is charmed")
                continue
            if self._skip_in_empty_area(room, mob):
                self.logger.debug(f"mobile_update skipping {self._actor_label(mob)} in {self._room_label(room)} because the area is empty and ACT_UPDATE_ALWAYS is not set")
                continue

            self._update_shop_money(mob)

            special_performed = await self.execute_special_function(mob, room)
            self.logger.debug(
                f"mobile_update special execution result for {self._actor_label(mob)} in {self._room_label(room)}: "
                f"special_name={str(getattr(mob, 'special_name', '') or '')!r}, performed={special_performed}"
            )
            if special_performed:
                continue

            if not MobileApi.mobile_is_standing(mob):
                self.logger.debug(f"mobile_update skipping generic specials for {self._actor_label(mob)} in {self._room_label(room)} because position is not standing")
                continue

            self.logger.debug(f"mobile_update executing generic special spec_scavenge for {self._actor_label(mob)} in {self._room_label(room)}")
            await self._execute_generic_special(mob, room, "spec_scavenge")
            room = self._resolve_room_for_mobile(room, mob)
            if room is None:
                self.logger.debug(f"mobile_update stopping after spec_scavenge because {self._actor_label(mob)} no longer resolves to a room")
                continue

            self.logger.debug(f"mobile_update executing generic special spec_wander for {self._actor_label(mob)} in {self._room_label(room)}")
            await self._execute_generic_special(mob, room, "spec_wander")
        self.logger.debug("mobile_update completed")

    def _skip_in_empty_area(self, room, mob: Mobile) -> bool:
        area = self.area_registry.get_or_none(id=getattr(room, "area_id", ""))
        if area is None or not getattr(area, "empty", False):
            return False
        return not MobileApi.mobile_has_act(mob, self.act_bits, "ACT_UPDATE_ALWAYS")

    def _update_shop_money(self, mob: Mobile):
        shop = self.shop_registry.find_by_keeper_vnum(getattr(mob, "vnum", ""))
        if shop is None:
            return
        wealth = GenericUtil.to_int(getattr(mob, "wealth", 0), 0)
        if wealth <= 0:
            return
        gold = GenericUtil.to_int(getattr(mob, "gold", 0), 0)
        silver = GenericUtil.to_int(getattr(mob, "silver", 0), 0)
        if (gold * 100 + silver) >= wealth:
            return
        self.logger.info(
            f"mobile_update topping up shopkeeper money for {self._actor_label(mob)}: "
            f"wealth={wealth}, current={gold * 100 + silver}"
        )
        mob.gold = gold + (wealth * self.rng.number_range(1, 20) // 5000000)
        mob.silver = silver + (wealth * self.rng.number_range(1, 20) // 50000)

    async def execute_special_function(self, mob: Mobile, room) -> bool:
        lambdas = list(getattr(mob, "special_function", []) or [])
        if not lambdas:
            self.logger.debug(
                f"execute_special_function found no bound special lambdas for {self._actor_label(mob)} in {self._room_label(room)} "
                f"(special_name={str(getattr(mob, 'special_name', '') or '')!r})"
            )
            return False
        self.logger.debug(
            f"execute_special_function starting for {self._actor_label(mob)} in {self._room_label(room)} "
            f"with special_name={str(getattr(mob, 'special_name', '') or '')!r} and {len(lambdas)} lambda(s)"
        )
        context = MobileContext(actor=mob, room=room, handler=self, special_name=str(getattr(mob, "special_name", "") or ""))
        await self._execute_lambda_sequence(context, lambdas)
        await self._flush_context_payloads(context)
        self.logger.debug(
            f"execute_special_function completed for {self._actor_label(mob)} in {self._room_label(context.room)}: "
            f"performed={context.performed}, done={context.done}"
        )
        return bool(context.performed)

    def execute_special_by_name(self, mob: Mobile, special_name: str, room, context: MobileContext | None = None) -> bool:
        lambdas = self._special_library().get(str(special_name or "").strip().lower(), [])
        if not lambdas:
            self.logger.debug(
                f"execute_special_by_name found no library special for name={str(special_name or '')!r} "
                f"on {self._actor_label(mob)} in {self._room_label(room)}"
            )
            return False
        active_context = context or MobileContext(actor=mob, room=room, handler=self, special_name=str(special_name or ""))
        if special_name == "spec_wander":
            self.logger.debug(
                f"execute_special_by_name commencing={str(special_name or '')!r} for {self._actor_label(mob)} "
                f"in {self._room_label(active_context.room)} with {len(lambdas)} lambda(s)"
            )
        for lambda_str in lambdas:
            try:
                self.logger.debug(f"execute_special_by_name evaluating lambda for {self._actor_label(mob)}: {lambda_str}")
                func = eval(lambda_str)
            except Exception:
                self.logger.error(f"Invalid mobile special lambda: {lambda_str}", exc_info=True)
                return False
            if not callable(func):
                self.logger.debug(f"execute_special_by_name skipping non-callable lambda result for {self._actor_label(mob)}: {lambda_str}")
                continue
            result = func(active_context)
            if inspect.isawaitable(result):
                self.logger.warning(f"Async mobile special lambda is not supported in nested execution: {lambda_str}")
                continue
            self.logger.debug(
                f"execute_special_by_name lambda result for {self._actor_label(mob)}: "
                f"result={result!r}, performed={active_context.performed}, done={active_context.done}"
            )
            if active_context.done:
                break
        self.logger.debug(
            f"execute_special_by_name completed name={str(special_name or '')!r} for {self._actor_label(mob)}: "
            f"performed={active_context.performed}, done={active_context.done}"
        )
        return bool(active_context.performed)

    async def _execute_lambda_sequence(self, context: MobileContext, lambdas: list[str]):
        for lambda_str in lambdas:
            try:
                message = f"_execute_lambda_sequence evaluating {context.special_name!r} for {self._actor_label(context.actor)} in {self._room_label(context.room)}: {lambda_str}"
                self.logger.debug(message)
                func = eval(lambda_str)
                if not callable(func):
                    self.logger.debug(f"_execute_lambda_sequence skipping non-callable lambda for {self._actor_label(context.actor)}: {lambda_str}")
                    continue
                result = func(context)
                if inspect.isawaitable(result):
                    await result
                    message = f"_execute_lambda_sequence awaited lambda for {self._actor_label(context.actor)}: performed={context.performed}, done={context.done}"
                    self.logger.debug(message)
                else:
                    message = f"_execute_lambda_sequence lambda returned for {self._actor_label(context.actor)}: result={result!r}, performed={context.performed}, done={context.done}"
                    self.logger.debug(message)
            except Exception as exc:
                self.logger.error(f"Mobile special failed for {context.special_name or getattr(context.actor, 'special_name', '')}: {lambda_str} | {exc}", exc_info=True)
                break
            await self._flush_context_payloads(context)
            if context.done:
                message = f"_execute_lambda_sequence stopping early for {self._actor_label(context.actor)} because context.done is set for special {context.special_name!r}"
                self.logger.debug(message)
                break

    async def _flush_context_payloads(self, context: MobileContext):
        while context.payloads:
            payload = context.payloads.pop(0)
            self.logger.debug(
                f"_flush_context_payloads delivering payload for {self._actor_label(context.actor)} "
                f"in {self._room_label(context.room)} with keys={sorted(payload.keys())}"
            )
            await self._handle_payload(payload)

    async def _execute_generic_special(self, mob: Mobile, room, special_name: str) -> bool:
        context = MobileContext(actor=mob, room=room, handler=self, special_name=str(special_name or ""))
        self.logger.debug(
            f"_execute_generic_special starting name={str(special_name or '')!r} for {self._actor_label(mob)} "
            f"in {self._room_label(room)}"
        )
        self.execute_special_by_name(mob, special_name, room, context)
        await self._flush_context_payloads(context)
        self.logger.debug(
            f"_execute_generic_special completed name={str(special_name or '')!r} for {self._actor_label(mob)}: "
            f"performed={context.performed}, done={context.done}, room={self._room_label(context.room)}"
        )
        return bool(context.performed)

    async def _handle_payload(self, payload: dict):
        if payload.get("to_victim") and payload.get("victim") is not None and not CharacterApi.is_npc(payload["victim"]):
            await self.message_bus.send_to_character(payload["victim"].id, self.message_bus.text_to_message(payload["to_victim"]))
        if payload.get("to_room"):
            targets = payload.get("targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["to_room"]), targets)
        if payload.get("room_message"):
            targets = payload.get("room_targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["room_message"]), targets)
        if payload.get("global_message"):
            targets = payload.get("global_targets", [])
            if len(targets) > 0:
                await self.message_bus.send_to_room(self.message_bus.text_to_message(payload["global_message"]), targets)
        if payload.get("broadcast_message"):
            await self.message_bus.broadcast(self.message_bus.text_to_message(payload["broadcast_message"]), payload.get("exclude_character_ids", []))
        if payload.get("area_message"):
            await self._send_to_area(payload.get("area_id", ""), payload["area_message"])

    async def _send_to_area(self, area_id: str, text: str):
        message = self.message_bus.text_to_message(text)
        for room in self.room_registry.all_rooms():
            if room is None or str(getattr(room, "area_id", "") or "") != str(area_id or ""):
                continue
            for player in room.characters.values():
                await self.message_bus.send_to_character(player.id, message)

    def _resolve_room_for_mobile(self, room, mob: Mobile):
        if mob is None:
            return None
        try:
            resolved = MobileContext(actor=mob, room=room, handler=self)
            MobileApi.require_in_room(resolved)
            if resolved.room is not room:
                self.logger.debug(
                    f"_resolve_room_for_mobile changed room for {self._actor_label(mob)} from "
                    f"{self._room_label(room)} to {self._room_label(resolved.room)}"
                )
            return resolved.room
        except Exception:
            self.logger.error(f"_resolve_room_for_mobile failed for {self._actor_label(mob)}", exc_info=True)
            return room

    def _special_library(self) -> dict[str, list[str]]:
        if self._special_library_cache is None:
            library = {}
            for special in self.special_registry.all_specials():
                name = str(getattr(special, "name", "") or "").strip().lower()
                lambdas = list(getattr(special, "special_function", []) or [])
                if name and lambdas and name not in library:
                    library[name] = lambdas

            self._special_library_cache = library
            self.logger.info(f"_special_library built cache with {len(library)} special definition(s)")
        return self._special_library_cache

    @staticmethod
    def _actor_label(mob: Mobile | None) -> str:
        if mob is None:
            return "unknown-mobile"
        short_desc = str(getattr(mob, "short_description", "") or "").strip()
        vnum = str(getattr(mob, "vnum", "") or "").strip()
        mob_id = str(getattr(mob, "id", "") or "").strip()
        if short_desc:
            return f"{short_desc} [vnum={vnum}, id={mob_id}]"
        name = str(getattr(mob, "name", "unknown-mobile") or "unknown-mobile").strip()
        return f"{name} [vnum={vnum}, id={mob_id}]"

    @staticmethod
    def _room_label(room) -> str:
        if room is None:
            return "no-room"
        name = str(getattr(room, "name", "") or "").strip()
        vnum = str(getattr(room, "vnum", "") or "").strip()
        room_id = str(getattr(room, "id", "") or "").strip()
        return f"{name or 'unnamed-room'} [vnum={vnum}, id={room_id}]"
