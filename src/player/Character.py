from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Any, TYPE_CHECKING

from game.AnimateEntity import AnimateEntity
from game.Equipped import Equipped
from interp.Context import Context
from player.ArmorClass import ArmorClass
from player.CharacterClass import CharacterClass
from player.CharacterFlags import CharacterFlags
from player.CharacterRace import CharacterRace
from player.CharacterAttributes import CharacterAttributes
from interp.PromptFormat import PromptFormat
from game.StatusFlags import StatusFlags
from util.GenericUtil import GenericUtil

if TYPE_CHECKING:
    from item.Item import Item


@dataclass
class Character(AnimateEntity):
    account_id: str
    title: str
    description: str
    cloaked: bool
    guild: str
    role: str
    hit: int
    max_hit: int
    mana: int
    max_mana: int
    movement: int
    max_movement: int
    trust: int
    character_class: CharacterClass
    prompt_format: PromptFormat
    character_flags: CharacterFlags | None = None
    character_race: CharacterRace | None = None
    skills: List[dict] = field(default_factory=list)
    spells: List[dict] = field(default_factory=list)
    loot: List[Item] = field(default_factory=list)
    context: Optional[Context] = None
    carriage_return: bool = True

    def __post_init__(self):
        super().__post_init__()
        self.load_inventory()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.id == other.id
        return False

    @classmethod
    def from_json(cls, data):
        from util.GenericUtil import GenericUtil
        from item.Effect import Effect
        from item.Item import Item
        payload = GenericUtil.camel_to_snake_case(data)
        prompt_format = payload.get('prompt_format')
        character_flags = payload.get('character_flags')
        character_class = payload.get('character_class')
        armor_class = payload.get('armor_class')
        character_attributes = payload.get('character_attributes')
        status_flags = payload.get('status_flags')
        character_race = payload.get('character_race', payload.get('race'))
        equipped_data = payload.get('equipped')

        payload.setdefault('room_id', "")
        payload['status_flags'] = StatusFlags.from_json(status_flags)
        payload['character_attributes'] = CharacterAttributes.from_json(character_attributes)
        payload['armor_class'] = ArmorClass.from_json(armor_class)
        payload['prompt_format'] = PromptFormat.from_template(prompt_format)
        payload['character_flags'] = CharacterFlags.from_json(character_flags) if character_flags else None
        payload['character_class'] = CharacterClass.from_json(character_class)
        payload['character_race'] = CharacterRace.from_json(character_race, character_class=payload['character_class'])
        payload.pop('race', None)
        payload['effects'] = [
            effect if isinstance(effect, Effect) else Effect.from_json(effect)
            for effect in list(payload.get('effects', []) or [])
        ]

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

    def load_inventory(self):
        from item.Item import Item
        with self.lock:
            self.loot = []
            for item in list(self.inventory or []):
                self.loot.append(item if isinstance(item, Item) else Item.from_json(item))

    def skill_level(self, skill_name: str) -> int:
        return Character.learned_entry_level(Character.get_learned(self, skill_name, collection_name="skills")) or 1

    def spell_level(self, spell_name: str) -> int:
        return Character.learned_entry_level(Character.get_learned(self, spell_name, collection_name="spells")) or 1

    def get_items(self) -> List[Item]:
        return self.loot

    def carry_count(self) -> int:
        return len(list(self.loot or []))

    def carry_weight(self) -> int:
        item_weight = sum(GenericUtil.to_int(getattr(item, "weight", 0), 0) for item in list(self.loot or []))
        coin_weight = int((GenericUtil.to_int(self.silver, 0) / 10) + (GenericUtil.to_int(self.gold, 0) * 2 / 5))
        return item_weight + coin_weight

    def max_items(self) -> int:
        return self.character_attributes.max_items

    def max_weight(self) -> int:
        return self.character_attributes.max_weight

    def size_value(self) -> int:
        direct_size = GenericUtil.to_int(getattr(self, "size", None), None)
        if direct_size is not None:
            return direct_size

        from api.CharacterApi import CharacterApi

        race_name = str(getattr(self, "race", "") or "").strip().lower()
        try:
            race_data = CharacterApi.pc_races_map().get(race_name, {})
        except RuntimeError:
            race_data = {}
        raw_size = race_data.get("size")
        try:
            size_enum = CharacterApi.get_enum("size")
        except RuntimeError:
            size_enum = None
        if isinstance(raw_size, str) and size_enum is not None and hasattr(size_enum, raw_size):
            return int(getattr(size_enum, raw_size).value)
        size_value = GenericUtil.to_int(raw_size, None)
        if size_value is not None:
            return size_value
        return self.large_size_value() - 1

    @staticmethod
    def large_size_value() -> int:
        from api.CharacterApi import CharacterApi

        try:
            size_enum = CharacterApi.get_enum("size")
        except RuntimeError:
            size_enum = None
        if size_enum is not None and hasattr(size_enum, "SIZE_LARGE"):
            return int(size_enum.SIZE_LARGE.value)
        return 3

    def has_item_vnum(self, vnum: str | int) -> bool:
        wanted = str(vnum or "")
        if not wanted:
            return False
        return any(str(getattr(item, "vnum", "")) == wanted for item in list(self.loot or []))

    def has_key(self, key: int) -> bool:
        return GenericUtil.to_int(key, -1) >= 0 and self.has_item_vnum(key)

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

    def get_age(self) -> int:
        return int(17 + (self.status_flags.played + datetime.now().timestamp() - self.status_flags.logon) / 72000)

    def has_boat(self) -> bool:
        for item in list(self.loot or []):
            item_type = str(getattr(item, "item_type", "") or "").lower()
            if "boat" in item_type:
                return True
        return False

    def learned(self) -> List[Any]:
        return [self.skills, self.spells]

    @staticmethod
    def learned_entry_name(entry) -> str:
        if entry is None:
            return ""
        if isinstance(entry, dict):
            return str(entry.get("name", "") or "").strip()
        return str(getattr(entry, "name", "") or "").strip()

    @staticmethod
    def learned_entry_level(entry) -> int:
        if entry is None:
            return 0
        if isinstance(entry, dict):
            return max(0, min(100, GenericUtil.to_int(entry.get("level", 0), 0)))
        return max(0, min(100, GenericUtil.to_int(getattr(entry, "level", 0), 0)))

    @staticmethod
    def _set_learned_entry_level(entry, learned_level: int) -> None:
        if entry is None:
            return
        normalized = max(0, min(100, GenericUtil.to_int(learned_level, 0)))
        if isinstance(entry, dict):
            entry["level"] = normalized
            return
        setattr(entry, "level", normalized)

    @staticmethod
    def learned_entries(character, *, collection_name: str = "") -> List[Any]:
        collection_key = str(collection_name or "").strip().lower()
        if collection_key in {"skills", "spells"}:
            return list(getattr(character, collection_key, []) or [])

        entries: list[Any] = []
        collections = character.learned() if callable(getattr(character, "learned", None)) else [
            getattr(character, "skills", []),
            getattr(character, "spells", []),
        ]
        for learned in list(collections or []):
            entries.extend(list(learned or []))
        return entries

    @staticmethod
    def visible_learned_entries(character, visible_fn=None, *, collection_name: str = "") -> List[Any]:
        entries = []
        for entry in Character.learned_entries(character, collection_name=collection_name):
            if Character.learned_entry_level(entry) < 1:
                continue
            name = Character.learned_entry_name(entry)
            if not name:
                continue
            if callable(visible_fn) and not visible_fn(character, name):
                continue
            entries.append(entry)
        return entries

    @staticmethod
    def get_learned(character, learned_name, *, prefix: bool = False, visible_only: bool = False, visible_fn=None,
                    collection_name: str = ""):
        wanted = str(learned_name or "").strip().lower()
        if not wanted:
            return None

        entries = Character.visible_learned_entries(character, visible_fn, collection_name=collection_name) \
            if visible_only else Character.learned_entries(character, collection_name=collection_name)

        prefix_match = None
        for item in entries:
            name = Character.learned_entry_name(item).lower()
            if not name:
                continue
            if name == wanted:
                return item
            if prefix and prefix_match is None and name.startswith(wanted):
                prefix_match = item
        return prefix_match

    @staticmethod
    def set_learned(character, learned_name, learned_level, *, collection_name: str = "", create: bool = False):
        entry = Character.get_learned(character, learned_name, collection_name=collection_name)
        if entry is not None:
            Character._set_learned_entry_level(entry, learned_level)
            return entry

        if not create:
            raise ValueError(f"Learned skill with ID {learned_name} not found")

        collection_key = "spells" if str(collection_name or "").strip().lower() == "spells" else "skills"
        collection = getattr(character, collection_key, None)
        if collection is None:
            collection = []
            setattr(character, collection_key, collection)

        entry = {"name": str(learned_name or "").strip(), "level": 0}
        collection.append(entry)
        Character._set_learned_entry_level(entry, learned_level)
        return entry
