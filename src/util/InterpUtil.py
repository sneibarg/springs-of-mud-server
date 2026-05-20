from typing import Optional, Union, Any, List
from interp.Command import Command
from interp.InterpView import InterpView
from server.LoggerFactory import LoggerFactory

logger = LoggerFactory.get_logger("InterpUtil")


class InterpUtil:
    pass

    @staticmethod
    def find_nth_by_keyword(dictionary: dict, argument: str, default=None):
        n, keyword = InterpUtil.number_argument(argument)
        for item in dictionary.values():
            if keyword.lower() in str(getattr(item, 'name', '')).lower():
                n -= 1
                if n == 0:
                    return item
        return default

    @staticmethod
    def build_arguments(cmd: Command, arguments: str) -> List[str]:
        argument_list: List[str] = []
        remaining = arguments.strip()
        while len(argument_list) < cmd.max_arguments and remaining:
            argument, remaining = InterpUtil.one_argument(remaining)
            if not argument:
                argument_list.append("")
                break
            argument_list.append(argument)
        return argument_list

    @staticmethod
    def one_argument(argument: str) -> tuple[str, str]:
        """Split off the first word from argument, return (first_word, remainder)."""
        if not argument:
            return "", ""

        argument = argument.lstrip()

        if not argument:
            return "", ""

        if argument[0] in ("'", '"'):
            quote = argument[0]
            argument = argument[1:]
            end = argument.find(quote)
            if end == -1:
                word = argument
                rest = ""
            else:
                word = argument[:end]
                rest = argument[end + 1:].lstrip()
        else:
            parts = argument.split(maxsplit=1)
            word = parts[0]
            rest = parts[1] if len(parts) > 1 else ""

        return word.lower(), rest

    @staticmethod
    def number_argument(argument: str) -> tuple[int, str]:
        """Parse 'number.word' format.
        Returns (number, word). If no dot, returns (1, argument).
        """
        if not argument:
            return 1, ""

        if '.' not in argument:
            return 1, argument.strip()

        num_str, word = argument.split('.', 1)
        try:
            number = int(num_str)
        except ValueError:
            number = 1

        return number, word.strip()

    @staticmethod
    def shortcut_tokens(shortcuts) -> list[str]:
        if shortcuts is None:
            return []
        if isinstance(shortcuts, list):
            values = shortcuts
        else:
            values = str(shortcuts).split(",")

        tokens = []
        for value in values:
            token = str(value).strip().lower()
            if token:
                tokens.append(token)
        return tokens

    @staticmethod
    def find_command_by_name(name: str, commands: List[Command]) -> Optional[Command]:
        for command in commands:
            shortcuts = InterpUtil.shortcut_tokens(command.shortcuts)
            if name in shortcuts:
                return command
            if command.name == name:
                return command
        return None

    @staticmethod
    def extract_parameters(interp_registry, command: str) -> Union[tuple[Any, str], tuple[None, None]]:
        normalized = " ".join((command or "").split()).strip()
        if not normalized:
            return None, None

        parts = normalized.split(" ", 1)
        command_text = parts[0].lower()
        parameters = parts[1].strip() if len(parts) > 1 else ""
        get_or_none = getattr(interp_registry, "get_or_none", None)
        if callable(get_or_none):
            exact = get_or_none(name=command_text)
            if exact is not None:
                return exact, parameters

        for cmd in interp_registry.all_commands():
            if not cmd.name:
                continue

            shortcuts = InterpUtil.shortcut_tokens(cmd.shortcuts)
            if command_text == cmd.name or command_text in shortcuts:
                return cmd, parameters
        return None, None

    @staticmethod
    def argument_text(view: InterpView) -> str:
        context = view.context
        result = getattr(context, "result", "")
        text = (result if isinstance(result, str) else "").strip()
        if text:
            return text
        return " ".join(getattr(context, "parameters", []) or []).strip()
