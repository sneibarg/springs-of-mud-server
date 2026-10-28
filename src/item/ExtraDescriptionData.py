import ast
import json

from dataclasses import dataclass
from typing import Mapping


@dataclass
class ExtraDescriptionData:
    valid: bool
    keyword: str
    description: str
    next: 'ExtraDescriptionData | None' = None

    @classmethod
    def from_json(cls, data: str):
        if isinstance(data, cls):
            return data
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                try:
                    parsed = ast.literal_eval(data)
                except (SyntaxError, ValueError) as exc:
                    raise ValueError(f"Unable to parse exits value: {data!r}") from exc
        elif isinstance(data, Mapping):
            parsed = dict(data)
        else:
            raise TypeError(f"Exit.from_json expected mapping or JSON string; got {type(data).__name__}")

        if not isinstance(parsed, Mapping):
            raise TypeError(f"Parsed exit must be a mapping, got {type(parsed).__name__}")
        if parsed.get('valid') is None:
            parsed['valid'] = False
            parsed['keyword'] = None
            parsed['description'] = None
        if parsed.get('next') is not None:
            parsed['next'] = cls.from_json(parsed['next'])
        return cls(**parsed)

    @classmethod
    def entries(cls, data):
        """Walk the canonical description chain, accepting legacy wire objects."""
        seen = set()
        while data is not None and id(data) not in seen:
            seen.add(id(data))
            entry = cls.from_json(data)
            yield entry
            data = entry.next
