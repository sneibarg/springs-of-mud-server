from injector import inject
from server.messaging import MessageBus
from server.LoggerFactory import LoggerFactory


class NoteHandler:
    @inject
    def __init__(self, message_bus: MessageBus):
        self.__name__ = "NoteHandler"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.message_bus = message_bus
