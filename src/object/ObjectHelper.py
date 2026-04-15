from injector import inject
from area.RoomHelper import RoomHelper
from object.ObjectMacros import ObjectMacros
from player.Character import Character
from object.Item import Item
from player.CharacterMacros import CharacterMacros
from server.LoggerFactory import LoggerFactory


class ObjectHelper:
    @inject
    def __init__(self, object_macros: ObjectMacros, character_macros: CharacterMacros, room_helper: RoomHelper):
        self.__name__ = "ObjectHelper"
        self.logger = LoggerFactory.get_logger(__name__)
        self.object_macros = object_macros
        self.character_macros = character_macros
        self.room_helper = room_helper
        self.PlayerActBits = self.character_macros.PlayerActBits
        self.AffectBits = self.object_macros.AffectBits
        self.ItemFlags = self.object_macros.ItemFlags
        self.ItemTypes = self.object_macros.ItemTypes

    def can_see_object(self, character: Character, obj: Item) -> bool:
        if not self.character_macros.is_npc(character) and self.character_macros.is_set(int(self.character_macros.convert_flags(character.character_flags.act)), self.PlayerActBits.PLR_HOLYLIGHT.value):
            return True

        if self.object_macros.is_set(int(obj.extra_flags), self.ItemFlags.ITEM_VIS_DEATH.value):
            return False

        if self.character_macros.is_affected(character, self.AffectBits.AFF_BLIND.value) and obj.item_type != self.ItemTypes.ITEM_POTION.value:
            return False

        if obj.item_type == self.ItemTypes.ITEM_LIGHT.value and int(obj.value2) != 0:
            return True

        if self.object_macros.is_set(int(obj.extra_flags), self.ItemFlags.ITEM_INVIS.value and not self.character_macros.is_affected(character, self.AffectBits.AFF_DETECT_INVIS.value)):
            return False

        if self.object_macros.is_set(int(obj.extra_flags), self.ItemFlags.ITEM_GLOW.value):
            return True

        if self.room_helper.is_room_dark(character.room_id) and not self.character_macros.is_affected(character, self.AffectBits.AFF_DARK_VISION.value):
            return False

        return True
