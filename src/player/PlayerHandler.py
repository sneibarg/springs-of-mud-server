from typing import Any
from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from interp.CommandHelper import CommandHelper
from interp.Context import Context
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerUtil import PlayerUtil
from player.PlayerHelper import PlayerHelper
from object.ItemUtil import ItemUtil
from server.messaging import MessageBus
from server.session.SessionHandler import SessionHandler
from server.LoggerFactory import LoggerFactory


class PlayerHandler:
    EQUIP_SLOT_LABELS = [
        ("light", "<used as light>      "),
        ("finger1", "<worn on finger>    "),
        ("finger2", "<worn on finger>    "),
        ("neck1", "<worn around neck>   "),
        ("neck2", "<worn around neck>   "),
        ("torso", "<worn on torso>      "),
        ("head", "<worn on head>       "),
        ("legs", "<worn on legs>       "),
        ("feet", "<worn on feet>       "),
        ("hands", "<worn on hands>      "),
        ("arms", "<worn on arms>       "),
        ("shield", "<worn as shield>     "),
        ("body", "<worn about body>     "),
        ("waist", "<worn about waist>    "),
        ("wrist1", "<worn around wrist>  "),
        ("wrist2", "<worn around wrist>  "),
        ("wielded", "<wielded>            "),
        ("held", "<held>               "),
        ("floating_nearby", "<floating nearby>    "),
    ]
    @inject
    def __init__(self, message_bus: MessageBus,
                 registry_service: RegistryService,
                 session_handler: SessionHandler,
                 command_helper: CommandHelper,
                 room_helper: RoomHelper,
                 player_helper: PlayerHelper,
                 character_macros: CharacterMacros):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.character_registry = registry_service.character_registry
        self.room_registry = registry_service.room_registry
        self.session_handler = session_handler
        self.command_helper = command_helper
        self.room_helper = room_helper
        self.player_helper = player_helper
        self.character_macros = character_macros
        self.PlayerActBits = character_macros.enums.get('playerActBits')
        self.logger = LoggerFactory.get_logger(__name__)

    async def do_quit(self, character: Character, context: Context):
        room = self.room_registry.get(id=character.room_id)
        in_room = self.player_helper.players_in_room(character, room)
        message = self.message_bus.text_to_message(f"{character.name} has left the game.\r\n")
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(f"Alas, all good things must come to an end.\r\n"))
        if len(in_room) > 0:
            await self.message_bus.send_to_room(message, in_room)
        self.session_handler.remove_session(character.id)
        await context.disconnect()

    async def print_players_in_room(self, character: Character):
        message = self.player_helper.get_players_in_room(character)
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message))

    async def do_who(self, character):
        who_list = [character] + PlayerUtil.visible(character, self.session_handler)
        who_line = ""
        players_found = "Players found: " + str(len(who_list)) + "\r\n"
        for c in who_list:
            who_line = who_line + f"[{c.level}    {c.race}    {c.character_class.name}] {c.name} {c.title}\r\n"

        who_line = who_line + players_found
        message = self.message_bus.text_to_message(who_line)
        await self.message_bus.send_to_character(character.id, message)

    async def to_player(self, character_id, msg: str):
        text = msg + "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character_id, message)

    async def to_target(self, context: Context):
        target = self.character_registry.get_or_none(name=context.parameters[0])
        if target is None:
            await self.message_bus.send_to_character(context.character.id, self.message_bus.text_to_message("They aren't here.\r\n"))
            return
        text = context.parameters[1] + "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(target.id, message)

    async def to_room(self, character: Character, msg: str):
        room = self.room_registry.get(id=character.room_id)
        text = msg.replace("%c", character.name).replace("%m", msg)
        message = self.message_bus.text_to_message(text)
        in_room = self.player_helper.players_in_room(character, room)
        await self.message_bus.send_to_room(message, in_room)

    async def look_target(self, character: Any, context: Context):
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 in ("", "auto", "i", "in", "on"):
            return

        target = PlayerUtil.get_target(character, arg1, room, self.character_macros, self.room_helper)
        if target is None:
            context.jump_to(4)
            return

        desc = (getattr(target, "description", "") or "").strip()
        if not desc:
            desc = "You see nothing special."

        lines = [desc, self._target_condition_line(target)]
        equip_lines = self._target_equipment_lines(target)
        if equip_lines:
            lines.append("")
            lines.append(f"{(target.name or 'They')} is using:")
            lines.extend(equip_lines)

        text = "\r\n".join(lines) + "\r\n"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
        context.finish()

    @staticmethod
    def _target_condition_line(target: Any) -> str:
        hit = getattr(target, "hit")
        max_hit = getattr(target, "max_hit")
        try:
            hit = int(hit)
            max_hit = int(max_hit)
        except (TypeError, ValueError):
            hit, max_hit = 0, 0

        if max_hit > 0:
            percent = (100 * hit) // max_hit
        else:
            percent = -1

        name = (getattr(target, "name", None) or "They")
        if percent >= 100:
            return f"{name} is in excellent condition."
        if percent >= 90:
            return f"{name} has a few scratches."
        if percent >= 75:
            return f"{name} has some small wounds and bruises."
        if percent >= 50:
            return f"{name} has quite a few wounds."
        if percent >= 30:
            return f"{name} has some big nasty wounds and scratches."
        if percent >= 15:
            return f"{name} looks pretty hurt."
        if percent >= 0:
            return f"{name} is in awful condition."
        return f"{name} is bleeding to death."

    def _target_equipment_lines(self, target: Any) -> list[str]:
        item_flags = self.character_macros.enums.get("itemFlags")
        lines = []

        equipped = getattr(target, "equipped", None)
        for slot, label in self.EQUIP_SLOT_LABELS:
            obj = None
            if equipped is not None:
                obj = equipped.get(slot) if isinstance(equipped, dict) else getattr(equipped, slot, None)
            if obj is None:
                obj = self._find_inventory_item_for_slot(target, slot)
                if obj is None:
                    continue
            item_text = ItemUtil.format_obj_to_char(obj, item_flags_enum=item_flags, f_short=True)
            lines.append(f"{label}{item_text}")
        return lines

    @staticmethod
    def _find_inventory_item_for_slot(target: Any, slot: str):
        from game.Equipped import WEAR_LOC_TO_EQUIPPED_SLOT
        wanted_locs = [loc for loc, slot_name in WEAR_LOC_TO_EQUIPPED_SLOT.items() if slot_name == slot]
        if not wanted_locs:
            return None
        inventory = getattr(target, "inventory", None) or []
        for item in inventory:
            try:
                wear_loc = int(getattr(item, "wear_loc", -1))
            except (TypeError, ValueError):
                wear_loc = -1
            if wear_loc in wanted_locs:
                return item
        return None

    async def do_look(self, character: Character, context: Context):
        if not self.command_helper.check_position(character):
            context.finish()
            return

        if not self.room_helper.check_blind(character):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You can't see a thing!\n\r"))
            context.finish()
            return

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if (not self.character_macros.is_npc(character)
                and not self.character_macros.has_holy_light(character)
                and self.room_helper.is_room_dark(character.room_id)):
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("It is pitch black ...\n\r"))
            context.jump_to(1)  # show chars/mobs only
            return

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            context.finish()
            return

        if arg1 == "" or arg1 == "auto":
            await context.room_handler().print_room(character.id, room)
            if self.character_macros.is_set(int(self.character_macros.convert_flags(character.character_flags.act)), self.PlayerActBits.PLR_AUTOEXIT.value):
                await context.room_handler().print_exits(character, room)
            context.jump_to(1)  # players + mobiles
            return

        if arg1 in ("i", "in", "on"):
            context.jump_to(2)
            return

        context.jump_to(3)
        return
