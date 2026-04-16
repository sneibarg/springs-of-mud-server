from interp.HelpEntry import HelpEntry
from interp.InterpRegistry import InterpRegistry
from server.LoggerFactory import LoggerFactory


class InfoCommands:
    def __init__(self, interp_registry: InterpRegistry):
        self.__name__ = "InfoCommands"
        self.interp_registry = interp_registry
        self.logger = LoggerFactory.get_logger(self.__name__)

    async def help_usage(self, character, argument: str = ""):
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

        message_text = "".join(output_parts) if len(output_parts) > 0 else "No help on that word.\n\r"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(message_text))