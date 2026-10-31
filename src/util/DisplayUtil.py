class RecipientText(str):
    """Text whose observer-specific variants survive ordinary concatenation."""

    def __new__(cls, text, variants, fallback):
        value = super().__new__(cls, text)
        value.variants = variants
        value.fallback = fallback
        return value

    def for_recipient(self, recipient_id):
        return self.variants.get(str(recipient_id), self.fallback)

    def __add__(self, other):
        if isinstance(other, RecipientText):
            keys = self.variants.keys() | other.variants.keys()
            variants = {key: self.for_recipient(key) + other.for_recipient(key) for key in keys}
            fallback = self.fallback + other.fallback
        else:
            variants = {key: text + other for key, text in self.variants.items()}
            fallback = self.fallback + other
        return RecipientText(str(self) + str(other), variants, fallback)

    def __radd__(self, other):
        return RecipientText(other + str(self), {key: other + text for key, text in self.variants.items()},
                             other + self.fallback)


class DisplayUtil:
    @staticmethod
    def room_listeners(actor, room):
        from api.CharacterApi import CharacterApi

        if room is None:
            return []
        candidates = list(room.player_targets(actor))
        candidates.extend(mobile for mobile in getattr(room, 'mobiles', {}).values()
                          if mobile is not actor
                          and (getattr(mobile, 'context', None) or {}).get('controller_original') is not None)
        resting = CharacterApi.pos_value('POS_RESTING')
        return [listener for listener in candidates if CharacterApi.position_value(listener) >= resting]

    @staticmethod
    def visible_tokens(entities, observer, room):
        from api.CharacterApi import CharacterApi

        tokens = {}
        for token, entity in entities.items():
            if entity is None:
                tokens[token] = ""
            elif hasattr(entity, "item_type"):
                from util.LookupUtil import LookupUtil
                tokens[token] = ((getattr(entity, "short_description", "") or getattr(entity, "name", "something"))
                                 if observer is not None and LookupUtil.object_visible(observer, room, entity)
                                 else "something")
            else:
                tokens[token] = (DisplayUtil.entity_name(entity, is_npc=CharacterApi.is_npc)
                                 if observer is not None and CharacterApi.can_see(observer, entity, room)
                                 else "someone")
        return tokens

    @staticmethod
    def room_text(text, render, room):
        fallback = render(None)
        variants = {str(player.id): render(player) for player in getattr(room, "characters", {}).values()}
        return RecipientText(text, variants, fallback)

    @staticmethod
    def entity_name(entity, *, is_npc) -> str:
        if entity is None:
            return "someone"
        if is_npc(entity):
            return str(getattr(entity, "short_description", "") or getattr(entity, "name", "someone"))
        return str(getattr(entity, "name", "someone"))

    @staticmethod
    def display_effect_message(message) -> str:
        text = str(message or "").strip()
        if len(text) >= 2 and text.startswith("!") and text.endswith("!"):
            return ""
        return text
