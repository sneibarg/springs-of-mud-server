from server.messaging import MessageBus
from server.protocol import Message, MessageType


class PlayerHandler:
    def __init__(self, message_bus: MessageBus):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus

    def print_visible(self, player_id, character, visible):
        who_list = [character] + visible
        who_line = ""
        players_found = "Players found: " + str(len(who_list)) + "\r\n"
        for character in who_list:
            who_line = "[{}\t{}\t{}] {} {}\r\n".format(str(character.level), character.race, character.character_class,
                                                       character.name, character.title)

        who_line = who_line + '\r\n' + players_found
        self.message_bus.send_to_character(player_id, Message(type=MessageType.GAME, data={"text": who_line}))

    def to_player(self, message):
        message += "\r\n"
        self.writer().write(message.encode('utf-8'))

    def to_room(self, player_service, message, pattern):
        player_service.to_room(self, message, pattern)