import json

from server.protocol.Message import Message
from server.protocol.MessageTypes import MessageType
from server.LoggerFactory import LoggerFactory


logger = LoggerFactory.get_logger("MessageCodec")


class MessageCodec:
    @staticmethod
    def encode_json(message: Message) -> bytes:
        json_str = json.dumps(message.to_dict())
        return (json_str + '\n').encode('utf-8')

    @staticmethod
    def decode_json(data: bytes) -> Message:
        json_str = data.decode('utf-8').strip()
        message_dict = json.loads(json_str)
        return Message.from_dict(message_dict)

    @staticmethod
    def encode_text(message: Message) -> bytes:
        msg_type = message.type
        data = message.data
        text = str()

        if msg_type == MessageType.ERROR:
            text = f"ERROR: {data.get('text', 'Unknown error')}"
        if msg_type == MessageType.GAME:
            text = data.get('text', '')

        if not text.endswith('\r\n'):
            text += '\r\n'

        return text.encode('utf-8')

    @staticmethod
    def decode_text(data: bytes) -> Message:
        text = data.decode('utf-8').strip()
        if not text:
            return Message(type=MessageType.GAME, data={'text': ''})

        if MessageCodec.is_json(data):
            try:
                return MessageCodec.decode_json(data)
            except Exception as e:
                logger.error(f"Failed to decode JSON: {e}")
                return Message(type=MessageType.ERROR, data={'text': 'Failed to decode JSON'})

        if text.startswith('logon '):
            parts = text.split(maxsplit=1)
            if len(parts) == 2:
                try:
                    payload = json.loads(parts[1])
                    return Message(type=MessageType.AUTH, data=payload)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON payload: {e}")

        return Message(type=MessageType.GAME, data={'text': text})

    @staticmethod
    def is_json(data: bytes) -> bool:
        try:
            text = data.decode('utf-8').strip()
            return text.startswith('{') and text.endswith('}')
        except (UnicodeDecodeError, AttributeError):
            return False
