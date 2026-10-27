import json

from enum import Enum
from dataclasses import dataclass


class AffectWhere(Enum):
    TO_AFFECTS = 0  # applies effect/spell to the character
    TO_OBJECT = 1  # modifies the item's base stats
    TO_IMMUNE = 2  # applies immunity to the character
    TO_RESIST = 3  # applies resistance to the character
    TO_VULN = 4  # applies vulnerability to the character
    TO_WEAPON = 5  # modifies the weapon's base stats


@dataclass
class Effect:
    valid: bool = False
    where: str | int = 0
    type: str | int = ""
    level: int = 0
    duration: int = 0
    location: str | int = 0
    modifier: int = 0
    bitvector: str | int = 0
    apply_to: str = ""
    source: str = ""

    @staticmethod
    def item_source(item_id: str) -> str:
        return f"item:{item_id}"

    def belongs_to_item(self, item_id: str) -> bool:
        source = Effect.item_source(item_id)
        # Older saves appended Python's process-specific id(item).
        actual = str(self.source or '')
        return actual == source or actual.startswith(source + ':')

    def matches_location(self, apply_types, *names: str) -> bool:
        from util.GenericUtil import GenericUtil
        raw = str(self.location).strip().upper()
        if raw in names:
            return True
        value = GenericUtil.to_int(self.location, None)
        return value is not None and any(
            getattr(getattr(apply_types, name, None), 'value', None) == value for name in names)

    def has_bit(self, bit_name: str, bit: int) -> bool:
        from api.GameApi import GameApi

        raw = getattr(self, "bitvector", 0)
        if str(raw or "").strip().upper() == str(bit_name or "").strip().upper():
            return True
        return GameApi.flags_to_int(raw) == bit

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        from util.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        return cls(**payload)

    def evaluate_expressions(self, caster_level: int, evaluate) -> None:
        """Resolve this effect's numeric fields using the supplied safe evaluator."""
        self.level = evaluate(self.level, default=int(caster_level), level=caster_level)
        self.duration = evaluate(self.duration, default=0, level=caster_level)
        self.modifier = evaluate(self.modifier, default=0, level=caster_level)

    def try_dispel(self, dis_level: int, saves_dispel) -> bool:
        """Report dispel success, weakening this record when it resists."""
        from util.GenericUtil import GenericUtil

        level = GenericUtil.to_int(self.level, 0)
        if saves_dispel(dis_level, level, GenericUtil.to_int(self.duration, 0)):
            self.level = level - 1
            return False
        return True
