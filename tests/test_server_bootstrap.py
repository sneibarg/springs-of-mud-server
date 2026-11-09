import sys
import unittest
from copy import deepcopy
from dataclasses import fields
from pathlib import Path
from unittest.mock import Mock, patch

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from devtools.collection_query import load_collections
from game.RegistryService import RegistryService
from server.Bootstrapper import Bootstrapper
from server.MudServer import MudServer
from server.ServiceConfig import ServiceConfig
from tests.test_update_handler_active_players import build_character_data


class ServerBootstrapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        collections = load_collections(ROOT / "resources/collections", ["commands", "gamedata"])
        cls.game_data = collections["gamedata"].documents
        cls.quit_command = next(doc for doc in collections["commands"].documents if doc["name"] == "quit")

    def setUp(self):
        self.addCleanup(Bootstrapper.reset_runtime)
        endpoints = {field.name: "/" + field.name.removesuffix("_endpoint") for field in fields(ServiceConfig)}
        self.config = {"mudserver": {
            "host": "127.0.0.1", "port": 0, "modulith_host": "content.invalid", "modulith_port": 80,
            "api_version": "/api", "services": {"endpoints": endpoints},
            "playerone": {"accountId": "acct_001"},
        }}
        self.documents = {path: [] for path in endpoints.values()}
        self.documents.update({
            "/game_data": deepcopy(self.game_data),
            "/players": [dict(id="acct_001", banned=False, accountName="test", firstName="Test",
                              lastName="Player", emailAddress="", password="", playerCharacterList=["char_001"])],
            "/characters": [build_character_data()],
            "/rooms": [dict(id="room_001", areaId="area_001", vnum="1", name="Test room")],
            "/areas": [dict(id="area_001", vnum="1", name="Test area", author="Test", suggestedLevelRange="1 10")],
            "/helps": [dict(id="summary-help", keyword="SUMMARY", text="Help summary")],
            "/commands": [dict(self.quit_command, function=[], usage="")],
        })
        self.fail_endpoint = None
        self.http_get = self.enterContext(patch("requests.get", side_effect=self.response))

    def response(self, url, *, timeout):
        self.assertEqual(10, timeout)
        endpoint = "/" + url.rsplit("/", 1)[-1]
        response = Mock(json=Mock(return_value=deepcopy(self.documents[endpoint])))
        if endpoint == self.fail_endpoint:
            response.raise_for_status.side_effect = requests.HTTPError("503 Service Unavailable")
        return response

    def start_server(self):
        return MudServer(self.config, Mock())

    def test_valid_content_bootstraps_with_empty_notes_and_optional_collections(self):
        server = self.start_server()
        registries = server.injector.get(RegistryService)
        room = registries.room_registry.get(id="room_001")
        area = registries.area_registry.get(id="area_001")
        self.assertIs(area, room.area)
        self.assertIn(room, area.rooms)
        self.assertIsNotNone(registries.interp_registry.get(name="quit"))
        self.assertIsNotNone(registries.interp_registry.get(name="summary"))
        self.assertEqual([], registries.note_registry.all_notes())
        self.assertEqual("acct_001", server.player_one.id)
        self.assertEqual(len(self.documents), self.http_get.call_count)

    def test_http_failure_from_any_bootstrap_endpoint_aborts_startup(self):
        for endpoint in self.documents:
            with self.subTest(endpoint=endpoint):
                self.fail_endpoint = endpoint
                with self.assertRaisesRegex(RuntimeError, rf"Failed to load .*{endpoint}"):
                    self.start_server()
                Bootstrapper.reset_runtime()

    def test_empty_core_collection_aborts_startup(self):
        for endpoint in ("/game_data", "/areas", "/rooms", "/commands"):
            with self.subTest(endpoint=endpoint):
                original = self.documents[endpoint]
                self.documents[endpoint] = []
                with self.assertRaisesRegex(RuntimeError, "Required collection is empty"):
                    self.start_server()
                self.documents[endpoint] = original
                Bootstrapper.reset_runtime()

    def test_malformed_documents_abort_startup_after_a_valid_document(self):
        self.documents["/rooms"].append(dict(id="bad-room", areaId="area_001", exits=[{"unknown": 1}]))
        with self.assertRaisesRegex(RuntimeError, "Failed to load rooms"):
            self.start_server()

    def test_missing_summary_help_aborts_command_bootstrap(self):
        self.documents["/helps"] = []
        with self.assertRaisesRegex(RuntimeError, "Failed to load commands.*summary"):
            self.start_server()

    def test_room_with_missing_area_aborts_startup(self):
        self.documents["/rooms"][0]["areaId"] = "missing"
        with self.assertRaisesRegex(ValueError, "Room room_001 refers to an unknown area"):
            self.start_server()

    def test_invalid_pulse_rate_aborts_startup(self):
        self.documents["/game_data"][0]["enums"]["gameParameters"]["PULSE_PER_SECOND"] = 0
        with self.assertRaisesRegex(ValueError, "PULSE_PER_SECOND must be positive"):
            self.start_server()
