from injector import inject
from registry.PlayerRegistry import PlayerRegistry
from registry.CharacterRegistry import CharacterRegistry
from registry.MobileRegistry import MobileRegistry
from registry.AreaRegistry import AreaRegistry
from registry.RoomRegistry import RoomRegistry
from registry.ItemRegistry import ItemRegistry
from registry.SkillRegistry import SkillRegistry


class RegistryService:
    @inject
    def __init__(self,
                 player_registry: PlayerRegistry,
                 character_registry: CharacterRegistry,
                 mobile_registry: MobileRegistry,
                 area_registry: AreaRegistry,
                 room_registry: RoomRegistry,
                 item_registry: ItemRegistry,
                 skill_registry: SkillRegistry):

        self.player_registry = player_registry
        self.character_registry = character_registry
        self.mobile_registry = mobile_registry
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.item_registry = item_registry
        self.skill_registry = skill_registry
