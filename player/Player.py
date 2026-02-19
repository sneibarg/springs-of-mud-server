
import threading
from dataclasses import dataclass, field
from typing import Optional
from player import Character


@dataclass
class Player:
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
        return cls(**data)

    def reader(self):
        return self.connection[0]

    def writer(self):
        return self.connection[1]

    def print_visible(self, visible):
        who_list = [self.current_character] + visible
        players_found = "Players found: " + str(len(who_list)) + "\r\n"
        for character in who_list:
            who_line = "[{}\t{}\t{}] {} {}\r\n".format(str(character.level), character.race, character.character_class,
                                                       character.name, character.title)

            self.writer().write(who_line.encode('utf-8'))
        self.writer().write(b'\r\n')
        self.writer().write(players_found.encode('utf-8'))
        from utilities.player_util import bust_a_prompt
        bust_a_prompt(self)

    def to_player(self, message):
        message += "\r\n"
        self.writer().write(message.encode('utf-8'))
        from utilities.player_util import bust_a_prompt
        bust_a_prompt(self)

    def to_room(self, player_service, message, pattern):
        player_service.to_room(self, message, pattern)
        from utilities.player_util import bust_a_prompt
        bust_a_prompt(self)
