from server.protocol import Message, MessageType


class MessageFormatter:
    """
    Formats system and infrastructure messages.
    For game-specific messages (say, tell, emote, etc.), use CommunicationService.
    For room descriptions, use RoomService.
    For prompts, use PromptService.
    """

    @staticmethod
    def format_error(error_text: str) -> Message:
        """Format an error message"""
        return Message(
            type=MessageType.ERROR,
            data={'text': f"ERROR: {error_text}\r\n"}
        )

    @staticmethod
    def format_system(text: str) -> Message:
        """Format a system message"""
        if not text.endswith('\r\n'):
            text += '\r\n'

        return Message(
            type=MessageType.SYSTEM,
            data={'text': text}
        )
