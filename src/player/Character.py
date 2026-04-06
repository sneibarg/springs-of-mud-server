import asyncio
import threading

from dataclasses import dataclass, field
from typing import Dict, List
from interp.PromptFormat import PromptFormat
from object.Item import Item
from player.CharacterClass import CharacterClass
from player.PCArmorClass import PCArmorClass
from server.LoggerFactory import LoggerFactory


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
    act: str
    comm: str
    affected_by: str
    cloaked: bool
    level: int
    health: int
    mana: int
    movement: int
    experience: int
    accumulated_experience: int
    trains: int
    practices: int
    gold: int
    silver: int
    wimpy: int
    position: int
    max_weight: int
    max_items: int
    alignment: int
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int
    trust: int
    attributes: List[int]
    inventory: List[str]
    armor_class: PCArmorClass
    character_class: CharacterClass
    prompt_format: PromptFormat
    loot: Dict[str, object] = field(default_factory=dict)
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
            index = 0
            for item in self.inventory:
                self.inventory[index] = Item.from_json(item)
                index = index + 1

    def get_items(self) -> List[Item]:
        return self.inventory

    def get_fuzzy_item(self, fuzzy_item, usage, mb):
        fuzzy_item = fuzzy_item.strip().replace("\r\n", "")
        self.logger.debug("get_fuzzy_item: fuzzy_item=" + str(fuzzy_item))
        for item in self.inventory:
            if not isinstance(item, Item):
                self.logger.debug("get_fuzzy_item: not an Item: " + str(item))
                continue
            if item.name.startswith(fuzzy_item) or fuzzy_item == item.name:
                self.logger.debug("get_fuzzy_item: FOUND: " + str(item))
                return item
        asyncio.ensure_future(usage(self, mb))
        return None

    @classmethod
    def from_json(cls, data):
        from server.ServerUtil import ServerUtil
        payload = ServerUtil.camel_to_snake_case(data)
        prompt_format = payload.get('prompt_format')
        character_class = payload.get('character_class')
        armor_class = payload.get('armor_class')

        payload['armor_class'] = PCArmorClass.from_json(armor_class)
        payload['prompt_format'] = PromptFormat.from_template(prompt_format)
        payload['character_class'] = CharacterClass.from_json(character_class)
        return cls(**payload)



