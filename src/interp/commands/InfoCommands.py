from datetime import datetime
from typing import Any
from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from game.GenericUtil import GenericUtil
from game.WeatherHandler import WeatherHandler
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
    DAY_NAME = [
        "the Moon", "the Bull", "Deception", "Thunder", "Freedom",
        "the Great Gods", "the Sun"
    ]
    MONTH_NAME = [
        "Winter", "the Winter Wolf", "the Frost Giant", "the Old Forces",
        "the Grand Struggle", "the Spring", "Nature", "Futility", "the Dragon",
        "the Sun", "the Heat", "the Battle", "the Dark Shades", "the Shadows",
        "the Long Shadows", "the Ancient Darkness", "the Great Evil"
    ]
    SKY_LOOK = [
        "cloudless",
        "cloudy",
        "rainy",
        "lit by flashes of lightning",
    ]
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
                 session_handler: SessionHandler,
                 weather_handler: WeatherHandler):
        self.__name__ = "InfoCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.interp_registry = registry_service.interp_registry
        self.room_registry = registry_service.room_registry
        self.command_helper = command_helper
        self.room_helper = room_helper
        self.character_macros = character_macros
        self.player_helper = player_helper
        self.session_handler = session_handler
        self.weather_handler = weather_handler
        self.server_boot_time = datetime.now().ctime()
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

    def do_wimpy(self, character: Character, context: Context) -> str:
        if self.character_macros.is_npc(character):
            context.finish()
            return ""

        attributes = getattr(character, "character_attributes", None)
        if attributes is None:
            context.finish()
            return ""

        raw_arg = context.result if isinstance(context.result, str) else ""
        arg = raw_arg.strip() if raw_arg else (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip()

        if arg == "":
            wimpy = int(getattr(character, "max_hit", 0) / 5)
        elif not arg.lstrip("-").isdigit():
            context.finish()
            return "Your courage exceeds your wisdom.\r\n"
        else:
            wimpy = GenericUtil.to_int(arg, 0)

        if wimpy < 0:
            context.finish()
            return "Your courage exceeds your wisdom.\r\n"

        if wimpy > int(getattr(character, "max_hit", 0) / 2):
            context.finish()
            return "Such cowardice ill becomes you.\r\n"

        attributes.wimpy = wimpy
        context.finish()
        return f"Wimpy set to {wimpy} hit points.\r\n"

    def do_score(self, character: Character, context: Context) -> str:
        attributes = getattr(character, "character_attributes", None)
        if attributes is None:
            context.finish()
            return ""

        temporal = getattr(character, "temporal_mechanics", None)
        played = GenericUtil.to_int(getattr(temporal, "played", 0), 0)
        logon = GenericUtil.to_int(getattr(temporal, "logon", 0), 0)
        elapsed = int(datetime.now().timestamp()) - logon if logon > 0 else 0
        total_seconds = max(played + elapsed, 0)
        total_hours = total_seconds // 3600
        age_years = 17 + (total_seconds // 72000)

        trust = self.character_macros.get_trust(character)
        sex_text = str(getattr(character, "sex", "sexless") or "sexless").lower()
        if sex_text not in ("male", "female", "sexless"):
            sex_text = "sexless"

        inventory = list(getattr(character, "loot", []) or [])
        carry_number = len(inventory)
        item_weight = sum(GenericUtil.to_int(getattr(item, "weight", 0), 0) for item in inventory)
        coin_weight = int((GenericUtil.to_int(character.silver, 0) / 10) + (GenericUtil.to_int(character.gold, 0) * 2 / 5))
        carry_weight = item_weight + coin_weight
        max_items = GenericUtil.to_int(getattr(attributes, "max_items", 0), 0)
        max_weight = GenericUtil.to_int(getattr(attributes, "max_weight", 0), 0)

        lines = [
            f"You are {character.name}{character.title}, level {character.level}, {age_years} years old ({total_hours} hours).",
        ]
        if trust != character.level:
            lines.append(f"You are trusted at level {trust}.")

        lines.extend([
            f"Race: {character.race}  Sex: {sex_text}  Class: {character.character_class.name}",
            f"You have {character.hit}/{character.max_hit} hit, {character.mana}/{character.max_mana} mana, {character.movement}/{character.max_movement} movement.",
            f"You have {attributes.practices} practices and {attributes.trains} training sessions.",
            f"You are carrying {carry_number}/{max_items} items with weight {carry_weight // 10}/{max_weight // 10} pounds.",
            f"Str: {attributes.strength}({attributes.strength})  Int: {attributes.intelligence}({attributes.intelligence})  Wis: {attributes.wisdom}({attributes.wisdom})  Dex: {attributes.dexterity}({attributes.dexterity})  Con: {attributes.constitution}({attributes.constitution})",
            f"You have scored {character.experience} exp, and have {character.gold} gold and {character.silver} silver coins.",
        ])

        hero_level = self.character_macros.GameParametersEnum.LEVEL_HERO.value if self.character_macros.GameParametersEnum else 90
        if character.level < hero_level:
            next_total = GenericUtil.to_int(getattr(character, "accumulated_experience", 0), 0)
            if next_total > character.experience:
                lines.append(f"You need {next_total - character.experience} exp to level.")

        lines.append(f"Wimpy set to {attributes.wimpy} hit points.")

        char_context = character.context if isinstance(character.context, dict) else {}
        drunk = GenericUtil.to_int(getattr(character, "drunk", char_context.get("drunk", 0)), 0)
        thirst = GenericUtil.to_int(getattr(character, "thirst", char_context.get("thirst", 1)), 1)
        hunger = GenericUtil.to_int(getattr(character, "hunger", char_context.get("hunger", 1)), 1)
        if drunk > 10:
            lines.append("You are drunk.")
        if thirst == 0:
            lines.append("You are thirsty.")
        if hunger == 0:
            lines.append("You are hungry.")

        position_line = self._score_position_line(attributes)
        lines.append(position_line)

        ac_pierce = self.character_macros.get_ac(character, 0)
        ac_bash = self.character_macros.get_ac(character, 1)
        ac_slash = self.character_macros.get_ac(character, 2)
        ac_magic = self.character_macros.get_ac(character, 3)

        if character.level >= 25:
            lines.append(f"Armor: pierce: {ac_pierce}  bash: {ac_bash}  slash: {ac_slash}  magic: {ac_magic}")

        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_pierce, 'piercing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_bash, 'bashing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_slash, 'slashing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_magic, 'magic')}.")

        if self.character_macros.is_immortal(character):
            holy = "on" if self.character_macros.has_holy_light(character) else "off"
            imm_text = f"Holy Light: {holy}"
            if GenericUtil.to_int(getattr(character, "invis_level", 0), 0) > 0:
                imm_text += f"  Invisible: level {character.invis_level}"
            if GenericUtil.to_int(getattr(character, "incog_level", 0), 0) > 0:
                imm_text += f"  Incognito: level {character.incog_level}"
            lines.append(imm_text)

        if character.level >= 15:
            lines.append(
                f"Hitroll: {self.character_macros.get_hitroll(character)}  Damroll: {self.character_macros.get_damroll(character)}."
            )

        alignment = GenericUtil.to_int(getattr(attributes, "alignment", 0), 0)
        if character.level >= 10:
            lines.append(f"Alignment: {alignment}.")
        lines.append(f"You are {InfoUtil.score_alignment_word(alignment)}.")
        context.finish()
        return "\r\n".join(lines) + "\r\n"

    def do_time(self, context: Context) -> str:
        time_info = self.weather_handler.time_info
        if time_info is None:
            context.finish()
            return "Time is unavailable.\r\n"

        day = int(getattr(time_info, "day", 0)) + 1
        if 4 < day < 20:
            suf = "th"
        elif day % 10 == 1:
            suf = "st"
        elif day % 10 == 2:
            suf = "nd"
        elif day % 10 == 3:
            suf = "rd"
        else:
            suf = "th"

        hour = int(getattr(time_info, "hour", 0))
        month = int(getattr(time_info, "month", 0))
        text = (
            f"It is {12 if hour % 12 == 0 else hour % 12} o'clock "
            f"{'pm' if hour >= 12 else 'am'}, "
            f"Day of {self.DAY_NAME[day % 7]}, {day}{suf} the Month of {self.MONTH_NAME[month]}.\r\n"
            f"ROM started up at {self.server_boot_time}\r\n"
            f"The system time is {datetime.now().ctime()}.\r\n"
        )
        context.finish()
        return text

    def do_weather(self, character: Character, context: Context) -> str:
        if not self.character_macros.is_outside(character):
            context.finish()
            return "You can't see the weather indoors.\r\n"

        weather_info = self.weather_handler.weather_info
        if weather_info is None:
            context.finish()
            return "The weather is unavailable.\r\n"

        sky = getattr(weather_info, "sky", 0)
        if hasattr(sky, "value"):
            sky_index = int(sky.value)
        else:
            sky_index = int(sky)
        if sky_index < 0 or sky_index >= len(self.SKY_LOOK):
            sky_index = 0

        breeze = "a warm southerly breeze blows" if int(getattr(weather_info, "change", 0)) >= 0 else "a cold northern gust blows"
        context.finish()
        return f"The sky is {self.SKY_LOOK[sky_index]} and {breeze}.\r\n"

    def do_where(self, character: Character, context: Context) -> str:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        my_room = self.room_registry.get_or_none(id=character.room_id)
        if my_room is None:
            context.finish()
            return "None\r\n"

        room_flags = self.character_macros.enums.get("roomFlags")
        nowhere_bit = room_flags.ROOM_NOWHERE.value if room_flags and hasattr(room_flags, "ROOM_NOWHERE") else None

        if not arg:
            lines = ["Players near you:\r\n"]
            found = False
            for session in self.session_handler.get_playing_sessions():
                victim = session.character
                if victim is None or self.character_macros.is_npc(victim):
                    continue
                if victim.id == character.id:
                    continue
                room = self.room_registry.get_or_none(id=victim.room_id)
                if room is None:
                    continue
                if room.area_id != my_room.area_id:
                    continue
                if nowhere_bit is not None and self.character_macros.is_set(int(room.room_flags), nowhere_bit):
                    continue
                if not self.character_macros.can_see(character, victim, self.room_helper):
                    continue
                lines.append(f"{victim.name:<28} {room.name}\r\n")
                found = True

            if not found:
                lines.append("None\r\n")
            context.finish()
            return "".join(lines)

        wanted = arg
        for session in self.session_handler.get_playing_sessions():
            victim = session.character
            if victim is None:
                continue
            room = self.room_registry.get_or_none(id=victim.room_id)
            if room is None or room.area_id != my_room.area_id:
                continue
            if not self.character_macros.can_see(character, victim, self.room_helper):
                continue
            victim_name = (victim.name or "").lower()
            if victim_name == wanted or victim_name.startswith(wanted):
                context.finish()
                return f"{victim.name:<28} {room.name}\r\n"

        for room in self.room_registry.all_rooms():
            if room.area_id != my_room.area_id:
                continue
            for mob in room.mobiles.values():
                if mob is None:
                    continue
                if not self.character_macros.can_see(character, mob, self.room_helper):
                    continue
                mob_name = (getattr(mob, "name", "") or "").lower()
                short_name = (getattr(mob, "short_description", "") or "").lower()
                if mob_name == wanted or mob_name.startswith(wanted) or short_name.startswith(wanted):
                    display_name = getattr(mob, "short_description", None) or getattr(mob, "name", "someone")
                    context.finish()
                    return f"{display_name:<28} {room.name}\r\n"

        context.finish()
        return f"You didn't find any {wanted}.\r\n"

    def do_consider(self, character: Character, context: Context) -> str:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg:
            context.finish()
            return "Consider killing whom?\r\n"

        room = self.room_registry.get_or_none(id=character.room_id)
        if room is None:
            context.finish()
            return "They're not here.\r\n"

        victim = PlayerUtil.get_target(character, arg, room, self.character_macros, self.room_helper)
        if victim is None:
            context.finish()
            return "They're not here.\r\n"

        diff = GenericUtil.to_int(getattr(victim, "level", 0), 0) - GenericUtil.to_int(getattr(character, "level", 0), 0)
        if diff <= -10:
            msg = f"You can kill {getattr(victim, 'name', 'them')} naked and weaponless."
        elif diff <= -5:
            msg = f"{getattr(victim, 'name', 'They')} is no match for you."
        elif diff <= -2:
            msg = f"{getattr(victim, 'name', 'They')} looks like an easy kill."
        elif diff <= 1:
            msg = "The perfect match!"
        elif diff <= 4:
            msg = f"{getattr(victim, 'name', 'They')} says 'Do you feel lucky, punk?'."
        elif diff <= 9:
            msg = f"{getattr(victim, 'name', 'They')} laughs at you mercilessly."
        else:
            msg = "Death will thank you for your gift."

        context.finish()
        return msg + "\r\n"

    def _score_position_line(self, attributes: Any) -> str:
        position_value = GenericUtil.to_int(getattr(attributes, "position", 0), 0)
        positions = self.character_macros.PositionsEnum
        pos_dead = positions.POS_DEAD.value if positions and hasattr(positions, "POS_DEAD") else -1
        pos_mortal = positions.POS_MORTAL.value if positions and hasattr(positions, "POS_MORTAL") else -1
        pos_incap = positions.POS_INCAP.value if positions and hasattr(positions, "POS_INCAP") else -1
        pos_stunned = positions.POS_STUNNED.value if positions and hasattr(positions, "POS_STUNNED") else -1
        pos_sleeping = positions.POS_SLEEPING.value if positions and hasattr(positions, "POS_SLEEPING") else -1
        pos_resting = positions.POS_RESTING.value if positions and hasattr(positions, "POS_RESTING") else -1
        pos_sitting = positions.POS_SITTING.value if positions and hasattr(positions, "POS_SITTING") else -1
        pos_fighting = positions.POS_FIGHTING.value if positions and hasattr(positions, "POS_FIGHTING") else -1
        if position_value == pos_dead:
            return "You are DEAD!!"
        if position_value == pos_mortal:
            return "You are mortally wounded."
        if position_value == pos_incap:
            return "You are incapacitated."
        if position_value == pos_stunned:
            return "You are stunned."
        if position_value == pos_sleeping:
            return "You are sleeping."
        if position_value == pos_resting:
            return "You are resting."
        if position_value == pos_sitting:
            return "You are sitting."
        if position_value == pos_fighting:
            return "You are fighting."
        return "You are standing."

