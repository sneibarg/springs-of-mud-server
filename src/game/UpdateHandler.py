import asyncio

from injector import inject
from area.AreaHandler import AreaHandler
from combat.CombatHandler import FightHandler
from game.EntityUpdateHandler import EntityUpdateHandler
from game.EnumProvider import EnumProvider
from item.ItemUpdateHandler import ItemUpdateHandler
from game.WeatherHandler import WeatherHandler
from mobile.MobileHandler import MobileHandler
from player.Character import Character
from player.CharacterService import CharacterService
from server.session.SessionHandler import SessionHandler


class UpdateHandler:
    """Schedule world pulses and coordinate active-player ticks and persistence."""

    @inject
    def __init__(self,
                 weather_handler: WeatherHandler,
                 area_handler: AreaHandler,
                 mobile_handler: MobileHandler,
                 fight_handler: FightHandler,
                 character_service: CharacterService,
                 session_handler: SessionHandler,
                 enum_provider: EnumProvider,
                 entity_update_handler: EntityUpdateHandler,
                 item_update_handler: ItemUpdateHandler):
        self.weather_handler = weather_handler
        self.area_handler = area_handler
        self.mobile_handler = mobile_handler
        self.fight_handler = fight_handler
        self.character_service = character_service
        self.session_handler = session_handler
        self.entity_update_handler = entity_update_handler
        self.item_update_handler = item_update_handler
        self.pulse_area = 0
        self.pulse_mobile = 0
        self.pulse_violence = 0
        self.pulse_point = 0
        self.pulse_music = 0  # maybe we skip migrating music
        self.save_cycle = 30
        self.save_number = 0
        self.GameParametersEnum = enum_provider.get("gameParameters")

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
            self.fight_handler.refresh_combat_registry_from_world()
            await self.fight_handler.violence_update()
        await self.fight_handler.aggression_update()

    async def char_update(self):
        if not self.entity_update_handler.enabled:
            return

        self._advance_save_counter()
        await self.entity_update_handler.update(self._active_player_characters())
        await self._autosave_due_characters()

    async def obj_update(self):
        await self.item_update_handler.update()

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

    def _advance_save_counter(self) -> None:
        self.save_number += 1
        if self.save_number >= self.save_cycle:
            self.save_number = 0

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
