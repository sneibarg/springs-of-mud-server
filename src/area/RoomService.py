from typing import Optional, List, Any
from injector import inject

from game import GameData
from .RomRoom import RomRoom
from registry import RegistryService
from server.LoggerFactory import LoggerFactory
from server.protocol import Message, MessageType
from server.ServiceConfig import ServiceConfig


class RoomService:
    @inject
    def __init__(self, config: ServiceConfig, registry: RegistryService, game_data: GameData):
        self.rooms_endpoint = config.rooms_endpoint
        self.logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.registry = registry
        self.game_data = game_data
        self.logger.info("Initialized RoomService instance.")

    def is_outside(self, room: RomRoom) -> bool:
        """Check if a room is outdoors based on its flags."""
        self.logger.info(f"is_outside: {room.room_flags}={self.game_data.flags['room']['INDOORS']}")
        return (room.room_flags & self.game_data.flags['room']["INDOORS"]) == 0

    def get_room(self, room_id) -> RomRoom | None:
        if room_id is None:
            self.logger.debug("get_room: room_id is None")
            return None
        if room_id not in self.registry.room_registry:
            self.logger.debug("get_room: room_id="+str(room_id)+" not in registry.")
            return None
        return self.registry.room_registry[room_id]

    def print_room(self, writer, character):
        room: RomRoom = self.registry.room_registry[character.room_id]
        writer.write(f'[{room.name}]'.encode('utf-8'))
        room.print_description(writer, room)
        self.print_exits(writer, room)

    def print_exits(self, writer, room):
        writer.write(str("Exits: ").encode('utf-8'))
        for room_exit in room.get_exits():
            if room_exit is not None and isinstance(room_exit, str):
                room = self.get_room(room_exit)
                if room is not None:
                    writer.write(str(room.name + " ").encode('utf-8'))
                else:
                    self.logger.debug("print_exits: get_room returned None.")
        writer.write("\r\n".encode('utf-8'))

    def format_room_description(self, room_name: str, description: str, exits: list) -> Message:
        text = f"[{room_name}]\r\n{description}\r\n"
        if exits:
            exits_text = "Exits: " + ", ".join(exits) + "\r\n"
            text += exits_text

        return Message(
            type=MessageType.ROOM_DESCRIPTION,
            data={
                'text': text,
                'room_name': room_name,
                'description': description,
                'exits': exits
            }
        )

    async def send_to_room(self, room_id: str, message: Message, message_bus,
                          exclude_player_ids: Optional[List[str]] = None) -> int:
        exclude = exclude_player_ids or []
        count = 0
        sessions = message_bus.session_handler.get_playing_sessions()
        for session in sessions:
            if session.player_id in exclude:
                continue

            if await message_bus.send_to_player(session.player_id, message):
                count += 1

        return count
