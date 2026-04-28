from enum import IntEnum

from util.GenericUtil import GenericUtil


class GameMacros:
    @staticmethod
    def is_set(flag: int, bit) -> bool:
        if hasattr(bit, "value"):
            return (flag & bit.value) != 0
        return (flag & bit) != 0

    @staticmethod
    def set_bit(flag: int, bit) -> int:
        if hasattr(bit, "value"):
            return flag | bit.value
        return flag | bit

    @staticmethod
    def unset_bit(flag: int, bit) -> int:
        if hasattr(bit, "value"):
            return flag & ~bit.value
        return flag & ~bit

    @staticmethod
    def parse_flag_string(flag_str: str | None, FlagLetters: type[IntEnum] | None) -> int:
        if not flag_str or str(flag_str).strip() in ("", "0", "None", "null"):
            return 0

        total = 0
        for char in flag_str.strip():
            if char.isalnum():
                upper = char.upper()
                try:
                    member = FlagLetters[upper]
                    total |= member
                except KeyError:
                    pass

        return total

    @staticmethod
    def convert_flags(flag_value: str) -> int:
        return GameMacros.letters_to_flags(str(flag_value or ""))

    @staticmethod
    def letters_to_flags(value: str) -> int:
        total = 0
        for c in str(value or "").upper():
            if "A" <= c <= "Z":
                total |= (1 << (ord(c) - ord("A")))
        return total

    @staticmethod
    def flags_to_letters(value: int) -> str:
        if GenericUtil.to_int(value, 0) <= 0:
            return ""
        out = []
        raw = GenericUtil.to_int(value, 0)
        for bit in range(26):
            if raw & (1 << bit):
                out.append(chr(ord("A") + bit))
        return "".join(out)

    @staticmethod
    def flags_to_int(raw) -> int:
        value = GenericUtil.to_int(raw, None)
        if value is not None:
            return value
        return GameMacros.letters_to_flags(str(raw or "0"))
