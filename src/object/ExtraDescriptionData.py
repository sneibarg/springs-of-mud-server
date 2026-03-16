from dataclasses import dataclass


@dataclass
class ExtraDescriptionData:
    valid: bool
    keyword: str
    description: str
