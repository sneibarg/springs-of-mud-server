"""Read-only immortal diagnostics over live world state and prototypes."""
from api.AreaApi import AreaApi
from api.CharacterApi import CharacterApi
from api.InterpApi import InterpApi
from item.ItemOwnership import ItemOwnership
from util.LookupUtil import LookupUtil
from util.WizUtil import WizUtil


class WizDiagnostics:
    def __init__(self, registries, handler):
        self.registries = registries
        self.handler = handler
        self.rooms = registries.room_registry
        self.characters = registries.character_registry

    @staticmethod
    def text(lines):
        return '\r\n'.join(lines) + ('\r\n' if lines else '')

    def mwhere(self, actor, argument):
        lines = []
        actor_room = self.rooms.get_or_none(id=actor.room_id)
        if not argument:
            for session in self.handler.session_handler.get_playing_sessions():
                target = session.character
                room = None if target is None else self.rooms.get_or_none(id=target.room_id)
                if room is None or not CharacterApi.can_see(actor, target, actor_room) or not CharacterApi.can_see_room(actor, room):
                    continue
                original = session.metadata.get('switched_original')
                name = (f'{original.name} (in the body of {WizUtil.display_name(target)})'
                        if original is not None else target.name)
                lines.append(f'{len(lines) + 1}) {name} is in {room.name} [{room.vnum}]')
            return self.text(lines)
        for target in WizUtil.live_world_entities(self.rooms):
            if not WizUtil.name_matches(argument, target.name):
                continue
            room = self.rooms.get_or_none(id=target.room_id)
            vnum = getattr(target, 'vnum', 0) if CharacterApi.is_npc(target) else 0
            lines.append(f'{len(lines) + 1}) [{vnum}] {WizUtil.display_name(target)} - [{room.vnum}] {room.name}')
        return self.text(lines) if lines else f"You didn't find any {argument}.\r\n"

    def owhere(self, actor, argument):
        if not argument:
            return 'Find what?\r\n'
        actor_room = self.rooms.get_or_none(id=actor.room_id)
        lines = []
        for obj, _, location in ItemOwnership(None, self.rooms).walk_world_items():
            if (not WizUtil.name_matches(argument, obj.name) or actor.level < obj.level
                    or not LookupUtil.object_visible(actor, actor_room, obj)):
                continue
            room = location['room']
            holder = location['parent']
            if location['kind'] != 'room' and CharacterApi.can_see(actor, holder, actor_room):
                place = f'is carried by {WizUtil.display_name(holder)} [Room {room.vnum}]'
            elif location['kind'] == 'room' and CharacterApi.can_see_room(actor, room):
                place = f'is in {room.name} [Room {room.vnum}]'
            else:
                place = 'is somewhere'
            lines.append(f'{len(lines) + 1}) {obj.short_description} {place}')
            if len(lines) >= 200:
                break
        return self.text(lines) if lines else 'Nothing like that in heaven or earth.\r\n'

    def vnum(self, argument):
        kind, rest = WizUtil.split_argument(argument)
        if not kind:
            return InterpApi.command_payload('syntax')
        if kind in ('skill', 'spell'):
            abilities = [*self.registries.skill_registry.all_skills(), *self.registries.spell_registry.all_spells()]
            matches = [ability for ability in abilities if rest == 'all' or (rest and (
                ability.name.lower().startswith(rest.lower()) or str(getattr(ability, 'id', '')) == rest))]
            if rest != 'all':
                exact = [ability for ability in matches if ability.name.lower() == rest.lower()]
                matches = (exact or matches)[:1]
            return {'to_char': self.text([f"{ability.name}: id {getattr(ability, 'id', '')}, slot {getattr(ability, 'slot', 0)}" for ability in matches]) or 'No such skill or spell.\r\n'}
        query = rest if kind in ('obj', 'mob', 'char') else argument
        lines = []
        sources = []
        if kind != 'obj':
            sources.append(('M', self.registries.mobile_registry.all_mobiles()))
        if kind not in ('mob', 'char'):
            sources.append(('O', self.registries.item_registry.all_items()))
        for label, prototypes in sources:
            for obj in sorted(prototypes, key=lambda value: str(value.vnum)):
                if query == 'all' or (query and WizUtil.name_matches(query, obj.name)):
                    lines.append(f'{label} [{obj.vnum}] {obj.short_description}')
        return {'to_char': self.text(lines) or 'No vnum has that keyword.\r\n'}

    @staticmethod
    def fields(target, names):
        return ', '.join(f'{name}: {getattr(target, name, "")}' for name in names)

    @classmethod
    def effects(cls, target):
        return [f'Affect: {cls.fields(effect, ("type", "where", "level", "duration", "location", "modifier", "bitvector"))}'
                for effect in getattr(target, 'effects', []) or []]

    @classmethod
    def character_text(cls, target):
        lines = [f'{WizUtil.display_name(target)} [{getattr(target, "vnum", 0)}]',
                 cls.fields(target, ('name', 'id', 'room_id', 'race', 'character_class', 'level', 'trust', 'sex', 'position')),
                 f'Hit: {target.hit}/{target.max_hit} Mana: {target.mana}/{target.max_mana} Move: {target.movement}/{target.max_movement}',
                 cls.fields(target, ('gold', 'silver', 'hit_roll', 'dam_roll', 'saving_throw', 'timer', 'size', 'material')),
                 f'Attributes: {getattr(target, "character_attributes", "")}',
                 f'Armor: {getattr(target, "armor_class", "")}',
                 f'Flags: {getattr(target, "status_flags", "")}',
                 cls.fields(target, ('special_name', 'description')),
                 'Master: ' + WizUtil.display_name(getattr(target, 'master', None)) + ' Leader: ' + WizUtil.display_name(getattr(target, 'leader', None))]
        lines.extend(cls.effects(target))
        lines.append('Carrying: ' + ', '.join(WizUtil.display_name(item) for item in target.owned_items()))
        return cls.text(lines)

    @classmethod
    def object_text(cls, obj):
        lines = [f'Obj [{obj.vnum}] {obj.short_description}',
                 cls.fields(obj, ('name', 'id', 'item_type', 'extra_flags', 'wear_flags', 'material', 'owner')),
                 cls.fields(obj, ('level', 'weight', 'cost', 'timer', 'condition', 'enchanted')),
                 cls.fields(obj, ('value0', 'value1', 'value2', 'value3', 'value4')),
                 f'Description: {obj.long_description}', f'Extra descriptions: {obj.extra_description}',
                 'Contains: ' + ', '.join(WizUtil.display_name(item) for item in obj.contains)]
        return cls.text(lines + cls.effects(obj))

    @classmethod
    def room_text(cls, room):
        lines = [f'Room [{room.vnum}] {room.name}',
                 cls.fields(room, ('area_id', 'room_flags', 'sector_type', 'light', 'heal_rate', 'mana_rate', 'owner', 'clan')),
                 room.description, f'Extra descriptions: {room.extra_description}',
                 'Characters: ' + ', '.join(WizUtil.display_name(value) for value in [*room.characters.values(), *room.mobiles.values()]),
                 'Objects: ' + ', '.join(WizUtil.display_name(value) for value in room.contents.values())]
        lines.extend('Exit: ' + cls.fields(exit_, ('direction', 'to_room_vnum', 'key', 'exit_flags', 'keyword', 'description')) for exit_ in room.exits)
        return cls.text(lines)

    def stat(self, actor, argument):
        kind, rest = WizUtil.split_argument(argument)
        if not kind:
            return InterpApi.command_payload('syntax')
        room_mode = kind in ('room', 'r')
        if room_mode:
            room = (AreaApi.find_location(rest, self.rooms, self.characters, WizUtil.name_matches, observer=actor)
                    if rest else self.rooms.get_or_none(id=actor.room_id))
        else:
            query = rest if kind in ('char', 'mob', 'player', 'm', 'obj', 'item', 'o') else argument
            if kind not in ('char', 'mob', 'player', 'm'):
                obj = WizUtil.find_world_item(self.characters, self.rooms, query, observer=actor)
                if obj is not None:
                    return {'to_char': self.object_text(obj)}
            if kind not in ('obj', 'item', 'o'):
                target = WizUtil.find_world_entity(self.characters, self.rooms, query, observer=actor)
                if target is not None:
                    return {'to_char': self.character_text(target)}
            room = (None if kind in ('char', 'mob', 'player', 'm', 'obj', 'item', 'o') else
                    AreaApi.find_location(argument, self.rooms, self.characters, WizUtil.name_matches, observer=actor))
        if room is None:
            return InterpApi.command_payload('room_missing' if room_mode else 'no_such_target')
        if self.handler.room_is_private_for_actor(actor, room, implementor_only=True):
            return {'to_char': 'That room is private right now.\r\n'}
        return {'to_char': self.room_text(room)}
