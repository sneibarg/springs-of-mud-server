from typing import Any
from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from game.GenericUtil import GenericUtil
from interp.commands.InfoUtil import InfoUtil
from interp.CommandHelper import CommandHelper
from interp.Context import Context
from interp.HelpEntry import HelpEntry
from object.ItemUtil import ItemUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from player.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory
from server.session.SessionHandler import SessionHandler


class InfoCommands:
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
    def __init__(self,
                 registry_service: RegistryService,
                 command_helper: CommandHelper,
                 room_helper: RoomHelper,
                 character_macros: CharacterMacros,
                 player_helper: PlayerHelper,
                 session_handler: SessionHandler):
        self.__name__ = "InfoCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.interp_registry = registry_service.interp_registry
        self.room_registry = registry_service.room_registry
        self.command_helper = command_helper
        self.room_helper = room_helper
        self.character_macros = character_macros
        self.player_helper = player_helper
        self.session_handler = session_handler
        self.PlayerActBits = character_macros.enums.get('playerActBits')

    def do_quit(self, character: Character):
        room = self.room_registry.get(id=character.room_id)
        in_room = self.player_helper.players_in_room(character, room)
        return {
            "in_room": in_room,
            "to_char": "Alas, all good things must come to an end.\r\n",
            "to_room": f"{character.name} has left the game.\r\n",
        }

    def do_who(self, character: Character) -> str:
        who_list = [character] + PlayerUtil.visible(character, self.session_handler)
        lines = [
            f"[{c.level}    {c.race}    {c.character_class.name}] {c.name} {c.title}\r\n"
            for c in who_list
        ]
        lines.append(f"Players found: {len(who_list)}\r\n")
        return "".join(lines)

    def do_help(self, argument: str = "") -> str:
        arg_all = " ".join((argument or "").split()).lower()
        if not arg_all:
            arg_all = "summary"
        output_parts = []
        found = False
        for command in self.interp_registry.all_commands():
            help_entry: HelpEntry = command.help
            if help_entry is None or not help_entry.keyword:
                continue

            q_words = arg_all.split()
            k_words = help_entry.keyword.split()
            if (not q_words or not k_words) or not all(any(k.startswith(q) for k in k_words) for q in q_words):
                continue

            level_raw = getattr(help_entry, "level", 0)
            try:
                level = int(level_raw)
            except (TypeError, ValueError):
                level = 0

            if found:
                output_parts.append("\n\r============================================================\n\r\n\r")
            found = True

            if level >= 0 and arg_all != "imotd":
                output_parts.append(str(getattr(help_entry, "keyword", "")))
                output_parts.append("\n\r")

            text = str(getattr(help_entry, "text", "") or "")
            if text.startswith("."):
                text = text[1:]
            output_parts.append(text)

        return "".join(output_parts) if len(output_parts) > 0 else "No help on that word.\n\r"

    def look_target(self, character: Any, context: Context) -> str | None:
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return None

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 in ("", "auto", "i", "in", "on"):
            return None

        target = PlayerUtil.get_target(character, arg1, room, self.character_macros, self.room_helper)
        if target is None:
            context.jump_to(4)
            return None

        desc = (getattr(target, "description", "") or "").strip()
        if not desc:
            desc = "You see nothing special."

        lines = [desc, InfoUtil.target_condition_line(target)]
        equip_lines = self._target_equipment_lines(target)
        if equip_lines:
            lines.append("")
            lines.append(f"{(target.name or 'They')} is using:")
            lines.extend(equip_lines)

        context.finish()
        return "\r\n".join(lines) + "\r\n"

    def _target_equipment_lines(self, target: Any) -> list[str]:
        item_flags = self.character_macros.enums.get("itemFlags")
        lines = []

        equipped = getattr(target, "equipped", None)
        for slot, label in self.EQUIP_SLOT_LABELS:
            obj = None
            if equipped is not None:
                obj = equipped.get(slot) if isinstance(equipped, dict) else getattr(equipped, slot, None)
            if obj is None:
                obj = InfoUtil.find_inventory_item_for_slot(target, slot)
                if obj is None:
                    continue
            item_text = ItemUtil.format_obj_to_char(obj, item_flags_enum=item_flags, f_short=True)
            lines.append(f"{label}{item_text}")
        return lines

    async def do_look(self, character: Character, context: Context) -> str | None:
        if not self.command_helper.check_position(character):
            context.finish()
            return None

        if not self.room_helper.check_blind(character):
            context.finish()
            return "You can't see a thing!\n\r"

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if (not self.character_macros.is_npc(character)
                and not self.character_macros.has_holy_light(character)
                and self.room_helper.is_room_dark(character.room_id)):
            context.jump_to(1)  # show chars/mobs only
            return "It is pitch black ...\n\r"

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            context.finish()
            return None

        if arg1 == "" or arg1 == "auto":
            await context.room_handler().print_room(character.id, room)
            if self.character_macros.is_set(int(self.character_macros.convert_flags(character.character_flags.act)),
                                            self.PlayerActBits.PLR_AUTOEXIT.value):
                await context.room_handler().print_exits(character, room)
            context.jump_to(1)  # players + mobiles
            return None

        if arg1 in ("i", "in", "on"):
            context.jump_to(2)
            return None

        context.jump_to(3)
        return None

    def do_scroll(self, character: Character, context: Context) -> str:
        raw_arg = context.result if isinstance(context.result, str) else ""
        arg = raw_arg.strip() if raw_arg else (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip()
        if character.context is None:
            character.context = {}

        current_lines = GenericUtil.to_int(character.context.get("scroll_lines", 0), 0)

        if arg == "":
            display_lines = current_lines + 2 if current_lines > 0 else 0
            text = f"You currently display {display_lines} lines per page.\r\n"
            context.finish()
            return text

        if not arg.lstrip("-").isdigit():
            context.finish()
            return "You must provide a number.\r\n"

        lines = GenericUtil.to_int(arg, 0)
        if lines == 0:
            character.context["scroll_lines"] = 0
            context.finish()
            return "Paging disabled.\r\n"

        if lines < 10 or lines > 100:
            context.finish()
            return "You must provide a reasonable number.\r\n"

        character.context["scroll_lines"] = lines - 2
        context.finish()
        return f"Scroll set to {lines} lines.\r\n"
