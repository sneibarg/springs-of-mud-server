from dataclasses import dataclass


@dataclass
class Reset:
    id: str
    area_id: str
    command: str
    arg1: str
    arg2: str
    arg3: str
    arg4: str
    comment: str

    def __init__(self):
        pass
