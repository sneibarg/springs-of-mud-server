from dataclasses import dataclass


@dataclass
class Special:
    id: str
    area_id: str
    mob_vnum: str
    special_function: str
    comment: str

    def __init__(self):
        pass
