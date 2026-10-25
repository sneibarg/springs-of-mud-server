from queue import SimpleQueue, Empty

from injector import inject
from game.WizHandler import WizHandler
from player.CharacterService import CharacterService
from server.messaging.MessageBus import MessageBus


class AdvancementHandler:
    """Persist synchronous level gains and deliver notices on the world loop."""

    @inject
    def __init__(self, character_service: CharacterService, wiz_handler: WizHandler, message_bus: MessageBus):
        self.character_service = character_service
        self.wiz_handler = wiz_handler
        self.message_bus = message_bus
        self.pending = SimpleQueue()

    def level_gained(self, character, result):
        self.character_service.save_character(character)
        self.pending.put((character, f"{character.name} has attained level {result.level}!"))

    async def flush(self):
        while True:
            try:
                character, text = self.pending.get_nowait()
            except Empty:
                return
            for recipient in self.wiz_handler.wiznet_targets(character, flag_name="WIZ_LEVELS"):
                decorated = self.wiz_handler.decorate_wiznet_text(recipient, text)
                await self.message_bus.send_to_character(recipient.id, self.message_bus.text_to_message(decorated))
