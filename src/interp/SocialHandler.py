import re

from injector import inject

from api.CharacterApi import CharacterApi
from util.DisplayUtil import DisplayUtil
from util.GenericUtil import GenericUtil
from util.InterpUtil import InterpUtil
from util.LookupUtil import LookupUtil
from game.RandomNumberGenerator import RandomNumberGenerator
from area.RoomRegistry import RoomRegistry
from interp.SocialRegistry import SocialRegistry
from server.messaging import MessageBus
from player.PlayerHandler import PlayerHandler


class SocialHandler:
    @inject
    def __init__(self, message_bus: MessageBus, social_registry: SocialRegistry, player_handler: PlayerHandler, room_registry: RoomRegistry):
        self.message_bus = message_bus
        self.social_registry = social_registry
        self.player_handler = player_handler
        self.room_registry = room_registry
        self.rng = RandomNumberGenerator()

    async def handle_social(self, actor, raw_input: str, social=None) -> bool:
        name, arguments = InterpUtil.one_argument(raw_input or '')
        if not name:
            return False
        social = social or self.social_registry.get_or_none(name=name)
        if social is None:
            return False
        denial = self._denial(actor, social)
        if denial:
            await self.message_bus.send_to_character(actor.id, self.message_bus.text_to_message(denial + '\r\n'))
            return True
        room = self.room_registry.get(id=actor.room_id)
        target_name, _ = InterpUtil.one_argument(arguments)
        if not target_name:
            await self._send(social.char_no_arg, actor, None, room, 'actor')
            await self._send(social.others_no_arg, actor, None, room, 'room')
            return True
        target = LookupUtil.character(room, actor, target_name,
                                      visible=lambda victim: CharacterApi.can_see(actor, victim, room))
        if target is None:
            text = self._render(social.char_not_found, actor, observer=actor, room=room)
            if text:
                await self.message_bus.send_to_character(actor.id, self.message_bus.text_to_message(text + '\r\n'))
        elif target is actor:
            await self._send(social.char_auto, actor, target, room, 'actor')
            await self._send(social.others_auto, actor, target, room, 'room')
        else:
            await self._exchange(actor, target, room, social.char_found, social.others_found, social.vict_found)
            if (not CharacterApi.is_npc(actor) and CharacterApi.is_npc(target)
                    and not CharacterApi.is_affected(target, CharacterApi.get_enum('affectedBy').AFF_CHARM)
                    and CharacterApi.is_awake(target)
                    and self.message_bus.session_handler.get_session_by_character(target.id) is None):
                roll = self.rng.number_bits(4)
                if roll <= 8:
                    await self._exchange(target, actor, room, social.char_found, social.others_found, social.vict_found)
                elif roll <= 12:
                    await self._exchange(target, actor, room, 'You slap $N.', '$n slaps $N.', '$n slaps you.')
        return True

    @staticmethod
    def _denial(actor, social):
        if (not CharacterApi.is_npc(actor)
                and actor.status_flags.comm & CharacterApi.get_enum('commFlags').COMM_NOEMOTE):
            return 'You are anti-social!'
        positions = CharacterApi.get_enum('positions')
        position = CharacterApi.position_value(actor)
        if position == positions.POS_DEAD:
            return 'Lie still; you are DEAD.'
        if position in (positions.POS_INCAP, positions.POS_MORTAL):
            return 'You are hurt far too bad for that.'
        if position == positions.POS_STUNNED:
            return 'You are too stunned to do that.'
        if position == positions.POS_SLEEPING and social.name != 'snore':
            return 'In your dreams, or what?'
        return ''

    async def _exchange(self, actor, target, room, to_actor, to_room, to_target):
        await self._send(to_actor, actor, target, room, 'actor')
        await self._send(to_target, actor, target, room, 'target')
        await self._send(to_room, actor, target, room, 'others')

    async def _send(self, template, actor, target, room, channel):
        if not template:
            return
        resting = CharacterApi.get_enum('positions').POS_RESTING
        if channel in ('actor', 'target'):
            recipient = actor if channel == 'actor' else target
            if CharacterApi.position_value(recipient) >= resting:
                text = self._render(template, actor, target, observer=recipient, room=room)
                await self.message_bus.send_to_character(recipient.id, self.message_bus.text_to_message(text + '\r\n'))
        else:
            recipients = [person for person in room.players_in_room()
                          if person is not actor and (channel != 'others' or person is not target)
                          and CharacterApi.position_value(person) >= resting]
            text = DisplayUtil.room_text(
                self._render(template, actor, target, observer=actor, room=room),
                lambda observer: self._render(template, actor, target, observer=observer, room=room), room)
            await self.message_bus.send_to_room(self.message_bus.text_to_message(text + '\r\n'), recipients)

    @staticmethod
    def _render(template, actor, target=None, *, observer, room):
        names = DisplayUtil.visible_tokens({'actor': actor, 'target': target}, observer, room)
        if getattr(actor, 'cloaked', False) and observer is not actor:
            names['actor'] = 'someone'
        tokens = {'n': names['actor'], 'N': names['target'], '$': '$'}
        for entity, keys in ((actor, ('e', 'm', 's')), (target, ('E', 'M', 'S'))):
            sex = str(getattr(entity, 'sex', '0')).lower()
            index = {'male': 1, 'female': 2, 'neutral': 0}.get(sex)
            if index is None:
                index = max(0, min(2, GenericUtil.to_int(sex, 0)))
            tokens.update(zip(keys, (('it', 'it', 'its'), ('he', 'him', 'his'), ('she', 'her', 'her'))[index]))
        text = re.sub(r'\$([nNeEmMsS$])', lambda match: tokens[match[1]], template or '')
        text = text.replace('%actor%', names['actor']).replace('%target%', names['target'])
        return text[:1].upper() + text[1:]
