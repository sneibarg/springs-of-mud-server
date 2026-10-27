"""Compatibility defaults for message keys absent from older live content."""

import json
from functools import lru_cache
from pathlib import Path

from game.GamePayload import GamePayload


@lru_cache(maxsize=None)
def bundled_payload(name):
    path = Path(__file__).resolve().parents[2] / 'resources' / 'collections' / 'SOMDB.Commands.json'
    with path.open(encoding='utf-8-sig') as source:
        command = next(entry for entry in json.load(source) if entry.get('name') == name)
    return GamePayload.from_json(command['payload'])


def render_command_message(command, channel, key, **tokens):
    fallback = ''
    if key not in getattr(command.payload, channel, {}):
        fallback = bundled_payload(command.name).render(channel, key, **tokens)
    return command.render_message(channel, key, fallback=fallback, **tokens)
