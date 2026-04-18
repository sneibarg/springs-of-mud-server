import threading

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, TYPE_CHECKING

from interp.PromptFormat import PromptFormat
from object.Item import Item
from player.CharacterClass import CharacterClass
from player.PCArmorClass import PCArmorClass
from player.TemporalMechanics import TemporalMechanics
from player.CharacterAttributes import CharacterAttributes
from player.CharacterFlags import CharacterFlags
from server.LoggerFactory import LoggerFactory

if TYPE_CHECKING:
    from game.Equipped import Equipped


@dataclass
class Character:
    id: str
    account_id: str
    title: str
    description: str
    cloaked: bool
    guild: str
    race: str
    name: str
    area_id: str
    room_id: str
    guild: str
    role: str
    sex: str
    cloaked: bool
    level: int
    hit: int
    max_hit: int
    mana: int
    max_mana: int
    movement: int
    max_movement: int
    experience: int
    accumulated_experience: int
    gold: int
    silver: int
    trust: int
    inventory: List[str]
    character_flags: CharacterFlags
    character_attributes: CharacterAttributes
    temporal_mechanics: TemporalMechanics
    armor_class: PCArmorClass
    character_class: CharacterClass
    prompt_format: PromptFormat
    invis_level: Optional[int] = 0
    incog_level: Optional[int] = 0
    fighting: Optional[Any] = None
    equipped: Optional[Equipped] = None
    context: Dict[str, object] = field(default_factory=dict)
    loot: List[Item] = field(default_factory=list)
    effects: list = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)
    carriage_return: bool = True

    def __post_init__(self):
        self.logger = LoggerFactory.get_logger(__name__)
        self.load_inventory()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.id == other.id
        return False

    def load_inventory(self):
        with self.lock:
            for item in self.inventory:
                self.loot.append(Item.from_json(item))

    def get_items(self) -> List[Item]:
        return self.loot

    @classmethod
    def from_json(cls, data):
        from game.GenericUtil import GenericUtil
        payload = GenericUtil.camel_to_snake_case(data)
        prompt_format = payload.get('prompt_format')
        character_class = payload.get('character_class')
        armor_class = payload.get('armor_class')
        temporal_mechanics = payload.get('temporal_mechanics')
        character_attributes = payload.get('character_attributes')
        character_flags = payload.get('character_flags')

        payload['character_flags'] = CharacterFlags.from_json(character_flags)
        payload['character_attributes'] = CharacterAttributes.from_json(character_attributes)
        payload['temporal_mechanics'] = TemporalMechanics.from_json(temporal_mechanics)
        payload['armor_class'] = PCArmorClass.from_json(armor_class)
        payload['prompt_format'] = PromptFormat.from_template(prompt_format)
        payload['character_class'] = CharacterClass.from_json(character_class)
        return cls(**payload)



