import unittest
from enum import IntEnum
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from tests.test_update_handler_active_players import Room
from game.WeatherHandler import WeatherHandler


class Weather(IntEnum):
    SUN_DARK = 0
    SUN_RISE = 1
    SUN_LIGHT = 2
    SUN_SET = 3
    SKY_CLOUDLESS = 0
    SKY_CLOUDY = 1
    SKY_RAINING = 2
    SKY_LIGHTNING = 3


class WeatherUpdateTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.bus = Mock(get_active_players=Mock(return_value=[]), send_to_character=AsyncMock())
        self.handler = WeatherHandler(self.bus, Mock(), SimpleNamespace(get=lambda name: Weather))
        self.handler.logger = Mock()

    def test_sky_pressure_boundaries_and_random_gates(self):
        # Each row is (sky, pressure, successful-roll result, failed-roll result, rolls).
        rows = [
            (0, 989, 1, 1, 0), (0, 990, 1, 0, 1), (0, 1009, 1, 0, 1), (0, 1010, 0, 0, 0),
            (1, 969, 2, 2, 0), (1, 970, 2, 1, 1), (1, 989, 2, 1, 1), (1, 990, 1, 1, 0),
            (1, 1030, 1, 1, 0), (1, 1031, 0, 1, 1), (1, 1040, 0, 1, 1),
            (2, 969, 3, 2, 1), (2, 970, 2, 2, 0), (2, 1000, 2, 2, 0), (2, 1010, 2, 2, 0),
            (2, 1011, 1, 2, 1), (2, 1030, 1, 2, 1), (2, 1031, 1, 1, 0), (2, 1040, 1, 1, 0),
            (3, 990, 3, 3, 0), (3, 991, 2, 3, 1), (3, 1010, 2, 3, 1), (3, 1011, 2, 2, 0),
        ]
        messages = {(0, 1): 'The sky is getting cloudy.', (1, 2): 'It starts to rain.',
                    (1, 0): 'The clouds disappear.', (2, 3): 'Lightning flashes in the sky.',
                    (2, 1): 'The rain stopped.', (3, 2): 'The lightning has stopped.'}
        for sky, pressure, success, failure, rolls in rows:
            for roll, expected in ((0, success), (1, failure)):
                with self.subTest(sky=sky, pressure=pressure, roll=roll):
                    self.handler.weather_info.sky = sky
                    self.handler.weather_info.mmhg = pressure
                    with patch('game.WeatherHandler.rng.number_bits', return_value=roll) as chance:
                        text = self.handler._sky_change()
                    self.assertEqual(expected, self.handler.weather_info.sky)
                    self.assertEqual(rolls, chance.call_count)
                    self.assertEqual(messages[(sky, expected)] + '\n\r' if sky != expected else '', text)
                    if rolls:
                        chance.assert_called_with(2)

    async def test_combined_notice_reaches_only_awake_outdoor_active_players(self):
        players = [SimpleNamespace(id=str(i), outside=outside, awake=awake)
                   for i, (outside, awake) in enumerate(((True, True), (True, False),
                                                         (False, True), (False, False)))]
        self.bus.get_active_players.return_value = players
        self.handler.time_info.hour = 4
        self.handler.weather_info.sky = Weather.SKY_CLOUDY
        self.handler.weather_info.mmhg = 1040
        with patch.object(self.handler, '_update_barometric_pressure'), patch(
                'game.WeatherHandler.rng.number_bits', return_value=0), patch(
                'game.WeatherHandler.CharacterApi.is_outside', side_effect=lambda ch: ch.outside), patch(
                'game.WeatherHandler.CharacterApi.is_awake', side_effect=lambda ch: ch.awake):
            await self.handler.update()
        self.bus.send_to_character.assert_awaited_once()
        character_id, message = self.bus.send_to_character.await_args.args
        self.assertEqual('0', character_id)
        self.assertEqual('The day has begun.\n\rThe clouds disappear.\n\r', message.data['text'])
        self.bus.broadcast.assert_not_called()

    async def test_invalid_sky_is_logged_and_reset_without_player_diagnostic(self):
        self.handler.weather_info.sky = 99
        with patch.object(self.handler, '_update_barometric_pressure'):
            await self.handler.update()
        self.handler.logger.error.assert_called_once_with('Weather_update: bad sky 99.')
        self.assertEqual(Weather.SKY_CLOUDLESS, self.handler.weather_info.sky)
        self.bus.send_to_character.assert_not_awaited()

    def test_time_notices_and_year_rollover(self):
        for hour, sunlight, text in ((4, Weather.SUN_LIGHT, 'The day has begun.'),
                                     (5, Weather.SUN_RISE, 'The sun rises in the east.'),
                                     (18, Weather.SUN_SET, 'The sun slowly disappears in the west.'),
                                     (19, Weather.SUN_DARK, 'The night has begun.')):
            self.handler.time_info.hour = hour
            self.assertEqual(text + '\n\r', self.handler._time_change())
            self.assertEqual(sunlight, self.handler.weather_info.sunlight)
        self.handler.time_info.hour = 23
        self.handler.time_info.day = 34
        self.handler.time_info.month = 16
        self.assertEqual('', self.handler._time_change())
        time = self.handler.time_info
        self.assertEqual((0, 0, 0, 2), (time.hour, time.day, time.month, time.year))

    def test_seasonal_pressure_thresholds_and_clamps(self):
        for month, pressure, expected_change in ((8, 1015, 2), (8, 1016, -2),
                                                  (9, 985, 2), (9, 986, -2),
                                                  (16, 986, -2), (0, 986, 2)):
            with self.subTest(month=month, pressure=pressure):
                self.handler.time_info.month = month
                weather = self.handler.weather_info
                weather.mmhg, weather.change = pressure, 0
                with patch('game.WeatherHandler.rng.dice', side_effect=[1, 2, 2]):
                    self.handler._update_barometric_pressure()
                self.assertEqual(expected_change, weather.change)
                self.assertEqual(pressure + expected_change, weather.mmhg)
        for pressure, change, dice, expected in ((1039, 11, [4, 12, 2], (1040, 12)),
                                                (961, -11, [1, 2, 12], (960, -12))):
            weather.mmhg, weather.change = pressure, change
            with patch('game.WeatherHandler.rng.dice', side_effect=dice):
                self.handler._update_barometric_pressure()
            self.assertEqual(expected, (weather.mmhg, weather.change))


if __name__ == '__main__':
    unittest.main()
