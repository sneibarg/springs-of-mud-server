"""ROM-style visible keyword and ordinal selection shared by gameplay paths."""
from util.InterpUtil import InterpUtil
from util.InfoUtil import InfoUtil
from util.GenericUtil import GenericUtil


class LookupUtil:
    @staticmethod
    def matches(selector, name):
        words = str(selector or "").strip().lower().split()
        return bool(words) and all(InfoUtil.look_keyword_matches(word, name) for word in words)

    @staticmethod
    def find(items, selector, *, visible=None):
        number, keyword = InterpUtil.number_argument(str(selector or "").strip())
        if number < 1 or not keyword:
            return None
        count = 0
        for item in items:
            if not LookupUtil.matches(keyword, getattr(item, "name", "")):
                continue
            if visible is not None and not visible(item):
                continue
            count += 1
            if count == number:
                return item
        return None

    @staticmethod
    def worn(character, item):
        return (character.equipped_slot_of(item) is not None
                or GenericUtil.to_int(getattr(item, "wear_loc", -1), -1) != -1)

    @staticmethod
    def inventory(character, selector, *, visible=None):
        return LookupUtil.find((item for item in character.owned_items()
                                if not LookupUtil.worn(character, item)), selector, visible=visible)

    @staticmethod
    def here(character, room, selector, *, visible=None):
        found = LookupUtil.find(list(getattr(room, "contents", {}).values()), selector, visible=visible)
        if found is not None:
            return found
        found = LookupUtil.inventory(character, selector, visible=visible)
        if found is not None:
            return found
        return LookupUtil.find((item for item in character.owned_items()
                                if LookupUtil.worn(character, item)), selector, visible=visible)

    @staticmethod
    def object_visible(observer, room, item):
        from util.ItemUtil import ItemUtil
        if observer is None:
            return True
        if room is None:
            from api.CharacterApi import CharacterApi
            try:
                registry = CharacterApi.get_registry()
                room = registry.room_registry.get_or_none(id=observer.room_id)
            except (RuntimeError, AttributeError):
                room = None
        return ItemUtil.can_see_object(room, observer, item)

    @staticmethod
    def people(room):
        people = getattr(room, "people", None)
        if callable(people):
            return list(people())
        return list((getattr(room, "characters", {}) or {}).values()) + list((getattr(room, "mobiles", {}) or {}).values())

    @staticmethod
    def character(room, observer, selector, *, visible=None):
        if str(selector or "").strip().lower() == "self":
            return observer
        return LookupUtil.find(LookupUtil.people(room), selector, visible=visible)
