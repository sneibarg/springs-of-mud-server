from typing import Optional, Callable
from .Message import Message
from .MessageTypes import MessageType
from .MessageCodec import MessageCodec


class TelnetProtocol:
    """
    Handles telnet-specific protocol concerns:
    - IAC command stripping
    - ANSI color support
    - Text encoding/decoding
    """

    IAC = 255  # Interpret As Command
    DO = 253
    DONT = 254
    WILL = 251
    WONT = 252
    SB = 250   # Subnegotiation Begin
    SE = 240   # Subnegotiation End

    def __init__(self, ansi_enabled: bool = False):
        self.ansi_enabled = ansi_enabled
        self.codec = MessageCodec()

    @staticmethod
    def strip_telnet_commands(data: bytes) -> bytes:
        """
        Strip telnet IAC sequences from data.
        Returns cleaned data suitable for text processing.
        """
        i = 0
        result = bytearray()
        length = len(data)

        while i < length:
            byte = data[i]
            if byte == TelnetProtocol.IAC:
                i += 1
                if i < length:
                    cmd = data[i]
                    if cmd in (TelnetProtocol.DO, TelnetProtocol.DONT,
                              TelnetProtocol.WILL, TelnetProtocol.WONT):
                        i += 1
                    elif cmd == TelnetProtocol.SB:
                        i += 1
                        while i < length - 1 and not (data[i] == TelnetProtocol.IAC
                                                      and data[i+1] == TelnetProtocol.SE):
                            i += 1
                        if i < length - 1:
                            i += 1  # Skip SE
            else:
                result.append(byte)
            i += 1

        return bytes(result)

    def encode_message(self, message: Message) -> bytes:
        """Encode a message for telnet transmission"""
        return self.codec.encode_text(message)

    def decode_input(self, data: bytes) -> Message:
        """Decode telnet input to a Message"""
        cleaned = self.strip_telnet_commands(data)
        return self.codec.decode_text(cleaned)

    def format_ansi(self, text: str, color_code: Optional[str] = None) -> str:
        """
        Format text with ANSI colors if enabled.

        Args:
            text: The text to format
            color_code: ANSI color code (e.g., '31' for red, '32' for green)
        """
        if not self.ansi_enabled or not color_code:
            return text

        return f"\033[{color_code}m{text}\033[0m"

    def create_prompt(self, health: int, mana: int, movement: int) -> Message:
        """Create a formatted prompt message"""
        prompt_text = f"<{health}hp {mana}m {movement}mv>\r\n"
        return Message(
            type=MessageType.PROMPT,
            data={'text': prompt_text, 'health': health, 'mana': mana, 'movement': movement}
        )
