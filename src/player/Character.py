import threading

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, TYPE_CHECKING

from interp.PromptFormat import PromptFormat
from object.Item import Item
from player.CharacterClass import CharacterClass
from player.CharacterArmorClass import PCArmorClass
from player.CharacterRace import CharacterRace
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
    gold: int
    silver: int
    trust: int
    inventory: List[Any]
    effects: List[Any]
    skills: List[Any]
    spells: List[Any]
    character_flags: CharacterFlags
    character_attributes: CharacterAttributes
    temporal_mechanics: TemporalMechanics
    armor_class: PCArmorClass
    character_class: CharacterClass
    prompt_format: PromptFormat
    character_race: CharacterRace | None = None
    invis_level: Optional[int] = 0
    incog_level: Optional[int] = 0
    fighting: Optional[Any] = None
    equipped: Optional[Equipped] = None
    context: Dict[str, object] = field(default_factory=dict)
    loot: List[Item] = field(default_factory=list)
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

    @property
    def race(self) -> str:
        if self.character_race is None:
            return ""
        return str(getattr(self.character_race, "who_name", "") or "")

    @race.setter
    def race(self, value: str) -> None:
        self.character_race = CharacterRace.from_name(value)

    @property
    def experience(self) -> int:
        attrs = getattr(self, "character_attributes", None)
        return 0 if attrs is None else getattr(attrs, "experience", 0)

    @experience.setter
    def experience(self, value: int) -> None:
        attrs = getattr(self, "character_attributes", None)
        if attrs is not None:
            attrs.experience = value

    @property
    def accumulated_experience(self) -> int:
        attrs = getattr(self, "character_attributes", None)
        return 0 if attrs is None else getattr(attrs, "accumulated_experience", 0)

    @accumulated_experience.setter
    def accumulated_experience(self, value: int) -> None:
        attrs = getattr(self, "character_attributes", None)
        if attrs is not None:
            attrs.accumulated_experience = value

    @property
    def experience_per_level(self) -> int:
        attrs = getattr(self, "character_attributes", None)
        return 0 if attrs is None else getattr(attrs, "experience_per_level", 0)

    @experience_per_level.setter
    def experience_per_level(self, value: int) -> None:
        attrs = getattr(self, "character_attributes", None)
        if attrs is not None:
            attrs.experience_per_level = value

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        from game.Equipped import Equipped
        payload = GenericUtil.camel_to_snake_case(data)
        prompt_format = payload.get('prompt_format')
        character_class = payload.get('character_class')
        armor_class = payload.get('armor_class')
        temporal_mechanics = payload.get('temporal_mechanics')
        character_attributes = payload.get('character_attributes')
        character_flags = payload.get('character_flags')
        character_race = payload.get('character_race', payload.get('race'))
        equipped_data = payload.get('equipped')

        payload['character_flags'] = CharacterFlags.from_json(character_flags)
        payload['character_attributes'] = CharacterAttributes.from_json(character_attributes)
        payload['temporal_mechanics'] = TemporalMechanics.from_json(temporal_mechanics)
        payload['armor_class'] = PCArmorClass.from_json(armor_class)
        payload['prompt_format'] = PromptFormat.from_template(prompt_format)
        payload['character_class'] = CharacterClass.from_json(character_class)
        payload['character_race'] = CharacterRace.from_json(character_race, character_class=payload['character_class'])
        payload.pop('race', None)

        if isinstance(equipped_data, dict):
            normalized_equipped = GenericUtil.camel_to_snake_case(equipped_data)
            equipped = Equipped()
            for slot, item_data in normalized_equipped.items():
                if not hasattr(equipped, slot) or item_data is None:
                    continue
                if isinstance(item_data, Item):
                    setattr(equipped, slot, item_data)
                    continue
                if isinstance(item_data, (dict, str)):
                    setattr(equipped, slot, Item.from_json(item_data))
            payload['equipped'] = equipped

        return cls(**payload)



