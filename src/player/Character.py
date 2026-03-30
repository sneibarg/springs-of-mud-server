import threading

from dataclasses import dataclass, field
from typing import Dict, List
from game.PromptFormat import PromptFormat
from object.Item import Item
from player.CharacterClass import CharacterClass
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
    piercing: int
    bashing: int
    slashing: int
    magic: int
    played: int
    logon: int
    pulse_wait: int
    pulse_daze: int
    trust: int
    attributes: List[int]
    inventory: List[str]
    character_class: CharacterClass
    prompt_format: PromptFormat
    loot: Dict[str, object] = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock)
    carriage_return: bool = True

    def __post_init__(self):
        self.logger = LoggerFactory.get_logger(__name__)
        self.load_inventory()

    def load_inventory(self):
        with self.lock:
            self.logger.info("Loading inventory...")
            for item in self.inventory:
                lootable = Item.from_json(item)
                self.loot[lootable.id] = lootable
            self.logger.info("Inventory loaded.")

    def get_items(self):
        return self.loot.values()

    def get_fuzzy_item(self, fuzzy_item, usage):
        fuzzy_item = fuzzy_item.strip().replace("\r\n", "")
        self.logger.debug("get_fuzzy_item: fuzzy_item=" + str(fuzzy_item))
        for item_id in self.loot:
            lootable = self.loot[item_id]
            if not isinstance(lootable, Item):
                self.logger.debug("get_fuzzy_item: lootable=" + str(lootable))
                continue
            if lootable.name.startswith(fuzzy_item) or fuzzy_item == lootable.name:
                return lootable
        usage(self)
        return None

    @classmethod
    def from_json(cls, data):
        payload = dict(data)
        prompt_format = payload.get('prompt_format')
        character_class = payload.get('character_class')

        if not isinstance(prompt_format, PromptFormat):
            prompt_format = PromptFormat.from_template(prompt_format)

        payload['prompt_format'] = prompt_format
        payload['character_class'] = CharacterClass.from_json(character_class)
        return cls(**payload)

