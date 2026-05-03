from datetime import datetime
from typing import Any
from injector import inject

from area.RoomHelper import RoomHelper
from game.RegistryService import RegistryService
from util.GenericUtil import GenericUtil
from game.WeatherHandler import WeatherHandler
from util.InfoUtil import InfoUtil
from interp.CommandHelper import CommandHelper
from interp.Context import Context
from interp.HelpEntry import HelpEntry
from util.InterpUtil import InterpUtil
from util.ItemUtil import ItemUtil
from player.Character import Character
from player.CharacterMacros import CharacterMacros
from player.PlayerHelper import PlayerHelper
from util.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory
from server.session.SessionHandler import SessionHandler
from util.SkillUtil import SkillUtil

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


class InfoCommands:
    @inject
    def __init__(self,
                 registry_service: RegistryService, command_helper: CommandHelper, room_helper: RoomHelper,
                 player_helper: PlayerHelper,session_handler: SessionHandler, weather_handler: WeatherHandler):
        self.__name__ = "InfoCommands"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.interp_registry = registry_service.interp_registry
        self.room_registry = registry_service.room_registry
        self.skill_registry = registry_service.skill_registry
        self.spell_registry = getattr(registry_service, "spell_registry", None)
        self.command_helper = command_helper
        self.room_helper = room_helper
        self.player_helper = player_helper
        self.session_handler = session_handler
        self.weather_handler = weather_handler
        self.server_boot_time = datetime.now().ctime()
        self.PlayerActBits = None

    def lazy_load(self):
        self.PlayerActBits = CharacterMacros.get_enum('playerActBits')

    def do_quit(self, character: Character):
        room = self.room_registry.get(id=character.room_id)
        in_room = self.player_helper.players_in_room(character, room)
        return {
            "people": in_room,
            "to_char": "Alas, all good things must come to an end.\r\n",
            "to_room": f"{character.name} has left the game.\r\n",
        }

    def do_who(self, character: Character) -> str:
        who_list = [character] + PlayerUtil.visible(character, self.session_handler)
        lines = [
            f"{CharacterMacros.who_line(character, c)}\r\n"
            for c in who_list
        ]
        lines.append(f"Players found: {len(who_list)}\r\n")
        return "".join(lines)

    def do_help(self, argument: str = "") -> str:
        arg_all = " ".join((argument or "").split()).lower()
        if not arg_all:
            arg_all = "summary"
        q_words = [CharacterMacros.normalize_help_token(w) for w in arg_all.split()]
        q_words = [w for w in q_words if w]
        output_parts = []
        found = False
        emitted_help_ids: set[str] = set()
        for command in self.interp_registry.all_commands():
            help_entry: HelpEntry = command.help
            if help_entry is None or not help_entry.keyword:
                continue
            help_id = str(getattr(help_entry, "id", "") or "")
            if help_id and help_id in emitted_help_ids:
                continue

            k_words = [CharacterMacros.normalize_help_token(w) for w in str(help_entry.keyword).split()]
            k_words = [w for w in k_words if w]
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
            if help_id:
                emitted_help_ids.add(help_id)

        return "".join(output_parts) if len(output_parts) > 0 else "No help on that word.\n\r"

    def look_target(self, character: Any, context: Context) -> str | None:
        room = self.room_registry.get(id=character.room_id)
        if room is None:
            return None

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 in ("", "auto", "i", "in", "on"):
            return None

        target = PlayerUtil.get_target(character, arg1, room, self.room_helper)
        if target is None:
            context.jump_to(4)
            return None

        desc = (getattr(target, "description", "") or "").strip()
        if not desc:
            desc = "You see nothing special."

        lines = [desc, InfoUtil.target_condition_line(target)]
        equip_lines = CharacterMacros.target_equipment_lines(target, EQUIP_SLOT_LABELS)
        if equip_lines:
            lines.append("")
            lines.append(f"{(target.name or 'They')} is using:")
            lines.extend(equip_lines)

        context.finish()
        return "\r\n".join(lines) + "\r\n"

    async def do_look(self, character: Character, context: Context) -> str | None:
        if not await self.command_helper.check_position(character):
            context.finish()
            return None

        if not self.room_helper.check_blind(character):
            context.finish()
            return "You can't see a thing!\n\r"

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if (not CharacterMacros.is_npc(character)
                and not CharacterMacros.has_holy_light(character)
                and self.room_helper.is_room_dark(character.room_id)):
            context.jump_to(1)  # show chars/mobs only
            return "It is pitch black ...\n\r"

        room = self.room_registry.get(id=character.room_id)
        if room is None:
            context.finish()
            return None

        if arg1 == "" or arg1 == "auto":
            await context.room_handler().print_room(character.id, room)
            if CharacterMacros.is_set(CharacterMacros.get_act_flags(character), self.PlayerActBits.PLR_AUTOEXIT.value):
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
        if CharacterMacros.is_npc(character):
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

        character_race = getattr(character, "character_race", None)
        status_flags = getattr(character, "status_flags", None)
        played = GenericUtil.to_int(getattr(status_flags, "played", 0), 0)
        logon = GenericUtil.to_int(getattr(status_flags, "logon", 0), 0)
        elapsed = int(datetime.now().timestamp()) - logon if logon > 0 else 0
        total_seconds = max(played + elapsed, 0)
        total_hours = total_seconds // 3600
        age_years = 17 + (total_seconds // 72000)

        trust = CharacterMacros.get_trust(character)
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
            f"Str: {attributes.strength}({character_race.max_strength})  Int: {attributes.intelligence}({character_race.max_intelligence})  Wis: {attributes.wisdom}({character_race.max_wisdom})  Dex: {attributes.dexterity}({character_race.max_dexterity})  Con: {attributes.constitution}({character_race.max_constitution})",
            f"You have scored {attributes.accumulated_experience} exp, and have {character.gold} gold and {character.silver} silver coins.",
            f"You need {attributes.experience_per_level - attributes.experience} exp to level."
        ])

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

        position_line = CharacterMacros.score_position_line(attributes)
        lines.append(position_line)

        ac_pierce = CharacterMacros.get_ac(character, 0)
        ac_bash = CharacterMacros.get_ac(character, 1)
        ac_slash = CharacterMacros.get_ac(character, 2)
        ac_magic = CharacterMacros.get_ac(character, 3)

        if character.level >= 25:
            lines.append(f"Armor: pierce: {ac_pierce}  bash: {ac_bash}  slash: {ac_slash}  magic: {ac_magic}")

        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_pierce, 'piercing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_bash, 'bashing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_slash, 'slashing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_magic, 'magic')}.")

        if CharacterMacros.is_immortal(character):
            holy = "on" if CharacterMacros.has_holy_light(character) else "off"
            imm_text = f"Holy Light: {holy}"
            if GenericUtil.to_int(getattr(character.status_flags, "invis_level", 0), 0) > 0:
                imm_text += f"  Invisible: level {character.status_flags.invis_level}"
            if GenericUtil.to_int(getattr(character.status_flags, "incog_level", 0), 0) > 0:
                imm_text += f"  Incognito: level {character.status_flags.incog_level}"
            lines.append(imm_text)

        if character.level >= 15:
            lines.append(
                f"Hitroll: {CharacterMacros.get_hitroll(character)}  Damroll: {CharacterMacros.get_damroll(character)}."
            )

        alignment = GenericUtil.to_int(getattr(attributes, "alignment", 0), 0)
        if character.level >= 10:
            lines.append(f"Alignment: {alignment}.")
        lines.append(f"You are {InfoUtil.score_alignment_word(alignment)}.")
        if CharacterMacros.is_comm_enabled(character, "COMM_SHOW_AFFECTS"):
            lines.append("")
            lines.append(CharacterMacros.format_affects(character).rstrip("\r\n"))
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
            f"Day of {DAY_NAME[day % 7]}, {day}{suf} the Month of {MONTH_NAME[month]}.\r\n"
            f"ROM started up at {self.server_boot_time}\r\n"
            f"The system time is {datetime.now().ctime()}.\r\n"
        )
        context.finish()
        return text

    def do_weather(self, character: Character, context: Context) -> str:
        if not CharacterMacros.is_outside(character):
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
        if sky_index < 0 or sky_index >= len(SKY_LOOK):
            sky_index = 0

        breeze = "a warm southerly breeze blows" if int(getattr(weather_info, "change", 0)) >= 0 else "a cold northern gust blows"
        context.finish()
        return f"The sky is {SKY_LOOK[sky_index]} and {breeze}.\r\n"

    def do_where(self, character: Character, context: Context) -> str:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        my_room = self.room_registry.get_or_none(id=character.room_id)
        if my_room is None:
            context.finish()
            return "None\r\n"

        room_flags = CharacterMacros.get_enum("roomFlags")
        nowhere_bit = room_flags.ROOM_NOWHERE.value if room_flags and hasattr(room_flags, "ROOM_NOWHERE") else None

        if not arg:
            lines = ["Players near you:\r\n"]
            found = False
            for session in self.session_handler.get_playing_sessions():
                victim = session.character
                if victim is None or CharacterMacros.is_npc(victim):
                    continue
                if victim.id == character.id:
                    continue
                room = self.room_registry.get_or_none(id=victim.room_id)
                if room is None:
                    continue
                if room.area_id != my_room.area_id:
                    continue
                if nowhere_bit is not None and CharacterMacros.is_set(int(room.room_flags), nowhere_bit):
                    continue
                if not CharacterMacros.can_see(character, victim, self.room_helper):
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
            if not CharacterMacros.can_see(character, victim, self.room_helper):
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
                if not CharacterMacros.can_see(character, mob, self.room_helper):
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

        victim = PlayerUtil.get_target(character, arg, room, self.room_helper)
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

    def do_title(self, character: Character, context: Context) -> str:
        if CharacterMacros.is_npc(character):
            context.finish()
            return ""

        argument = (context.result if isinstance(context.result, str) else "").strip()
        if argument == "":
            context.finish()
            return "Change your title to what?\r\n"

        argument = argument.replace("~", "")[:45]
        if argument and argument[0] not in (".", ",", "!", "?"):
            character.title = f" {argument}"
        else:
            character.title = argument

        context.finish()
        return "Ok.\r\n"

    def do_description(self, character: Character, context: Context) -> str:
        argument = (context.result if isinstance(context.result, str) else "").strip()
        description = (getattr(character, "description", "") or "").replace("~", "")

        if argument:
            arg = argument.replace("~", "")
            if arg.startswith("-"):
                lines = [line for line in description.splitlines() if line.strip() != ""]
                if not lines:
                    context.finish()
                    return "No lines left to remove.\r\n"
                lines = lines[:-1]
                character.description = ("\r\n".join(lines) + ("\r\n" if lines else ""))
                if lines:
                    context.finish()
                    return "Your description is:\r\n" + character.description
                context.finish()
                return "Description cleared.\r\n"

            if arg.startswith("+"):
                append_text = arg[1:].lstrip()
                new_desc = description + append_text + "\r\n"
            else:
                new_desc = arg + "\r\n"

            if len(new_desc) >= 1024:
                context.finish()
                return "Description too long.\r\n"
            character.description = new_desc

        final_desc = getattr(character, "description", None)
        context.finish()
        if final_desc:
            return "Your description is:\r\n" + final_desc
        return "Your description is:\r\n(None).\r\n"

    def do_report(self, character: Character):
        room = self.room_registry.get_or_none(id=character.room_id)
        in_room = self.player_helper.players_in_room(character, room) if room is not None else []
        say_text = (
            f"I have {character.hit}/{character.max_hit} hp "
            f"{character.mana}/{character.max_mana} mana "
            f"{character.movement}/{character.max_movement} mv "
            f"{character.experience} xp."
        )
        return {
            "people": in_room,
            "to_char": f"You say '{say_text}'\r\n",
            "to_room": f"{character.name} says '{say_text}'\r\n",
        }

    def do_worth(self, character: Character, context: Context) -> str:
        if CharacterMacros.is_npc(character):
            context.finish()
            return f"You have {character.gold} gold and {character.silver} silver.\r\n"

        exp_to_level = GenericUtil.to_int(getattr(character, "accumulated_experience", 0), 0) - GenericUtil.to_int(character.experience, 0)
        if exp_to_level < 0:
            exp_to_level = 0
        context.finish()
        return (
            f"You have {character.gold} gold, {character.silver} silver, and "
            f"{character.experience} experience ({exp_to_level} exp to level).\r\n"
        )

    def do_affects(self, character: Character, context: Context) -> str:
        context.finish()
        return CharacterMacros.format_affects(character)

    def do_autolist(self, character: Character, context: Context) -> str:
        if CharacterMacros.is_npc(character):
            context.finish()
            return ""

        act_bits = self.PlayerActBits
        comm_bits = CharacterMacros.get_enum("commFlags")
        act = CharacterMacros.get_act_flags(character)
        comm = CharacterMacros.get_comm_flags(character)

        def on_off(value: bool) -> str:
            return "ON" if value else "OFF"

        def act_enabled(name: str) -> bool:
            if act_bits is None or not hasattr(act_bits, name):
                return False
            return CharacterMacros.is_set(act, getattr(act_bits, name).value)

        lines = [
            "   action     status\r\n",
            "---------------------\r\n",
            f"autoassist     {on_off(act_enabled('PLR_AUTOASSIST'))}\r\n",
            f"autoexit       {on_off(act_enabled('PLR_AUTOEXIT'))}\r\n",
            f"autogold       {on_off(act_enabled('PLR_AUTOGOLD'))}\r\n",
            f"autoloot       {on_off(act_enabled('PLR_AUTOLOOT'))}\r\n",
            f"autosac        {on_off(act_enabled('PLR_AUTOSAC'))}\r\n",
            f"autosplit      {on_off(act_enabled('PLR_AUTOSPLIT'))}\r\n",
        ]
        if comm_bits is not None:
            def comm_enabled(name: str) -> bool:
                if not hasattr(comm_bits, name):
                    return False
                return CharacterMacros.is_set(comm, getattr(comm_bits, name).value)
            lines.extend([
                f"compact mode   {on_off(comm_enabled('COMM_COMPACT'))}\r\n",
                f"prompt         {on_off(comm_enabled('COMM_PROMPT'))}\r\n",
                f"combine items  {on_off(comm_enabled('COMM_COMBINE'))}\r\n",
            ])
        if hasattr(act_bits, "PLR_CANLOOT"):
            if not CharacterMacros.is_set(act, getattr(act_bits, "PLR_CANLOOT").value):
                lines.append("Your corpse is safe from thieves.\r\n")
            else:
                lines.append("Your corpse may be looted.\r\n")
        if hasattr(act_bits, "PLR_NOSUMMON"):
            if CharacterMacros.is_set(act, getattr(act_bits, "PLR_NOSUMMON").value):
                lines.append("You cannot be summoned.\r\n")
            else:
                lines.append("You can be summoned.\r\n")
        if hasattr(act_bits, "PLR_NOFOLLOW"):
            if CharacterMacros.is_set(act, getattr(act_bits, "PLR_NOFOLLOW").value):
                lines.append("You do not welcome followers.\r\n")
            else:
                lines.append("You accept followers.\r\n")

        context.finish()
        return "".join(lines)

    def do_autoassist(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(character, "PLR_AUTOASSIST", "Autoassist removed.\r\n", "You will now assist when needed.\r\n")
        context.finish()
        return text

    def do_autoexit(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(character, "PLR_AUTOEXIT", "Exits will no longer be displayed.\r\n", "Exits will now be displayed.\r\n")
        context.finish()
        return text

    def do_autogold(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(character, "PLR_AUTOGOLD", "Autogold removed.\r\n", "Automatic gold looting set.\r\n")
        context.finish()
        return text

    def do_autoloot(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(character, "PLR_AUTOLOOT", "Autolooting removed.\r\n", "Automatic corpse looting set.\r\n")
        context.finish()
        return text

    def do_autosac(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(character, "PLR_AUTOSAC", "Autosacrificing removed.\r\n", "Automatic corpse sacrificing set.\r\n")
        context.finish()
        return text

    def do_autosplit(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(character, "PLR_AUTOSPLIT", "Autosplitting removed.\r\n", "Automatic gold splitting set.\r\n")
        context.finish()
        return text

    def do_brief(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_comm(character, "COMM_BRIEF", "Full descriptions activated.\r\n", "Short descriptions activated.\r\n")
        context.finish()
        return text

    def do_compact(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_comm(character, "COMM_COMPACT", "Compact mode removed.\r\n", "Compact mode set.\r\n")
        comm_bits = CharacterMacros.get_enum("commFlags")
        comm = CharacterMacros.get_comm_flags(character)
        is_compact = (
            comm_bits is not None
            and hasattr(comm_bits, "COMM_COMPACT")
            and CharacterMacros.is_set(comm, comm_bits.COMM_COMPACT.value)
        )
        character.carriage_return = not is_compact
        if getattr(character, "prompt_format", None) is not None:
            character.prompt_format.carriage_return = not is_compact
        context.finish()
        return text

    def do_combine(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_comm(character, "COMM_COMBINE", "Long inventory selected.\r\n", "Combined inventory selected.\r\n")
        context.finish()
        return text

    def do_noloot(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(
            character,
            "PLR_CANLOOT",
            "Your corpse is now safe from thieves.\r\n",
            "Your corpse may now be looted.\r\n",
        )
        context.finish()
        return text

    def do_nofollow(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(
            character,
            "PLR_NOFOLLOW",
            "You now accept followers.\r\n",
            "You no longer accept followers.\r\n",
        )
        context.finish()
        return text

    def do_nosummon(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_player_act(
            character,
            "PLR_NOSUMMON",
            "You are now summonable.\r\n",
            "You are no longer summonable.\r\n",
        )
        context.finish()
        return text

    def do_read(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip()
        if not arg and context.parameters:
            arg = " ".join(context.parameters).strip()
        if not arg:
            return {"look": True}
        return {"argument": arg}

    def do_examine(self, character: Character, context: Context) -> dict:
        arg = (context.result if isinstance(context.result, str) else "").strip()
        if not arg and context.parameters:
            arg = " ".join(context.parameters).strip()
        if not arg:
            context.finish()
            return {"error": "Examine what?\r\n"}

        room = self.room_registry.get_or_none(id=character.room_id)
        obj = ItemUtil.find_item(character, room, arg) if room is not None else None
        look_in = bool(obj is not None and (ItemUtil.is_container_like(obj) or ItemUtil.is_drink_container(obj)))
        return {"argument": arg, "look_in": look_in}

    def do_whois(self, character: Character, context: Context) -> str:
        arg = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not arg:
            context.finish()
            return self.do_who(character)

        matches = []
        for c in [character] + PlayerUtil.visible(character, self.session_handler):
            name = (c.name or "").lower()
            if name == arg or name.startswith(arg):
                matches.append(c)

        context.finish()
        if not matches:
            return "No one by that name is playing.\r\n"

        lines = [
            f"{CharacterMacros.who_line(character, c)}\r\n"
            for c in matches
        ]
        return "".join(lines)

    def do_count(self, context: Context) -> str:
        count = len(self.session_handler.get_playing_sessions())
        context.finish()
        if count == 1:
            return "There is 1 player online.\r\n"
        return f"There are {count} players online.\r\n"

    def do_show(self, character: Character, context: Context) -> str:
        text = CharacterMacros.toggle_comm(
            character,
            "COMM_SHOW_AFFECTS",
            "Affects will no longer be shown in score.\r\n",
            "Affects will now be shown in score.\r\n",
        )
        context.finish()
        return text

    def do_practice(self, character: Character, context: Context) -> str | dict:
        if CharacterMacros.is_npc(character):
            context.finish()
            return ""

        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()

        skills = list(getattr(character, "skills", []) or [])
        spells = list(getattr(character, "spells", []) or [])
        practice_entries = skills + spells
        attributes = getattr(character, "character_attributes", None)
        practices = GenericUtil.to_int(getattr(attributes, "practices", 0), 0) if attributes is not None else 0

        if not raw:
            lines = []
            known_skills = []
            for skill in practice_entries:
                name = str(skill.get("name", "") or "").strip()
                level = GenericUtil.to_int(skill.get("level", 0), 0)
                meta = self._practice_meta(name)
                if not name or level < 1 or not self._practice_visible(character, meta):
                    continue
                known_skills.append((name, level))

            for i, (name, level) in enumerate(known_skills):
                lines.append(f"{name:<18}   {level:>3}%  ")
                if (i + 1) % 3 == 0:
                    lines.append("\r\n")
            if len(known_skills) % 3 != 0:
                lines.append("\r\n")
            lines.append(f"You have {practices} practice sessions left.\r\n")
            context.finish()
            return "".join(lines)

        if not CharacterMacros.is_awake(character):
            context.finish()
            return "In your dreams, or what?\r\n"

        if practices <= 0:
            context.finish()
            return "You have no practice sessions left.\r\n"

        room = self.room_registry.get_or_none(id=character.room_id)
        act_bits = CharacterMacros.get_enum("actBits")
        trainer = None
        if room is not None:
            practice_bit = act_bits.ACT_PRACTICE.value if act_bits is not None and hasattr(act_bits, "ACT_PRACTICE") else 0
            for mob in room.mobiles.values():
                if SkillUtil.is_practice_trainer(mob, practice_bit):
                    trainer = mob
                    break

        if trainer is None:
            context.finish()
            return "You can't do that here.\r\n"

        practiced_skill = SkillUtil.find_character_skill(practice_entries, raw)
        practice_meta = self._practice_meta(raw if practiced_skill is None else practiced_skill.get("name", raw))
        learned = GenericUtil.to_int(practiced_skill.get("level", 0), 0) if practiced_skill is not None else 0

        if practiced_skill is None or learned < 1 or not self._practice_visible(character, practice_meta):
            context.finish()
            return "You can't practice that.\r\n"

        rating = self._practice_rating(character, practice_meta)
        if rating <= 0:
            context.finish()
            return "You can't practice that.\r\n"

        adept = SkillUtil.practice_adept(character)
        skill_name = str(practiced_skill.get("name", raw) or raw)

        if learned >= adept:
            context.finish()
            return f"You are already learned at {skill_name}.\r\n"

        attributes.practices = max(0, practices - 1)
        gain = SkillUtil.practice_gain(character, rating)
        new_level = learned + gain
        room = self.room_registry.get_or_none(id=character.room_id)
        targets = room.player_targets(character)

        if new_level < adept:
            practiced_skill["level"] = new_level
            context.finish()
            return {
                "to_char": f"You practice {skill_name}.\r\n",
                "to_room": f"{character.name} practices {skill_name}.\r\n",
                "targets": targets,
            }

        practiced_skill["level"] = adept
        context.finish()
        return {
            "to_char": f"You are now learned at {skill_name}.\r\n",
            "to_room": f"{character.name} is now learned at {skill_name}.\r\n",
            "targets": targets,
        }

    def _practice_meta(self, skill_name: str):
        wanted = str(skill_name or "").strip().lower()
        if not wanted:
            return None

        if self.skill_registry is not None:
            for skill in self.skill_registry.all_skills():
                if str(getattr(skill, "name", "") or "").strip().lower() == wanted:
                    return skill

        if self.spell_registry is not None:
            for spell in self.spell_registry.all_spells():
                if str(getattr(spell, "name", "") or "").strip().lower() == wanted:
                    return spell

        return None

    @staticmethod
    def _practice_class_name(character: Character) -> str:
        return str(getattr(getattr(character, "character_class", None), "name", "") or "").strip().lower()

    def _practice_visible(self, character: Character, meta) -> bool:
        if meta is None:
            return True
        required_level = self._practice_level_requirement(character, meta)
        return GenericUtil.to_int(getattr(character, "level", 0), 0) >= required_level

    def _practice_level_requirement(self, character: Character, meta) -> int:
        class_name = self._practice_class_name(character)
        level_map = getattr(meta, "level_by_class", {}) or {}
        if class_name in level_map:
            return max(0, GenericUtil.to_int(level_map.get(class_name), 99))
        return max(0, GenericUtil.to_int(level_map.get("mage", 99), 99))

    def _practice_rating(self, character: Character, meta) -> int:
        if meta is None:
            return 1
        class_name = self._practice_class_name(character)
        rating_map = getattr(meta, "rating_by_class", {}) or {}
        if class_name in rating_map:
            return max(0, GenericUtil.to_int(rating_map.get(class_name), 0))
        return max(0, GenericUtil.to_int(rating_map.get("mage", 0), 0))

    def do_prompt(self, character: Character, context: Context) -> str:
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()

        if raw == "":
            text = CharacterMacros.toggle_comm(character, "COMM_PROMPT", "You will no longer see prompts.\r\n", "You will now see prompts.\r\n")
            context.finish()
            return text

        if getattr(character, "prompt_format", None) is None:
            context.finish()
            return "Prompt settings are unavailable.\r\n"

        if raw.lower() == "all":
            for attr, value in vars(character.prompt_format).items():
                if isinstance(value, bool) and attr == "health" or attr == "mana" or attr == "movement":
                    setattr(character.prompt_format, attr, True)
                else:
                    setattr(character.prompt_format, attr, False)
            context.finish()
            return "Prompt set to <%hhp %mm %vmv> \r\n"

        template = raw.replace("~", "")[:50]
        tokens = set()
        for i in range(len(template) - 1):
            if template[i] == "%":
                tokens.add("%" + template[i + 1])

        character.prompt_format.health = "%h" in tokens
        character.prompt_format.max_health = "%H" in tokens
        character.prompt_format.mana = "%m" in tokens
        character.prompt_format.max_mana = "%M" in tokens
        character.prompt_format.movement = "%v" in tokens
        character.prompt_format.max_movement = "%V" in tokens
        character.prompt_format.experience = "%x" in tokens
        character.prompt_format.accumulated_experience = "%X" in tokens
        character.prompt_format.gold = "%g" in tokens
        character.prompt_format.silver = "%s" in tokens
        character.prompt_format.alignment = "%a" in tokens
        character.prompt_format.room_name = "%r" in tokens
        character.prompt_format.exits = "%e" in tokens
        character.prompt_format.room_vnum = "%R" in tokens
        character.prompt_format.area_name = "%z" in tokens
        character.prompt_format.carriage_return = "%c" in tokens

        shown = template if "%c" in template else (template + " ")
        context.finish()
        return f"Prompt set to {shown}\r\n"

    def do_equipment(self, character: Character, context: Context) -> str:
        lines = CharacterMacros.target_equipment_lines(character, EQUIP_SLOT_LABELS)
        context.finish()
        if not lines:
            return "You are using:\r\nNothing.\r\n"
        return "You are using:\r\n" + "\r\n".join(lines) + "\r\n"

    def do_compare(self, character: Character, context: Context) -> str:
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if raw:
            arg1, rest = InterpUtil.one_argument(raw)
            arg2, _ = InterpUtil.one_argument(rest)
        else:
            arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
            arg2 = (context.parameters[1] if context.parameters and len(context.parameters) > 1 else "").strip().lower()
        if not arg1:
            context.finish()
            return "Compare what to what?\r\n"

        obj1 = CharacterMacros.find_owned_item(character, arg1)
        if obj1 is None:
            context.finish()
            return "You do not have that item.\r\n"

        obj2 = CharacterMacros.find_owned_item(character, arg2) if arg2 else CharacterMacros.find_comparable_equipped_item(character, obj1)
        if obj2 is None:
            context.finish()
            return "You aren't wearing anything comparable.\r\n" if not arg2 else "You do not have that item.\r\n"

        t1 = str(getattr(obj1, "item_type", "") or "").strip().lower()
        t2 = str(getattr(obj2, "item_type", "") or "").strip().lower()
        if t1 != t2:
            context.finish()
            return "You can't compare those items.\r\n"

        v1 = CharacterMacros.compare_value(obj1)
        v2 = CharacterMacros.compare_value(obj2)
        if v1 is None or v2 is None:
            context.finish()
            return "You can't compare those items.\r\n"

        item_flags = CharacterMacros.get_enum("itemFlags")
        n1 = ItemUtil.format_obj_to_char(obj1, item_flags_enum=item_flags, f_short=True)
        n2 = ItemUtil.format_obj_to_char(obj2, item_flags_enum=item_flags, f_short=True)

        context.finish()
        if v1 == v2:
            return f"{n1} looks about the same as {n2}.\r\n"
        if v1 > v2:
            return f"{n1} looks better than {n2}.\r\n"
        return f"{n1} looks worse than {n2}.\r\n"
