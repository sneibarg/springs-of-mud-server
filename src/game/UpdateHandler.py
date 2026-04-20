from enum import IntEnum
from injector import inject
from area.AreaHandler import AreaHandler
from game.WeatherHandler import WeatherHandler
from mobile.MobileHandler import MobileHandler


class UpdateHandler:
    @inject
    def __init__(self, weather_handler: WeatherHandler, area_handler: AreaHandler, mobile_handler: MobileHandler):
        self.weather_handler = weather_handler
        self.area_handler = area_handler
        self.mobile_handler = mobile_handler
        self.enums: dict[str, IntEnum] = {}
        self.pulse_area = 0
        self.pulse_mobile = 0
        self.pulse_violence = 0
        self.pulse_point = 0
        self.pulse_music = 0  # maybe we skip migrating music
        self.GameParametersEnum = None

    def set_enums(self, enums: dict[str, IntEnum]):
        self.enums = enums
        self.GameParametersEnum = enums.get('gameParameters')
        self.mobile_handler.set_enums(enums)

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
        if self.pulse_music <= 0:
            self.pulse_music = self.GameParametersEnum.PULSE_MUSIC.value
        if self.pulse_mobile <= 0:
            self.pulse_mobile = self.GameParametersEnum.PULSE_MOBILE.value
            await self.mobile_handler.mobile_update()
        if self.pulse_violence <= 0:
            self.pulse_violence = self.GameParametersEnum.PULSE_VIOLENCE.value

