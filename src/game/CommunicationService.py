from typing import Optional
from server.protocol import Message, MessageType


class CommunicationService:
    @staticmethod
    def format_say(speaker_name: str, text: str, cloaked: bool = False) -> Message:
        display_name = "Someone" if cloaked else speaker_name
        formatted = f"{display_name} says '{text}'\r\n"

        return Message(
            type=MessageType.SAY,
            data={
                'text': formatted,
                'speaker': speaker_name,
                'message': text,
                'cloaked': cloaked
            }
        )

    @staticmethod
    def format_emote(actor_name: str, action: str, cloaked: bool = False) -> Message:
        display_name = "Someone" if cloaked else actor_name
        formatted = f"{display_name} {action}\r\n"

        return Message(
            type=MessageType.EMOTE,
            data={
                'text': formatted,
                'actor': actor_name,
                'action': action,
                'cloaked': cloaked
            }
        )

    @staticmethod
    def format_tell(from_name: str, to_name: str, text: str) -> Message:
        formatted = f"{from_name} tells you '{text}'\r\n"

        return Message(
            type=MessageType.TELL,
            data={
                'text': formatted,
                'from': from_name,
                'to': to_name,
                'message': text
            }
        )

    @staticmethod
    def format_room_message(text: str, pattern: Optional[str] = None, sender_name: Optional[str] = None,
                           cloaked: bool = False) -> Message:
        if pattern:
            display_name = "Someone" if cloaked else (sender_name or "Someone")
            formatted = pattern.replace('%p', display_name).replace('%m', text)
            text = formatted

        if not text.endswith('\r\n'):
            text += '\r\n'

        return Message(
            type=MessageType.ROOM_MESSAGE,
            data={
                'text': text,
                'sender': sender_name,
                'cloaked': cloaked
            }
        )

    @staticmethod
    def format_character_list(characters: list) -> Message:
        lines = ["Players found: {}\r\n".format(len(characters))]
        for char in characters:
            line = "[{}\t{}\t{}] {} {}\r\n".format(
                char.get('level', '?'),
                char.get('race', '?'),
                char.get('character_class', '?'),
                char.get('name', 'Unknown'),
                char.get('title', '')
            )
            lines.append(line)

        return Message(
            type=MessageType.ROOM_PLAYERS,
            data={
                'text': ''.join(lines),
                'characters': characters
            }
        )
