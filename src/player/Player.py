import threading

from dataclasses import dataclass, field
from typing import Optional
from player.Character import Character


@dataclass
class Player:
    banned: bool
    first_name: str
    last_name: str
    account_name: str
    email_address: str
    password: str
    player_character_list: list
    id: str
    current_character: Character = field(default=None)
    connection: Optional[tuple] = field(default=None)
    session_id: Optional[str] = field(default=None)
    ansi_enabled: Optional[bool] = field(default=False)
    usage: Optional[str] = field(default=None)
    lock: Optional[threading.Lock] = field(default=None)

    def __post_init__(self):
        self.lock = threading.Lock()
        from server.LoggerFactory import LoggerFactory
        self.logger = LoggerFactory.get_logger(__name__)
        self.logger.info("Instantiated Player account " + self.account_name)

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        data = ServerUtil.camel_to_snake_case(data)
        return cls(**data)
