from enum import IntEnum


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
