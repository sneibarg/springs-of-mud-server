from typing import Optional, List
from injector import inject
from area.Exit import Exit
from area.Room import Room
from area.RoomRegistry import RoomRegistry
from area.AreaRegistry import AreaRegistry
from item.ExtraDescriptionData import ExtraDescriptionData
from server.FetchAndRegisterMixin import FetchAndRegisterMixin
from server.LoggerFactory import LoggerFactory
from server.ServiceConfig import ServiceConfig
from util.GenericUtil import GenericUtil


class RoomService(FetchAndRegisterMixin):
    log_fetch_list_count = False

    @inject
    def __init__(self, config: ServiceConfig, room_registry: RoomRegistry, area_registry: AreaRegistry):
        self.__name__ = "RoomService"
        self.rooms_endpoint = config.rooms_endpoint
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.room_registry = room_registry
        self.area_registry = area_registry
        self.load_rooms()
        self.logger.info(f"Initialized RoomService instance with {len(self.room_registry.all_rooms())} rooms in memory.")

    def reload_rooms(self) -> None:
        self.logger.info("Reloading rooms...")
        self.room_registry.reset()
        self.load_rooms()
        self.logger.info("Rooms reload completed.")

    def load_rooms(self):
        self._fetch_and_register(self.rooms_endpoint, "rooms")

    def load_room(self, room_name: str):
        url = f"{self.rooms_endpoint}/name/{room_name}"
        return self._fetch_and_register(url, f"room '{room_name}'")

    def _build_fetch_item(self, room_data) -> Room:
        room_data = GenericUtil.camel_to_snake_case(room_data)
        room = Room.from_json(room_data)
        room.exits = self._load_exits(room_data)
        room.extra_description = self._load_extra_description(room_data)
        return room

    def _register_fetch_item(self, room: Room) -> None:
        room.bind_area(self.area_registry.get_or_none(id=room.area_id))
        self.room_registry.register(room)

    def _load_extra_description(self, room_json: dict) -> Optional[ExtraDescriptionData]:
        extra_desc = str(room_json.get('extra_description'))
        if extra_desc is None:
            return None
        if not isinstance(extra_desc, str):
            self.logger.warning(f"Expected extra description to be a string, got {type(extra_desc).__name__}")
        return ExtraDescriptionData.from_json(extra_desc)

    def _load_exits(self, room_json: dict) -> List[Exit]:
        exit_list = []
        room_id = room_json.get('id') or room_json.get('vnum') or "unknown"

        try:
            room_exits = room_json.get('exits') or []
            if not isinstance(room_exits, list):
                raise TypeError(f"Expected exits to be a list, got {type(room_exits).__name__}")

            for index, raw_exit in enumerate(room_exits):
                try:
                    exit_obj = Exit.from_json(raw_exit)
                    if exit_obj.room_id is None:
                        exit_obj.room_id = str(room_id)
                    exit_list.append(exit_obj)
                except (TypeError, ValueError) as exit_error:
                    self.logger.warning(f"Skipping malformed exit #{index} for room {room_id}: {exit_error}")
        except (TypeError, ValueError) as e:
            self.logger.error(f"Failed to parse exits for room {room_id}: {e}")
        return exit_list
