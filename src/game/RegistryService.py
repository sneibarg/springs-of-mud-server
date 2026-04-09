from injector import inject

from area.ResetRegistry import ResetRegistry
from area.ShopRegistry import ShopRegistry
from area.SpecialRegistry import SpecialRegistry
from player.PlayerRegistry import PlayerRegistry
from player.CharacterRegistry import CharacterRegistry
from mobile.MobileRegistry import MobileRegistry
from area.AreaRegistry import AreaRegistry
from area.RoomRegistry import RoomRegistry
from object.ItemRegistry import ItemRegistry
from skill.SkillRegistry import SkillRegistry


class RegistryService:
    @inject
    def __init__(self,
                 player_registry: PlayerRegistry,
                 character_registry: CharacterRegistry,
                 mobile_registry: MobileRegistry,
                 area_registry: AreaRegistry,
                 room_registry: RoomRegistry,
                 item_registry: ItemRegistry,
                 skill_registry: SkillRegistry,
                 shop_registry: ShopRegistry,
                 reset_registry: ResetRegistry,
                 special_registry: SpecialRegistry):

        self.player_registry = player_registry
        self.character_registry = character_registry
        self.mobile_registry = mobile_registry
        self.area_registry = area_registry
        self.room_registry = room_registry
        self.item_registry = item_registry
        self.skill_registry = skill_registry
        self.shop_registry = shop_registry
        self.reset_registry = reset_registry
        self.special_registry = special_registry
