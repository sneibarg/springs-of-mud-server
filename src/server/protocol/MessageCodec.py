import json
from typing import Union
from .Message import Message
from .MessageTypes import MessageType


class MessageCodec:
    """
    Handles encoding and decoding of messages between bytes and Message objects.
    Supports both structured JSON and legacy text-based protocols.
    """

    @staticmethod
    def encode_json(message: Message) -> bytes:
        """Encode a Message object to JSON bytes"""
        json_str = json.dumps(message.to_dict())
        return (json_str + '\n').encode('utf-8')

    @staticmethod
    def decode_json(data: bytes) -> Message:
        """Decode JSON bytes to a Message object"""
        json_str = data.decode('utf-8').strip()
        message_dict = json.loads(json_str)
        return Message.from_dict(message_dict)

    @staticmethod
    def encode_text(message: Message) -> bytes:
        """
        Encode a Message to legacy text format with ANSI support.
        Used for backwards compatibility with telnet clients.
        """
        msg_type = message.type
        data = message.data

        if msg_type == MessageType.ROOM_DESCRIPTION:
            text = data.get('text', '')
        elif msg_type == MessageType.PROMPT:
            text = data.get('text', '> ')
        elif msg_type == MessageType.ROOM_MESSAGE:
            text = data.get('text', '')
        elif msg_type == MessageType.ERROR:
            text = f"ERROR: {data.get('text', 'Unknown error')}"
        elif msg_type == MessageType.SYSTEM:
            text = data.get('text', '')
        else:
            text = data.get('text', str(data))

        if not text.endswith('\r\n'):
            text += '\r\n'

        return text.encode('utf-8')

    @staticmethod
    def decode_text(data: bytes) -> Message:
        """
        Decode text input to a Message object.
        Checks for JSON first, then treats as command.
        """
        text = data.decode('utf-8').strip()
        if not text:
            return Message(type=MessageType.INPUT, data={'text': ''})

        if MessageCodec.is_json(data):
            try:
                return MessageCodec.decode_json(data)
            except Exception:
                pass

        if text.startswith('logon '):
            parts = text.split(maxsplit=1)
            if len(parts) == 2:
                try:
                    payload = json.loads(parts[1])
                    return Message(
                        type=MessageType.CHAR_LOGON,
                        data=payload
                    )
                except json.JSONDecodeError:
                    pass

        return Message(type=MessageType.COMMAND, data={'text': text})

    @staticmethod
    def is_json(data: bytes) -> bool:
        """Check if data appears to be JSON"""
        try:
            text = data.decode('utf-8').strip()
            return text.startswith('{') and text.endswith('}')
        except (UnicodeDecodeError, AttributeError):
            return False
