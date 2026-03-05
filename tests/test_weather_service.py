import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest

from unittest.mock import Mock, AsyncMock, patch
from update import WeatherService, WeatherInfo, TimeInfo, SUN_DARK, SUN_LIGHT, SUN_RISE, SUN_SET, SKY_CLOUDLESS, SKY_CLOUDY, SKY_RAINING, SKY_LIGHTNING


class TestWeatherService(unittest.TestCase):
    """Test WeatherService"""

    def setUp(self):
        # Mock dependencies
        self.mock_message_bus = Mock()
        self.mock_message_bus.send_to_outdoor_players = AsyncMock()

        self.mock_player_service = Mock()
        self.mock_player_service.registry_service = Mock()
        self.mock_player_service.registry_service.character_registry = {}

        self.mock_room_service = Mock()

        self.mock_game_data = Mock()
        self.mock_game_data.constants = Mock()
        self.mock_game_data.constants.pulses = {
            'perSecond': 4,
            'tick': 240
        }

        self.weather_service = WeatherService(
            self.mock_message_bus,
            self.mock_player_service,
            self.mock_room_service,
            self.mock_game_data
        )

    def test_initialization(self):
        """Test WeatherService initialization"""
        self.assertIsNotNone(self.weather_service.logger)
        self.assertIsInstance(self.weather_service.weather_info, WeatherInfo)
        self.assertIsInstance(self.weather_service.time_info, TimeInfo)
        self.assertEqual(self.weather_service.pulse_count, 0)
        self.assertEqual(self.weather_service.pulse_tick, 240)

        # Check initial weather state
        self.assertEqual(self.weather_service.weather_info.mmhg, 1000)
        self.assertEqual(self.weather_service.weather_info.change, 0)
        self.assertEqual(self.weather_service.weather_info.sky, SKY_CLOUDLESS)
        self.assertEqual(self.weather_service.weather_info.sunlight, SUN_LIGHT)

        # Check initial time state
        self.assertEqual(self.weather_service.time_info.hour, 0)
        self.assertEqual(self.weather_service.time_info.day, 1)
        self.assertEqual(self.weather_service.time_info.month, 1)
        self.assertEqual(self.weather_service.time_info.year, 1)

    async def test_update_does_not_trigger_before_pulse_tick(self):
        """Test that update doesn't trigger before pulse_tick is reached"""
        # Update 239 times (just before pulse_tick)
        for i in range(239):
            await self.weather_service.update()

        # Should not have called send_to_outdoor_players yet
        self.mock_message_bus.send_to_outdoor_players.assert_not_called()
        self.assertEqual(self.weather_service.pulse_count, 239)

    async def test_update_triggers_at_pulse_tick(self):
        """Test that update triggers at pulse_tick"""
        # Update 240 times (reaching pulse_tick)
        for i in range(240):
            await self.weather_service.update()

        # Should reset pulse count
        self.assertEqual(self.weather_service.pulse_count, 0)

        # Time should have advanced by 1 hour
        self.assertEqual(self.weather_service.time_info.hour, 1)

    def test_time_change_hour_5(self):
        """Test time change at hour 5 (day begins)"""
        self.weather_service.time_info.hour = 4
        message = self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.hour, 5)
        self.assertEqual(self.weather_service.weather_info.sunlight, SUN_LIGHT)
        self.assertEqual(message, "The day has begun\n\r")

    def test_time_change_hour_6(self):
        """Test time change at hour 6 (sunrise)"""
        self.weather_service.time_info.hour = 5
        message = self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.hour, 6)
        self.assertEqual(self.weather_service.weather_info.sunlight, SUN_RISE)
        self.assertEqual(message, "The sun rises in the east.\n\r")

    def test_time_change_hour_19(self):
        """Test time change at hour 19 (sunset)"""
        self.weather_service.time_info.hour = 18
        message = self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.hour, 19)
        self.assertEqual(self.weather_service.weather_info.sunlight, SUN_SET)
        self.assertEqual(message, "The sun slowly disappears in the west.\n\r")

    def test_time_change_hour_20(self):
        """Test time change at hour 20 (night begins)"""
        self.weather_service.time_info.hour = 19
        message = self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.hour, 20)
        self.assertEqual(self.weather_service.weather_info.sunlight, SUN_DARK)
        self.assertEqual(message, "The night has begun\n\r")

    def test_time_change_hour_24_rolls_to_day_2(self):
        """Test time change at hour 24 rolls to next day"""
        self.weather_service.time_info.hour = 23
        message = self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.hour, 0)
        self.assertEqual(self.weather_service.time_info.day, 2)
        self.assertEqual(message, "")

    def test_time_change_day_35_rolls_to_month_2(self):
        """Test day 35 rolls to next month"""
        self.weather_service.time_info.hour = 23
        self.weather_service.time_info.day = 34

        self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.day, 0)
        self.assertEqual(self.weather_service.time_info.month, 2)

    def test_time_change_month_17_rolls_to_year_2(self):
        """Test month 17 rolls to next year"""
        self.weather_service.time_info.hour = 23
        self.weather_service.time_info.day = 34
        self.weather_service.time_info.month = 16

        self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.month, 0)
        self.assertEqual(self.weather_service.time_info.year, 2)

    def test_time_change_regular_hour(self):
        """Test time change for regular hour (no message)"""
        self.weather_service.time_info.hour = 10
        message = self.weather_service._time_change()

        self.assertEqual(self.weather_service.time_info.hour, 11)
        self.assertEqual(message, "")

    def test_weather_change_winter_months(self):
        """Test weather change during winter months (9-16)"""
        self.weather_service.time_info.month = 10
        self.weather_service.weather_info.mmhg = 1000
        initial_mmhg = self.weather_service.weather_info.mmhg

        self.weather_service._update_barometric_pressure()

        # Should have changed
        self.assertNotEqual(self.weather_service.weather_info.mmhg, initial_mmhg)
        # Should be within valid range
        self.assertGreaterEqual(self.weather_service.weather_info.mmhg, 960)
        self.assertLessEqual(self.weather_service.weather_info.mmhg, 1040)

    @patch("update.WeatherService.rng")
    def test_weather_change_summer_months(self, mock_rng):
        self.weather_service.time_info.month = 5
        self.weather_service.weather_info.mmhg = 1000
        initial = self.weather_service.weather_info.mmhg

        # Force: diff=2, dice(1,4)=4, dice(2,6)=12 then 2  => change += 2*4 + 12 - 2 = 18
        mock_rng.dice.side_effect = [4, 12, 2]

        self.weather_service._update_barometric_pressure()

        self.assertNotEqual(self.weather_service.weather_info.mmhg, initial)
        self.assertGreaterEqual(self.weather_service.weather_info.mmhg, 960)
        self.assertLessEqual(self.weather_service.weather_info.mmhg, 1040)

    def test_weather_change_constrains_change_value(self):
        """Test that weather change is constrained to -12 to 12"""
        self.weather_service.weather_info.change = 0

        # Run multiple times to test constraints
        for _ in range(20):
            self.weather_service._update_barometric_pressure()
            self.assertGreaterEqual(self.weather_service.weather_info.change, -12)
            self.assertLessEqual(self.weather_service.weather_info.change, 12)

    def test_weather_change_constrains_mmhg_value(self):
        """Test that mmhg is constrained to 960-1040"""
        # Test lower bound
        self.weather_service.weather_info.mmhg = 960
        self.weather_service.weather_info.change = -50
        self.weather_service._update_barometric_pressure()
        self.assertGreaterEqual(self.weather_service.weather_info.mmhg, 960)

        # Test upper bound
        self.weather_service.weather_info.mmhg = 1040
        self.weather_service.weather_info.change = 50
        self.weather_service._update_barometric_pressure()
        self.assertLessEqual(self.weather_service.weather_info.mmhg, 1040)

    @patch('update.WeatherService.rng')
    def test_sky_change_cloudless_to_cloudy(self, mock_rng):
        """Test sky transition from cloudless to cloudy"""
        mock_rng.number_bits.return_value = 0  # chance() returns True
        self.weather_service.weather_info.sky = SKY_CLOUDLESS
        self.weather_service.weather_info.mmhg = 985  # Low pressure

        message = self.weather_service._sky_change()

        self.assertEqual(self.weather_service.weather_info.sky, SKY_CLOUDY)
        self.assertEqual(message, "The sky is getting cloudy.\n\r")

    @patch('update.WeatherService.rng')
    def test_sky_change_cloudy_to_raining(self, mock_rng):
        """Test sky transition from cloudy to raining"""
        mock_rng.number_bits.return_value = 0  # chance() returns True
        self.weather_service.weather_info.sky = SKY_CLOUDY
        self.weather_service.weather_info.mmhg = 965  # Very low pressure

        message = self.weather_service._sky_change()

        self.assertEqual(self.weather_service.weather_info.sky, SKY_RAINING)
        self.assertEqual(message, "It starts to rain.\n\r")

    @patch('update.WeatherService.rng')
    def test_sky_change_raining_to_lightning(self, mock_rng):
        """Test sky transition from raining to lightning"""
        mock_rng.number_bits.return_value = 0  # chance() returns True
        self.weather_service.weather_info.sky = SKY_RAINING
        self.weather_service.weather_info.mmhg = 965  # Very low pressure

        message = self.weather_service._sky_change()

        self.assertEqual(self.weather_service.weather_info.sky, SKY_LIGHTNING)
        self.assertEqual(message, "Lightning flashes in the sky.\n\r")

    @patch('update.WeatherService.rng')
    def test_sky_change_lightning_to_raining(self, mock_rng):
        """Test sky transition from lightning to raining"""
        mock_rng.number_bits.return_value = 0  # chance() returns True
        self.weather_service.weather_info.sky = SKY_LIGHTNING
        self.weather_service.weather_info.mmhg = 1020  # Rising pressure

        message = self.weather_service._sky_change()

        self.assertEqual(self.weather_service.weather_info.sky, SKY_RAINING)
        self.assertEqual(message, "The lightning has stopped.\n\r")

    def test_is_player_outdoors_no_character(self):
        """Test is_player_outdoors when character doesn't exist"""
        result = self.weather_service._is_player_outdoors("nonexistent_id")
        self.assertFalse(result)

    def test_is_player_outdoors_with_outdoor_room(self):
        """Test is_player_outdoors when player is outdoors"""
        mock_character = Mock()
        mock_character.room_id = "room_123"

        mock_room = Mock()

        self.mock_player_service.registry_service.character_registry = {
            "player_123": mock_character
        }
        self.mock_room_service.get_room.return_value = mock_room
        self.mock_room_service.is_outside.return_value = True

        result = self.weather_service._is_player_outdoors("player_123")

        self.assertTrue(result)
        self.mock_room_service.get_room.assert_called_once_with("room_123")
        self.mock_room_service.is_outside.assert_called_once_with(mock_room)

    def test_is_player_outdoors_with_indoor_room(self):
        """Test is_player_outdoors when player is indoors"""
        mock_character = Mock()
        mock_character.room_id = "room_123"

        mock_room = Mock()

        self.mock_player_service.registry_service.character_registry = {
            "player_123": mock_character
        }
        self.mock_room_service.get_room.return_value = mock_room
        self.mock_room_service.is_outside.return_value = False

        result = self.weather_service._is_player_outdoors("player_123")

        self.assertFalse(result)

    async def test_time_update_with_message(self):
        """Test time_update sends message when there is a time change"""
        self.weather_service.time_info.hour = 4  # Will change to hour 5

        await self.weather_service.time_update()

        # Should have sent a message
        self.mock_message_bus.send_to_outdoor_players.assert_called_once()
        call_args = self.mock_message_bus.send_to_outdoor_players.call_args
        message = call_args[0][0]
        self.assertEqual(message.data['text'], "The day has begun\n\r")

    async def test_time_update_without_message(self):
        """Test time_update doesn't send message for regular hours"""
        self.weather_service.time_info.hour = 10  # Regular hour

        await self.weather_service.time_update()

        # Should not have sent a message
        self.mock_message_bus.send_to_outdoor_players.assert_not_called()

    @patch('update.WeatherService.rng')
    async def test_sky_update_with_message(self, mock_rng):
        """Test sky_update sends message when weather changes"""
        mock_rng.number_bits.return_value = 0
        self.weather_service.weather_info.sky = SKY_CLOUDLESS
        self.weather_service.weather_info.mmhg = 985

        await self.weather_service.sky_update()

        # Should have sent a message
        self.mock_message_bus.send_to_outdoor_players.assert_called_once()
        call_args = self.mock_message_bus.send_to_outdoor_players.call_args
        message = call_args[0][0]
        self.assertEqual(message.data['text'], "The sky is getting cloudy.\n\r")

    async def test_sky_update_without_message(self):
        """Test sky_update doesn't send message when no weather change"""
        self.weather_service.weather_info.sky = SKY_CLOUDLESS
        self.weather_service.weather_info.mmhg = 1020  # High pressure, won't change

        await self.weather_service.sky_update()

        # Should not have sent a message
        self.mock_message_bus.send_to_outdoor_players.assert_not_called()


if __name__ == '__main__':
    unittest.main()
