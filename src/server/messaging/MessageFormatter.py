from typing import Optional
from server.protocol import Message, MessageType


class MessageFormatter:
    """
    Formats game messages with proper structure and styling.
    Extracted from utilities for better organization.
    """

    @staticmethod
    def format_room_description(room_name: str, description: str, exits: list) -> Message:
        """Format a room description message"""
        text = f"[{room_name}]\r\n{description}\r\n"
        if exits:
            exits_text = "Exits: " + ", ".join(exits) + "\r\n"
            text += exits_text

        return Message(
            type=MessageType.ROOM_DESCRIPTION,
            data={
                'text': text,
                'room_name': room_name,
                'description': description,
                'exits': exits
            }
        )

    @staticmethod
    def format_room_message(text: str, pattern: Optional[str] = None, sender_name: Optional[str] = None,
                           cloaked: bool = False) -> Message:
        """
        Format a message to be sent to a room.
        Supports patterns like '%p says %m' where %p is player name and %m is message.
        """
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
    def format_say(speaker_name: str, text: str, cloaked: bool = False) -> Message:
        """Format a 'say' message"""
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
        """Format an emote message"""
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
        """Format a tell (private message)"""
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
    def format_character_list(characters: list) -> Message:
        """Format a list of characters"""
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
