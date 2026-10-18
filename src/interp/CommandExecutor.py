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


class CommandExecutor:
    """Run context-based command lambdas under an explicitly supplied access policy.

    Pipelines honor completion and jumps. Legacy sequences execute every entry,
    even when a lambda sets a pipeline control flag.
    """

    @staticmethod
    async def execute(command: Command, context: Context, *,
                      authorization: AuthorizationPolicy, message_bus: MessageBus) -> Any:
        denial = authorization(context.character, command)
        if denial is not None:
            context.finish()
            await message_bus.send_to_character(context.character.id,
                                                message_bus.text_to_message(denial.render(command)))
            return None

        lambdas = getattr(command, "lambdas", None) or []
        if not any(isinstance(value, str) and value.strip() for value in lambdas):
            context.finish()
            await message_bus.send_to_character(context.character.id, message_bus.text_to_message("Huh?\r\n"))
            return None

        index = 0
        while index < len(lambdas):
            source = lambdas[index]
            if not isinstance(source, str) or not source.strip():
                index += 1
                continue
            try:
                func = eval(source)
                if not callable(func):
                    index += 1
                    continue
                result = func(context)
                context.result = await result if inspect.isawaitable(result) else result
            except Exception:
                LoggerFactory.get_logger(__name__).exception(
                    "Command %s lambda failed at index %s: %s", command.name, index, source)
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
