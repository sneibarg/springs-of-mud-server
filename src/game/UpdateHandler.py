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
        self.stop_flag = False

    async def handle_updates(self):
        await self.weather_handler.update()

