"""Command auditing shared by direct and nested interpreter execution."""

from injector import inject

from api.CharacterApi import CharacterApi
from game.WizHandler import WizHandler
from server.LoggerFactory import LoggerFactory
from server.messaging.MessageBus import MessageBus


class CommandAudit:
    @inject
    def __init__(self, wiz_handler: WizHandler, message_bus: MessageBus):
        self.wiz_handler = wiz_handler
        self.message_bus = message_bus
        self.logger = LoggerFactory.get_logger('commands')

    async def record(self, actor, command, raw_command):
        mode = str(getattr(command, 'log', '') or '').upper()
        text = '' if mode == 'LOG_NEVER' else str(raw_command or '').lstrip()
        session = self.wiz_handler.current_session(actor)
        await self.message_bus.mirror_snoop_input(session, text)
        if not (self.wiz_handler.log_all or mode == 'LOG_ALWAYS'
                or CharacterApi.has_player_flag(actor, 'PLR_LOG')):
            return
        line = f"Log {actor.name}: {text}"
        self.logger.info('%s', line)
        for recipient in self.wiz_handler.wiznet_targets(actor, flag_name='WIZ_SECURE',
                                                       min_level=CharacterApi.get_trust(actor)):
            rendered = self.wiz_handler.decorate_wiznet_text(recipient, line + '\r\n')
            await self.message_bus.send_to_character(recipient.id, self.message_bus.text_to_message(rendered))
