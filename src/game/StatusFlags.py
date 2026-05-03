from __future__ import annotations

from dataclasses import dataclass


class BitField(int):
    def __new__(cls, value=0):
        return super().__new__(cls, int(value or 0))

    def set_bit(self, bit) -> "BitField":
        raw_bit = getattr(bit, "value", bit)
        return BitField(int(self) | int(raw_bit))

    def unset_bit(self, bit) -> "BitField":
        raw_bit = getattr(bit, "value", bit)
        return BitField(int(self) & ~int(raw_bit))

    def is_set(self, bit) -> bool:
        raw_bit = getattr(bit, "value", bit)
        return (int(self) & int(raw_bit)) != 0


@dataclass
class StatusFlags:
    BITFIELD_FIELDS = (
        "act",
        "comm",
        "affected_by",
        "off",
        "imm",
        "res",
        "vuln",
        "form",
        "parts",
    )

    act: BitField
    comm: BitField
    affected_by: BitField
    off: BitField
    imm: BitField
    res: BitField
    vuln: BitField
    form: BitField
    parts: BitField
    invis_level: int
    incog_level: int
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int

    def __post_init__(self):
        for field_name in self.BITFIELD_FIELDS:
            object.__setattr__(self, field_name, BitField(getattr(self, field_name, 0)))

    def __setattr__(self, name, value):
        if name in self.BITFIELD_FIELDS:
            value = BitField(value)
        super().__setattr__(name, value)

    def assign_bitfield(self, name: str, value) -> None:
        if name not in self.BITFIELD_FIELDS:
            raise AttributeError(f"{name} is not a bitfield member")
        setattr(self, name, BitField(value))

    def set_flag(self, name: str, bit) -> None:
        if name not in self.BITFIELD_FIELDS:
            raise AttributeError(f"{name} is not a bitfield member")
        setattr(self, name, getattr(self, name).set_bit(bit))

    def unset_flag(self, name: str, bit) -> None:
        if name not in self.BITFIELD_FIELDS:
            raise AttributeError(f"{name} is not a bitfield member")
        setattr(self, name, getattr(self, name).unset_bit(bit))

    @classmethod
    def default(cls) -> "StatusFlags":
        zero = BitField(0)
        return cls(
            act=zero,
            comm=zero,
            affected_by=zero,
            off=zero,
            imm=zero,
            res=zero,
            vuln=zero,
            form=zero,
            parts=zero,
            invis_level=0,
            incog_level=0,
            played=0,
            logon=0,
            pulse_wait=0,
            pulse_daze=0,
        )

    @classmethod
    def from_json(cls, data) -> "StatusFlags":
        from util.GenericUtil import GenericUtil

        if isinstance(data, StatusFlags):
            return data

        payload = GenericUtil.camel_to_snake_case(data or {})
        base = cls.default().__dict__.copy()
        base.update(payload)
        return cls(**base)
