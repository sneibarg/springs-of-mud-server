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
    def has_player_controller(entity):
        from api.CharacterApi import CharacterApi

        return entity is not None and (not CharacterApi.is_npc(entity)
                                      or (getattr(entity, 'context', None) or {}).get('controller_original') is not None)

    @staticmethod
    def room_listeners(actor, room):
        from api.CharacterApi import CharacterApi

        if room is None:
            return []
        candidates = list(room.players_in_room() if actor is None else room.player_targets(actor))
        candidates.extend(mobile for mobile in room.mobiles.values()
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
                tokens[token] = ((entity.short_description or entity.name)
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
        variants = {str(player.id): render(player) for player in (room.characters if room is not None else {}).values()}
        return RecipientText(text, variants, fallback)

    @classmethod
    def act_text(cls, text, observer, room, actor, victim=None, item=None):
        entities = {token: entity for token, entity in (("$n", actor), ("$N", victim), ("$p", item))
                    if entity is not None and (token in text or token == "$N" and "$S" in text)}
        tokens = cls.visible_tokens(entities, observer, room)
        if "$S" in text:
            tokens["$S"] = victim.his_her() if tokens.get("$N", "someone") != "someone" else "their"
        if "$N" in text:
            tokens.setdefault("$N", "someone")
        for token, value in tokens.items():
            text = text.replace(token, value)
        return text[:1].upper() + text[1:].rstrip("\r\n") + "\r\n"

    @classmethod
    def combat_act(cls, actor, victim, room, *, to_char="", to_room="", to_victim="",
                   include_victim_in_room=False):
        from api.CharacterApi import CharacterApi

        payloads = []
        candidates = (
            (actor, to_char),
            (victim if victim is not actor else None, to_victim),
        )
        for recipient, text in candidates:
            if (text and cls.has_player_controller(recipient)
                    and CharacterApi.position_value(recipient) >= CharacterApi.pos_value("POS_RESTING")):
                payloads.append({"victim": recipient,
                                 "to_victim": cls.act_text(text, recipient, room, actor, victim)})
        if to_room:
            listeners = [entity for entity in cls.room_listeners(actor, room)
                         if include_victim_in_room or entity is not victim]
            if listeners:
                fallback = cls.act_text(to_room, None, room, actor, victim)
                variants = {str(entity.id): cls.act_text(to_room, entity, room, actor, victim)
                            for entity in listeners}
                payloads.append({"to_room": RecipientText(fallback, variants, fallback), "targets": listeners})
        return payloads

    @staticmethod
    def entity_name(entity, *, is_npc) -> str:
        if entity is None:
            return "someone"
        if is_npc(entity):
            return str(entity.short_description or entity.name)
        return str(entity.name)

    @staticmethod
    def display_effect_message(message) -> str:
        text = str(message or "").strip()
        if len(text) >= 2 and text.startswith("!") and text.endswith("!"):
            return ""
        return text
