import unittest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch

from game import GameService
from game import GameData, Version, Constants, Integrity, BuildInfo
from server.ServiceConfig import ServiceConfig
from server.TimeVal import TimeVal


class TestGameService(unittest.IsolatedAsyncioTestCase):
    """Test GameService"""

    def setUp(self):
        """Set up test fixtures"""
        self.game_data_endpoint = "http://test.endpoint/game-data"
        self.mock_service_config = ServiceConfig(
            game_data_endpoint=self.game_data_endpoint,
            commands_endpoint="http://test/commands",
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles",
        )

        # Optional: keep around if you later want to inject directly rather than mocking HTTP
        self.mock_game_data = self._create_mock_game_data()

    def _create_mock_game_data(self) -> GameData:
        """Create a mock GameData object for testing"""
        return GameData(
            id="test-game",
            kind="mud",
            status="active",
            version=Version(
                family="test",
                lineage=["v1"],
                semver="1.0.0",
                created_at=datetime.now(timezone.utc),
                notes="Test version",
            ),
            constants=Constants(
                max={"players": 100, "level": 50},
                pulses={"perSecond": 4},
            ),
            enums={"directions": ["north", "south", "east", "west"]},
            flags={"room": {"DARK": 1, "NO_MOB": 2}},
            well_known_vnums={"temple": {"room": 3001}},
            integrity=Integrity(
                content_hash="abc123",
                build=BuildInfo(source="test", tool_version="1.0.0", extra={}),
            ),
        )

    def _create_game_data_dict(self) -> dict:
        """Create a dictionary representation of game data for JSON mocking"""
        return {
            # Prefer _id to match Mongo-style docs; GameData.from_json should tolerate either.
            "_id": "test-game",
            "kind": "mud",
            "status": "active",
            "version": {
                "family": "test",
                "lineage": ["v1"],
                "semver": "1.0.0",
                "createdAt": "2024-01-01T00:00:00Z",
                "notes": "Test version",
            },
            "constants": {
                "max": {"players": 100, "level": 50},
                "pulses": {"perSecond": 4},
            },
            "enums": {"directions": ["north", "south", "east", "west"]},
            "flags": {"room": {"DARK": 1, "NO_MOB": 2}},
            # Flat catalogs per your refactor
            "classes": {},
            "races": {},
            "pcRaces": {},
            "skills": {},
            "groups": {},
            "weapons": {},
            "attacks": {},
            "liquids": {},
            # Optional name indexes
            "classesNameIndex": {},
            "racesNameIndex": {},
            "pcRacesNameIndex": {},
            "skillsNameIndex": {},
            "groupsNameIndex": {},
            "weaponsNameIndex": {},
            "attacksNameIndex": {},
            "liquidsNameIndex": {},
            "wellKnownVnums": {"temple": {"room": 3001}},
            "integrity": {
                "contentHash": "abc123",
                "build": {
                    "source": "test",
                    "toolVersion": "1.0.0",
                },
            },
        }

    @patch("game.GameService.requests.get")
    def test_initialization(self, mock_get):
        """Test GameService initialization"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        service = GameService(self.mock_service_config)

        self.assertEqual(service.__name__, "GameService")
        self.assertEqual(service.game_data_endpoint, self.game_data_endpoint)
        self.assertIsNotNone(service.game_data)
        self.assertIsNotNone(service.last_time)
        self.assertIsNotNone(service.logger)

        mock_get.assert_called_once_with(self.game_data_endpoint)

    @patch("game.GameService.requests.get")
    def test_load_game_data_success(self, mock_get):
        """Test successful game data loading"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        service = GameService(self.mock_service_config)

        self.assertIsInstance(service.game_data, GameData)
        self.assertEqual(service.game_data.id, "test-game")
        self.assertEqual(service.game_data.constants.pulses["perSecond"], 4)

    @patch("game.GameService.LoggerFactory.get_logger")
    @patch("game.GameService.requests.get")
    def test_load_game_data_failure(self, mock_get, mock_logger):
        """Test game data loading failure"""
        mock_get.side_effect = Exception("Network error")
        mock_logger.return_value = Mock()

        with self.assertRaises(RuntimeError) as context:
            GameService(self.mock_service_config)

        self.assertIn("Failed to load game data", str(context.exception))

    @patch("game.GameService.LoggerFactory.get_logger")
    @patch("game.GameService.requests.get")
    def test_load_game_data_invalid_response(self, mock_get, mock_logger):
        """Test game data loading with invalid response"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        mock_logger.return_value = Mock()

        with self.assertRaises(RuntimeError):
            GameService(self.mock_service_config)

    @patch("game.GameService.requests.get")
    @patch("game.GameService.stall_until_last_time")
    @patch("game.GameService.gettimeofday")
    async def test_game_loop_iteration(self, mock_gettimeofday, mock_stall, mock_get):
        """Test single game loop iteration"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        mock_time = TimeVal(tv_sec=1000, tv_usec=500000)
        mock_gettimeofday.return_value = mock_time

        service = GameService(self.mock_service_config)

        # update() is awaited, so it must be AsyncMock
        mock_weather_service = Mock()
        mock_weather_service.update = AsyncMock(return_value=None)
        service.set_weather_service(mock_weather_service)

        await service._game_loop_iteration()

        self.assertEqual(service.last_time, mock_time)
        mock_stall.assert_called_once_with(mock_time, 4)
        mock_weather_service.update.assert_awaited_once()

    @patch("game.GameService.requests.get")
    @patch("game.GameService.stall_until_last_time")
    @patch("game.GameService.gettimeofday")
    async def test_game_loop_multiple_iterations(self, mock_gettimeofday, mock_stall, mock_get):
        """Test multiple game loop iterations"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        iteration_count = 0

        def mock_gettimeofday_side_effect():
            nonlocal iteration_count
            iteration_count += 1
            return TimeVal(tv_sec=1000 + iteration_count, tv_usec=500000)

        mock_gettimeofday.side_effect = mock_gettimeofday_side_effect

        service = GameService(self.mock_service_config)

        mock_weather_service = Mock()
        mock_weather_service.update = AsyncMock(return_value=None)
        service.set_weather_service(mock_weather_service)

        for _ in range(3):
            await service._game_loop_iteration()

        self.assertEqual(mock_stall.call_count, 3)
        self.assertEqual(mock_weather_service.update.await_count, 3)
        self.assertEqual(service.last_time.tv_sec, 1004)

    @patch("game.GameService.requests.get")
    async def test_start_method(self, mock_get):
        """Test start method calls game_loop"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        service = GameService(self.mock_service_config)

        # Mock game_loop to prevent infinite loop
        service.game_loop = AsyncMock()

        await service.start()

        service.game_loop.assert_awaited_once()

    @patch("game.GameService.requests.get")
    def test_game_data_endpoint_property(self, mock_get):
        """Test game data endpoint is stored correctly"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        endpoint = "http://custom.endpoint/data"
        custom_config = ServiceConfig(
            game_data_endpoint=endpoint,
            commands_endpoint="http://test/commands",
            players_endpoint="http://test/players",
            characters_endpoint="http://test/characters",
            rooms_endpoint="http://test/rooms",
            areas_endpoint="http://test/areas",
            items_endpoint="http://test/items",
            mobiles_endpoint="http://test/mobiles",
        )
        service = GameService(custom_config)

        self.assertEqual(service.game_data_endpoint, endpoint)

    @patch("game.GameService.requests.get")
    def test_logger_creation(self, mock_get):
        """Test logger is created with correct name"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        service = GameService(self.mock_service_config)

        self.assertIsNotNone(service.logger)
        self.assertEqual(service.__name__, "GameService")

    @patch("game.GameService.requests.get")
    @patch("game.GameService.gettimeofday")
    def test_last_time_initialization(self, mock_gettimeofday, mock_get):
        """Test last_time is initialized on service creation"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        initial_time = TimeVal(tv_sec=1000, tv_usec=0)
        mock_gettimeofday.return_value = initial_time

        service = GameService(self.mock_service_config)

        self.assertEqual(service.last_time, initial_time)

    @patch("game.GameService.requests.get")
    @patch("game.GameService.gettimeofday")
    @patch("game.GameService.stall_until_last_time")
    async def test_game_loop_updates_last_time(self, mock_stall, mock_gettimeofday, mock_get):
        """Test that game loop iteration updates last_time"""
        mock_response = Mock()
        mock_response.json.return_value = [self._create_game_data_dict()]
        mock_get.return_value = mock_response

        # __init__ calls gettimeofday once, and _game_loop_iteration calls it again.
        time1 = TimeVal(tv_sec=1000, tv_usec=0)
        time2 = TimeVal(tv_sec=1001, tv_usec=250000)
        mock_gettimeofday.side_effect = [time1, time2]

        service = GameService(self.mock_service_config)
        initial_time = service.last_time

        mock_weather_service = Mock()
        mock_weather_service.update = AsyncMock(return_value=None)
        service.set_weather_service(mock_weather_service)

        await service._game_loop_iteration()

        self.assertNotEqual(service.last_time, initial_time)
        self.assertEqual(service.last_time, time2)

    @patch("game.GameService.requests.get")
    def test_pulses_per_second_from_game_data(self, mock_get):
        """Test that pulses per second is read from game data"""
        game_data_dict = self._create_game_data_dict()
        game_data_dict["constants"]["pulses"]["perSecond"] = 8

        mock_response = Mock()
        mock_response.json.return_value = [game_data_dict]
        mock_get.return_value = mock_response

        service = GameService(self.mock_service_config)

        self.assertEqual(service.game_data.constants.pulses["perSecond"], 8)


if __name__ == "__main__":
    unittest.main()
