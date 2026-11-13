"""Execution mechanics shared by direct, forced, ordered, and remote commands."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any, TYPE_CHECKING

from interp.Command import Command
from interp.CommandAccess import CommandDenial
from interp.Context import Context
from server.LoggerFactory import LoggerFactory

if TYPE_CHECKING:
    from server.messaging.MessageBus import MessageBus


AuthorizationPolicy = Callable[[Any, Command], CommandDenial | None]
_SCRIPT_FILENAME = "<command script>"


class CommandScriptError(Exception):
    """An authored command step failed without an exception escaping a runtime helper."""


def _raised_in_script(error: Exception) -> bool:
    traceback = error.__traceback__
    while traceback.tb_next is not None:
        traceback = traceback.tb_next
    return traceback.tb_frame.f_code.co_filename == _SCRIPT_FILENAME


class CommandExecutor:
    """Run context-based command lambdas under an explicitly supplied access policy.

    Pipelines honor completion and jumps. Legacy sequences execute every entry,
    even when a lambda sets a pipeline control flag.
    """

    @staticmethod
    async def execute(command: Command, context: Context, *,
                      authorization: AuthorizationPolicy, message_bus: MessageBus, audit=None) -> Any:
        denial = authorization(context.character, command)
        if audit is not None and (denial is None or denial.message_key != 'command_frozen'):
            raw = context.raw_command if context.raw_command is not None else f'{command.name} {context.argument}'.rstrip()
            await audit.record(context.character, command, raw)
        if denial is not None:
            context.finish()
            await message_bus.send_to_character(context.character.id,
                                                message_bus.text_to_message(denial.render(command)))
            return None

        lambdas = command.lambdas or []
        if not any(isinstance(value, str) and value.strip() for value in lambdas):
            context.finish()
            await message_bus.send_to_character(context.character.id, message_bus.text_to_message("Huh?\r\n"))
            return None

        steps = {}
        for index, source in enumerate(lambdas):
            if not isinstance(source, str) or not source.strip():
                continue
            try:
                steps[index] = compile(source.strip(), _SCRIPT_FILENAME, "eval")
            except SyntaxError as error:
                raise CommandScriptError(f"Invalid syntax in command {command.name!r} at step {index + 1}") from error

        index = 0
        while index < len(lambdas):
            code = steps.get(index)
            if code is None:
                index += 1
                continue
            try:
                func = eval(code)
                if not callable(func):
                    index += 1
                    continue
                result = func(context)
                context.result = await result if inspect.isawaitable(result) else result
            except CommandScriptError:
                raise
            except Exception as error:
                if _raised_in_script(error):
                    raise CommandScriptError(f"Command {command.name!r} failed at step {index + 1}") from error
                LoggerFactory.get_logger(__name__).exception(
                    "Command %s lambda failed at index %s: %s", command.name, index, lambdas[index])
                raise

            if command.pipeline:
                if context.done:
                    break
                if isinstance(context.next_index, int) and context.next_index >= 0:
                    index = context.next_index
                    context.next_index = None
                    continue
            index += 1
        return context.result
