from __future__ import annotations

from dataclasses import dataclass, field


class BitField:
    __slots__ = ()

    @staticmethod
    def coerce(value) -> int:
        return int(value or 0)

    @staticmethod
    def set_bit(value, bit) -> int:
        raw_bit = getattr(bit, "value", bit)
        return BitField.coerce(value) | int(raw_bit)

    @staticmethod
    def unset_bit(value, bit) -> int:
        raw_bit = getattr(bit, "value", bit)
        return BitField.coerce(value) & ~int(raw_bit)


@dataclass(slots=True)
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

    act: int
    comm: int
    affected_by: int
    off: int
    imm: int
    res: int
    vuln: int
    form: int
    parts: int
    hunger: int
    thirst: int
    drunk: int
    invis_level: int
    incog_level: int
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int
    _bitfield_write_enabled: bool = field(default=False, init=False, repr=False, compare=False)
    _initialized: bool = field(default=False, init=False, repr=False, compare=False)

    def __post_init__(self):
        for field_name in self.BITFIELD_FIELDS:
            object.__setattr__(self, field_name, BitField.coerce(getattr(self, field_name, 0)))
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name, value):
        if name in self.BITFIELD_FIELDS:
            value = BitField.coerce(value)
            if getattr(self, "_initialized", False) and not getattr(self, "_bitfield_write_enabled", False):
                raise AttributeError(f"{name} must be modified through StatusFlags bitfield helpers")
        object.__setattr__(self, name, value)

    def assign_bitfield(self, name: str, value) -> None:
        if name not in self.BITFIELD_FIELDS:
            raise AttributeError(f"{name} is not a bitfield member")
        self._write_bitfield(name, BitField.coerce(value))

    def set_flag(self, name: str, bit) -> None:
        if name not in self.BITFIELD_FIELDS:
            raise AttributeError(f"{name} is not a bitfield member")
        self._write_bitfield(name, BitField.set_bit(getattr(self, name, 0), bit))

    def unset_flag(self, name: str, bit) -> None:
        if name not in self.BITFIELD_FIELDS:
            raise AttributeError(f"{name} is not a bitfield member")
        self._write_bitfield(name, BitField.unset_bit(getattr(self, name, 0), bit))

    def _write_bitfield(self, name: str, value: int) -> None:
        object.__setattr__(self, "_bitfield_write_enabled", True)
        try:
            setattr(self, name, value)
        finally:
            object.__setattr__(self, "_bitfield_write_enabled", False)

    @classmethod
    def default(cls) -> "StatusFlags":
        return cls(
            act=0,
            comm=0,
            affected_by=0,
            off=0,
            imm=0,
            res=0,
            vuln=0,
            form=0,
            parts=0,
            hunger=48,
            thirst=48,
            drunk=0,
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
        defaults = cls.default()
        constructor_fields = {
            field_name: field_def
            for field_name, field_def in cls.__dataclass_fields__.items()
            if field_def.init and not field_name.startswith("_")
        }
        base = {
            field_name: getattr(defaults, field_name)
            for field_name in constructor_fields
        }
        base.update({
            field_name: value
            for field_name, value in payload.items()
            if field_name in constructor_fields
        })
        return cls(**base)

    @classmethod
    def from_template(cls, template: "StatusFlags") -> "StatusFlags":
        return StatusFlags(
            act=template.act,
            comm=template.comm,
            affected_by=template.affected_by,
            off=template.off,
            imm=template.imm,
            res=template.res,
            vuln=template.vuln,
            form=template.form,
            parts=template.parts,
            hunger=48,
            thirst=48,
            drunk=0,
            invis_level=template.invis_level,
            incog_level=template.incog_level,
            played=template.played,
            logon=template.logon,
            pulse_wait=template.pulse_wait,
            pulse_daze=template.pulse_daze
        )
