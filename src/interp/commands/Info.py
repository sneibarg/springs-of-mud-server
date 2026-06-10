from datetime import datetime
from typing import Any
from injector import inject

from game.EnumProvider import EnumProvider
from game.RegistryService import RegistryService
from api.ItemApi import ItemApi
from util.EffectUtil import EffectUtil
from util.GenericUtil import GenericUtil
from game.WeatherHandler import WeatherHandler
from api.InterpApi import InterpApi
from util.InfoUtil import InfoUtil
from interp.Context import Context
from interp.HelpEntry import HelpEntry
from item.Item import Item
from util.InterpUtil import InterpUtil
from util.ItemUtil import ItemUtil
from util.MobileUtil import MobileUtil
from player.Character import Character
from api.CharacterApi import CharacterApi
from skill.Ability import Ability
from util.PlayerUtil import PlayerUtil
from server.LoggerFactory import LoggerFactory
from server.session.SessionHandler import SessionHandler

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


class Info:
    @inject
    def __init__(self,
                 registry_service: RegistryService,
                 session_handler: SessionHandler,
                 weather_handler: WeatherHandler,
                 enum_provider: EnumProvider,
                 interp_api: InterpApi):
        self.__name__ = "Info"
        self.logger = LoggerFactory.get_logger(self.__name__)
        self.interp_registry = registry_service.interp_registry
        self.room_registry = registry_service.room_registry
        self.session_handler = session_handler
        self.weather_handler = weather_handler
        self.interp_api = interp_api
        self.server_boot_time = datetime.now().ctime()
        self.PlayerActBits = enum_provider.get("playerActBits")

    def do_quit(self, context: Context):
        return self.interp_api.run_action(context, context.command.name)

    def do_who(self, character: Character) -> str:
        who_list = [character] + PlayerUtil.visible(character, self.session_handler)
        lines = [
            f"{InfoUtil.who_line(character, c)}\r\n"
            for c in who_list
        ]
        lines.append(f"Players found: {len(who_list)}\r\n")
        return "".join(lines)

    def do_help(self, argument: str = "") -> str:
        arg_all = " ".join((argument or "").split()).lower()
        if not arg_all:
            arg_all = "summary"
        q_words = [InterpUtil.normalize_help_token(w) for w in arg_all.split()]
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

            k_words = [InterpUtil.normalize_help_token(w) for w in str(help_entry.keyword).split()]
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
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        if room is None:
            return None

        arg1 = (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip().lower()
        if arg1 in ("", "auto", "i", "in", "on"):
            return None

        target = PlayerUtil.get_target(character, arg1, room)
        if target is None:
            context.jump_to(4)
            return None

        desc = (getattr(target, "description", "") or "").strip()
        if not desc:
            desc = "You see nothing special."

        lines = [desc, InfoUtil.target_condition_line(target)]
        equip_lines = InfoUtil.target_equipment_lines(target, EQUIP_SLOT_LABELS)
        if equip_lines:
            lines.append("")
            lines.append(f"{(target.name or 'They')} is using:")
            lines.extend(equip_lines)

        context.finish()
        return "\r\n".join(lines) + "\r\n"

    async def do_look(self, character: Character, context: Context) -> dict[str, Any] | None:
        room = context.room if context.room is not None else self.room_registry.get(id=character.room_id)
        if room is None:
            context.finish()
            return None

        payload = self.interp_api.evaluate_guards_only(context, context.command.name)
        if payload is not None:
            return payload

        look_mode = str(getattr(context, "look_mode", "room") or "room")
        if look_mode == "room":
            await context.room_handler().print_room(character.id, room)
            if CharacterApi.is_set(character.status_flags.act, self.PlayerActBits.PLR_AUTOEXIT.value):
                await context.room_handler().print_exits(character, room)
            context.jump_to(1)  # players + mobiles
            return None

        if look_mode == "in":
            context.jump_to(2)
            return None

        if look_mode == "target":
            context.jump_to(3)
            return None

        if look_mode == "item_or_extra":
            context.jump_to(4)
            return None

        if look_mode == "direction":
            context.jump_to(5)
            return None

        context.finish()
        return None

    def do_scroll(self, character: Character, context: Context) -> str:
        raw_arg = context.result if isinstance(context.result, str) else ""
        arg = raw_arg.strip() if raw_arg else (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip()
        if character.context is None:
            character.context = {}

        current_lines = GenericUtil.to_int(character.context.get("scroll_lines", 0), 0)
        context.scroll_argument = arg
        context.scroll_lines = GenericUtil.to_int(arg, 0)
        context.scroll_is_numeric = bool(arg) and arg.lstrip("-").isdigit()

        if arg == "":
            display_lines = current_lines + 2 if current_lines > 0 else 0
            context.finish()
            return self._render_message_key(context, "default", channel="to_char", n=display_lines).get("to_char", "")

        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

        lines = context.scroll_lines
        if lines == 0:
            character.context["scroll_lines"] = 0
            return self._render_message_key(context, "disable", channel="to_char").get("to_char", "")

        character.context["scroll_lines"] = lines - 2
        return self._render_message_key(context, "set", channel="to_char", n=lines).get("to_char", "")

    def do_wimpy(self, character: Character, context: Context) -> str:
        if CharacterApi.is_npc(character):
            context.finish()
            return ""

        attributes = getattr(character, "character_attributes", None)
        if attributes is None:
            context.finish()
            return ""

        raw_arg = context.result if isinstance(context.result, str) else ""
        arg = raw_arg.strip() if raw_arg else (context.parameters[0] if context.parameters and len(context.parameters) > 0 else "").strip()
        context.wimpy_argument = arg
        context.wimpy_is_numeric = bool(arg) and arg.lstrip("-").isdigit()

        if arg == "":
            wimpy = int(getattr(character, "max_hit", 0) / 5)
        else:
            wimpy = GenericUtil.to_int(arg, 0)
            context.wimpy_value = wimpy
            payload = self.interp_api.run_action(context, context.command.name)
            if payload.get("blocked"):
                return payload.get("to_char", "")

        attributes.wimpy = wimpy
        context.finish()
        return self._render_message_key(context, "set", channel="to_char", d=wimpy).get("to_char", "")

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

        trust = CharacterApi.get_trust(character)
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
            f"You are {character.name} {character.title}, level {character.level}, {age_years} years old ({total_hours} hours).",
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

        position_line = InfoUtil.score_position_line(attributes)
        lines.append(position_line)

        ac_pierce = character.armor_class.get_ac(character, 0)
        ac_bash = character.armor_class.get_ac(character, 1)
        ac_slash = character.armor_class.get_ac(character, 2)
        ac_magic = character.armor_class.get_ac(character, 3)

        if character.level >= 25:
            lines.append(f"Armor: pierce: {ac_pierce}  bash: {ac_bash}  slash: {ac_slash}  magic: {ac_magic}")

        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_pierce, 'piercing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_bash, 'bashing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_slash, 'slashing')}.")
        lines.append(f"You are {InfoUtil.score_ac_phrase(ac_magic, 'magic')}.")

        if CharacterApi.is_immortal(character):
            holy = "on" if CharacterApi.has_holy_light(character) else "off"
            imm_text = f"Holy Light: {holy}"
            if GenericUtil.to_int(getattr(character.status_flags, "invis_level", 0), 0) > 0:
                imm_text += f"  Invisible: level {character.status_flags.invis_level}"
            if GenericUtil.to_int(getattr(character.status_flags, "incog_level", 0), 0) > 0:
                imm_text += f"  Incognito: level {character.status_flags.incog_level}"
            lines.append(imm_text)

        if character.level >= 15:
            lines.append(f"Hitroll: {CharacterApi.get_hitroll(character)}  Damroll: {CharacterApi.get_damroll(character)}.")

        alignment = GenericUtil.to_int(getattr(attributes, "alignment", 0), 0)
        if character.level >= 10:
            lines.append(f"Alignment: {alignment}. You are {InfoUtil.score_alignment_word(alignment)}.")
        else:
            lines.append(f"You are {InfoUtil.score_alignment_word(alignment)}.")
        if CharacterApi.is_comm_enabled(character, "COMM_SHOW_AFFECTS"):
            lines.append(EffectUtil.format_affects(character).rstrip("\r\n"))
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
        context.weather_outside = CharacterApi.is_outside(character)
        weather_info = self.weather_handler.weather_info
        context.weather_available = weather_info is not None
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

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

        room_flags = CharacterApi.get_enum("roomFlags")
        nowhere_bit = room_flags.ROOM_NOWHERE.value if room_flags and hasattr(room_flags, "ROOM_NOWHERE") else None

        if not arg:
            lines = ["Players near you:\r\n"]
            found = False
            for session in self.session_handler.get_playing_sessions():
                victim = session.character
                if victim is None or CharacterApi.is_npc(victim):
                    continue
                if victim.id == character.id:
                    continue
                room = self.room_registry.get_or_none(id=victim.room_id)
                if room is None:
                    continue
                if room.area_id != my_room.area_id:
                    continue
                if nowhere_bit is not None and CharacterApi.is_set(int(room.room_flags), nowhere_bit):
                    continue
                if not CharacterApi.can_see(character, victim):
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
            if not CharacterApi.can_see(character, victim):
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
                if not CharacterApi.can_see(character, mob):
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
        room = self.room_registry.get_or_none(id=character.room_id)
        victim = PlayerUtil.get_target(character, arg, room) if room is not None else None
        context.consider_argument = arg
        context.consider_victim = victim
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

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
        if CharacterApi.is_npc(character):
            context.finish()
            return ""

        argument = (context.result if isinstance(context.result, str) else "").strip()
        context.title_argument = argument
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

        argument = argument.replace("~", "")[:45]
        if argument and argument[0] not in (".", ",", "!", "?"):
            character.title = f" {argument}"
        else:
            character.title = argument

        return self._render_message_key(context, "default", channel="to_char").get("to_char", "")

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
        in_room = room.player_targets(character) if room is not None else []
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
        if CharacterApi.is_npc(character):
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
        return EffectUtil.format_affects(character)

    def do_autolist(self, character: Character, context: Context) -> str:
        if CharacterApi.is_npc(character):
            context.finish()
            return ""

        act_bits = self.PlayerActBits
        comm_bits = CharacterApi.get_enum("commFlags")
        act = character.status_flags.act
        comm = character.status_flags.comm

        def on_off(value: bool) -> str:
            return "ON" if value else "OFF"

        def act_enabled(name: str) -> bool:
            if act_bits is None or not hasattr(act_bits, name):
                return False
            return CharacterApi.is_set(act, getattr(act_bits, name).value)

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
                return CharacterApi.is_set(comm, getattr(comm_bits, name).value)
            lines.extend([
                f"compact mode   {on_off(comm_enabled('COMM_COMPACT'))}\r\n",
                f"prompt         {on_off(comm_enabled('COMM_PROMPT'))}\r\n",
                f"combine items  {on_off(comm_enabled('COMM_COMBINE'))}\r\n",
            ])
        if hasattr(act_bits, "PLR_CANLOOT"):
            if not CharacterApi.is_set(act, getattr(act_bits, "PLR_CANLOOT").value):
                lines.append("Your corpse is safe from thieves.\r\n")
            else:
                lines.append("Your corpse may be looted.\r\n")
        if hasattr(act_bits, "PLR_NOSUMMON"):
            if CharacterApi.is_set(act, getattr(act_bits, "PLR_NOSUMMON").value):
                lines.append("You cannot be summoned.\r\n")
            else:
                lines.append("You can be summoned.\r\n")
        if hasattr(act_bits, "PLR_NOFOLLOW"):
            if CharacterApi.is_set(act, getattr(act_bits, "PLR_NOFOLLOW").value):
                lines.append("You do not welcome followers.\r\n")
            else:
                lines.append("You accept followers.\r\n")

        context.finish()
        return "".join(lines)

    def do_autoassist(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(character, "PLR_AUTOASSIST", "Autoassist removed.\r\n", "You will now assist when needed.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_AUTOASSIST") else "disable", channel="to_char").get("to_char", "")

    def do_autoexit(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(character, "PLR_AUTOEXIT", "Exits will no longer be displayed.\r\n", "Exits will now be displayed.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_AUTOEXIT") else "disable", channel="to_char").get("to_char", "")

    def do_autogold(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(character, "PLR_AUTOGOLD", "Autogold removed.\r\n", "Automatic gold looting set.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_AUTOGOLD") else "disable", channel="to_char").get("to_char", "")

    def do_autoloot(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(character, "PLR_AUTOLOOT", "Autolooting removed.\r\n", "Automatic corpse looting set.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_AUTOLOOT") else "disable", channel="to_char").get("to_char", "")

    def do_autosac(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(character, "PLR_AUTOSAC", "Autosacrificing removed.\r\n", "Automatic corpse sacrificing set.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_AUTOSAC") else "disable", channel="to_char").get("to_char", "")

    def do_autosplit(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(character, "PLR_AUTOSPLIT", "Autosplitting removed.\r\n", "Automatic gold splitting set.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_AUTOSPLIT") else "disable", channel="to_char").get("to_char", "")

    def do_brief(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_comm(character, "COMM_BRIEF", "Full descriptions activated.\r\n", "Short descriptions activated.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._comm_enabled(character, "COMM_BRIEF") else "disable", channel="to_char").get("to_char", "")

    def do_compact(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_comm(character, "COMM_COMPACT", "Compact mode removed.\r\n", "Compact mode set.\r\n")
        comm_bits = CharacterApi.get_enum("commFlags")
        comm = character.status_flags.comm
        is_compact = (
                comm_bits is not None
                and hasattr(comm_bits, "COMM_COMPACT")
                and CharacterApi.is_set(comm, comm_bits.COMM_COMPACT.value)
        )
        character.carriage_return = not is_compact
        if getattr(character, "prompt_format", None) is not None:
            character.prompt_format.carriage_return = not is_compact
        context.finish()
        return self._render_message_key(context, "enable" if is_compact else "disable", channel="to_char").get("to_char", "")

    def do_combine(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_comm(character, "COMM_COMBINE", "Long inventory selected.\r\n", "Combined inventory selected.\r\n")
        context.finish()
        return self._render_message_key(context, "enable" if self._comm_enabled(character, "COMM_COMBINE") else "disable", channel="to_char").get("to_char", "")

    def do_noloot(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(
            character,
            "PLR_CANLOOT",
            "Your corpse is now safe from thieves.\r\n",
            "Your corpse may now be looted.\r\n",
        )
        context.finish()
        return self._render_message_key(context, "disable" if self._player_act_enabled(character, "PLR_CANLOOT") else "enable", channel="to_char").get("to_char", "")

    def do_nofollow(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(
            character,
            "PLR_NOFOLLOW",
            "You now accept followers.\r\n",
            "You no longer accept followers.\r\n",
        )
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_NOFOLLOW") else "disable", channel="to_char").get("to_char", "")

    def do_nosummon(self, character: Character, context: Context) -> str:
        CharacterApi.toggle_player_act(
            character,
            "PLR_NOSUMMON",
            "You are now summonable.\r\n",
            "You are no longer summonable.\r\n",
        )
        context.finish()
        return self._render_message_key(context, "enable" if self._player_act_enabled(character, "PLR_NOSUMMON") else "disable", channel="to_char").get("to_char", "")

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
        context.examine_argument = arg
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return {"error": payload.get("to_char", "")}
        context.done = False

        room = self.room_registry.get_or_none(id=character.room_id)
        obj = (character.find_inventory_item(arg) if arg else None) or (None if room is None else room.find_room_item(arg))
        look_in = bool(obj is not None and (Item.is_container_like(obj) or Item.is_drink_container(obj)))
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

        context.whois_matches = matches
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

        lines = [
            f"{InfoUtil.who_line(character, c)}\r\n"
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
        CharacterApi.toggle_comm(
            character,
            "COMM_SHOW_AFFECTS",
            "Affects will no longer be shown in score.\r\n",
            "Affects will now be shown in score.\r\n",
        )
        context.finish()
        return self._render_message_key(context, "enable" if self._comm_enabled(character, "COMM_SHOW_AFFECTS") else "disable", channel="to_char").get("to_char", "")

    def do_practice(self, character: Character, context: Context) -> str | dict:
        if CharacterApi.is_npc(character):
            context.finish()
            return ""

        raw = (context.result if isinstance(context.result, str) else "").strip().lower()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip().lower()

        attributes = getattr(character, "character_attributes", None)
        practices = GenericUtil.to_int(getattr(attributes, "practices", 0), 0) if attributes is not None else 0

        if not raw:
            lines = []
            known_skills = []
            for skill in Character.visible_learned_entries(character, Ability.practice_visible):
                name = Character.learned_entry_name(skill)
                level = Character.learned_entry_level(skill)
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

        context.practice_argument = raw
        context.practice_is_awake = CharacterApi.is_awake(character)
        context.practice_sessions = practices

        room = self.room_registry.get_or_none(id=character.room_id)
        act_bits = CharacterApi.get_enum("actBits")
        trainer = None
        if room is not None:
            practice_bit = act_bits.ACT_PRACTICE.value if act_bits is not None and hasattr(act_bits, "ACT_PRACTICE") else 0
            for mob in room.mobiles.values():
                if MobileUtil.is_practice_trainer(mob, practice_bit):
                    trainer = mob
                    break

        context.practice_trainer = trainer

        practiced_skill = Character.get_learned(character, raw, prefix=True, visible_only=True, visible_fn=Ability.practice_visible)
        practice_name = Character.learned_entry_name(practiced_skill) or raw
        practice_meta = Ability.practice_meta(practice_name)
        learned = Character.learned_entry_level(practiced_skill)
        context.practice_skill = practiced_skill
        context.practice_skill_name = practice_name
        context.practice_learned = learned
        context.practice_visible = practiced_skill is not None

        rating = Ability.practice_rating(character, practice_meta)
        context.practice_rating = rating

        adept = Ability.practice_adept(character)
        context.practice_adept = adept
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

        attributes.practices = max(0, practices - 1)
        gain = Ability.practice_gain(character, rating)
        new_level = learned + gain
        room = self.room_registry.get_or_none(id=character.room_id)
        targets = room.player_targets(character)
        skill_name = context.practice_skill_name

        if new_level < adept:
            Character.set_learned(character, skill_name, new_level)
            context.finish()
            return {
                **self._render_message_key(context, "practice", s=skill_name),
                "to_room": self._render_message_key(context, "default", channel="to_room", s=skill_name).get("to_room", ""),
                "targets": targets,
            }

        practiced_skill["level"] = adept
        context.finish()
        return {
            **self._render_message_key(context, "now_adept", s=skill_name),
            "to_room": self._render_message_key(context, "learned", channel="to_room", s=skill_name).get("to_room", ""),
            "targets": targets,
        }

    def do_prompt(self, character: Character, context: Context) -> str:
        raw = (context.result if isinstance(context.result, str) else "").strip()
        if not raw and context.parameters:
            raw = " ".join(context.parameters).strip()

        if raw == "":
            CharacterApi.toggle_comm(character, "COMM_PROMPT", "You will no longer see prompts.\r\n", "You will now see prompts.\r\n")
            context.finish()
            return self._render_message_key(context, "enable" if self._comm_enabled(character, "COMM_PROMPT") else "disable", channel="to_char").get("to_char", "")

        context.prompt_argument = raw
        context.prompt_format_available = getattr(character, "prompt_format", None) is not None
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

        if raw.lower() == "all":
            for attr, value in vars(character.prompt_format).items():
                if isinstance(value, bool) and attr == "health" or attr == "mana" or attr == "movement":
                    setattr(character.prompt_format, attr, True)
                else:
                    setattr(character.prompt_format, attr, False)
            context.finish()
            return self._render_message_key(context, "set", channel="to_char", s="<%hhp %mm %vmv> ").get("to_char", "")

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
        return self._render_message_key(context, "set", channel="to_char", s=shown).get("to_char", "")

    def do_equipment(self, character: Character, context: Context) -> str:
        lines = InfoUtil.target_equipment_lines(character, EQUIP_SLOT_LABELS)
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
        obj1 = character.find_owned_item(arg1) if arg1 else None
        obj2 = character.find_owned_item(arg2) if arg2 else (ItemApi.find_comparable_equipped_item(character, obj1) if obj1 is not None else None)
        t1 = str(getattr(obj1, "item_type", "") or "").strip().lower() if obj1 is not None else ""
        t2 = str(getattr(obj2, "item_type", "") or "").strip().lower() if obj2 is not None else ""
        v1 = ItemApi.compare_value(obj1) if obj1 is not None else None
        v2 = ItemApi.compare_value(obj2) if obj2 is not None else None
        context.compare_arg1 = arg1
        context.compare_arg2 = arg2
        context.compare_obj1 = obj1
        context.compare_obj2 = obj2
        context.compare_same_type = bool(obj1 is not None and obj2 is not None and t1 == t2)
        context.compare_values_available = v1 is not None and v2 is not None
        payload = self.interp_api.run_action(context, context.command.name)
        if payload.get("blocked"):
            return payload.get("to_char", "")

        item_flags = CharacterApi.get_enum("itemFlags")
        n1 = ItemUtil.format_obj_to_char(obj1, item_flags_enum=item_flags, f_short=True)
        n2 = ItemUtil.format_obj_to_char(obj2, item_flags_enum=item_flags, f_short=True)

        context.finish()
        if v1 == v2:
            return f"{n1} looks about the same as {n2}.\r\n"
        if v1 > v2:
            return f"{n1} looks better than {n2}.\r\n"
        return f"{n1} looks worse than {n2}.\r\n"

    def _render_message_key(self, context: Context, message_key: str, channel: str = "", **tokens) -> dict:
        return self.interp_api.render_message_key(context, message_key, channel=channel, **tokens)

    @staticmethod
    def _player_act_enabled(character: Character, bit_name: str) -> bool:
        player_act_bits = CharacterApi.get_enum("playerActBits")
        if player_act_bits is None or not hasattr(player_act_bits, bit_name):
            return False
        return CharacterApi.is_set(character.status_flags.act, getattr(player_act_bits, bit_name).value)

    @staticmethod
    def _comm_enabled(character: Character, bit_name: str) -> bool:
        comm_bits = CharacterApi.get_enum("commFlags")
        if comm_bits is None or not hasattr(comm_bits, bit_name):
            return False
        return CharacterApi.is_set(character.status_flags.comm, getattr(comm_bits, bit_name).value)
