import re
from typing import List, Dict, Any

from injector import inject
from player.Character import Character
from player.CharacterRegistry import CharacterRegistry
from server.messaging import MessageBus
from server.session.SessionHandler import SessionHandler


LOOK_CTX_KEY = "_look_ctx"
LOOK_IN_ALIASES = {"i", "in", "on"}
LOOK_DIRECTIONS = {"n", "north", "e", "east", "s", "south", "w", "west", "u", "up", "d", "down"}


class PlayerHandler:
    @inject
    def __init__(self, message_bus: MessageBus, character_registry: CharacterRegistry, session_handler: SessionHandler):
        self.__name__ = "PlayerHandler"
        self.message_bus = message_bus
        self.character_registry = character_registry
        self.session_handler = session_handler

    async def print_visible(self, character):
        who_list = [character] + self._visible(character)
        who_line = ""
        players_found = "Players found: " + str(len(who_list)) + "\r\n"
        for c in who_list:
            who_line = who_line + f"[{c.level}    {c.race}    {c.character_class.name}] {c.name} {c.title}\r\n"

        who_line = who_line + players_found
        message = self.message_bus.text_to_message(who_line)
        await self.message_bus.send_to_character(character.id, message)

    async def to_player(self, character_id, text):
        text += "\r\n"
        message = self.message_bus.text_to_message(text)
        await self.message_bus.send_to_character(character_id, message)

    def _visible(self, character) -> List[Character]:
        visible = []
        for session in self.session_handler.get_playing_sessions():
            char = session.character
            if char.id == character.id:
                continue
            if char.cloaked and character.role == "player":
                continue
            visible.append(char)
        return visible

    def _look_ctx(self, character: Character) -> Dict[str, Any]:
        if character.loot is None:
            character.loot = {}
        ctx = character.loot.get(LOOK_CTX_KEY)
        if not isinstance(ctx, dict):
            ctx = {
                "arg1": "",
                "arg2": "",
                "arg3": "",
                "argument": "",
                "number": 1,
                "count": 0,
                "branch": None,
                "done": False,
            }
            character.loot[LOOK_CTX_KEY] = ctx
        return ctx

    async def look_begin(self, character: Character, argument: str = ""):
        text = " ".join((argument or "").split())
        parts = text.split(" ", 1)
        arg1 = parts[0].strip().lower() if parts and parts[0] else ""
        arg2 = parts[1].strip().lower() if len(parts) > 1 else ""

        number = 1
        arg3 = arg1
        match = re.match(r"^(\d+)\.(.+)$", arg1)
        if match:
            number = max(1, int(match.group(1)))
            arg3 = match.group(2).strip().lower()

        character.loot[LOOK_CTX_KEY] = {
            "arg1": arg1,
            "arg2": arg2,
            "arg3": arg3,
            "argument": text,
            "number": number,
            "count": 0,
            "branch": "default" if arg1 in ("", "auto") else None,
            "done": False,
        }

    def look_context(self, character: Character) -> Dict[str, Any]:
        return self._look_ctx(character)

    def look_done(self, character: Character) -> bool:
        return bool(self._look_ctx(character).get("done", False))

    def look_mark_done(self, character: Character):
        self._look_ctx(character)["done"] = True

    def look_register_match(self, character: Character) -> bool:
        ctx = self._look_ctx(character)
        ctx["count"] = int(ctx.get("count", 0)) + 1
        return ctx["count"] == int(ctx.get("number", 1))

    def look_keyword_matches(self, token: str, keyword: str) -> bool:
        t = (token or "").strip().lower()
        k = (keyword or "").strip().lower()
        if not t or not k:
            return False
        words = [w for w in k.split() if w]
        return any(w == t or w.startswith(t) for w in words)

    def look_is_named_target_query(self, character: Character) -> bool:
        ctx = self._look_ctx(character)
        arg1 = ctx.get("arg1", "")
        if not arg1:
            return False
        if arg1 in LOOK_IN_ALIASES:
            return False
        return True

    async def look_complete_default(self, character: Character):
        if self.look_done(character):
            return
        ctx = self._look_ctx(character)
        if ctx.get("branch") == "default":
            ctx["done"] = True

    async def look_player_target(self, character: Character):
        if self.look_done(character):
            return

        ctx = self._look_ctx(character)
        arg1 = ctx.get("arg1", "")
        if not arg1 or arg1 in LOOK_IN_ALIASES:
            return

        target = None
        for session in self.session_handler.get_playing_sessions():
            cand = session.character
            if cand.room_id != character.room_id:
                continue
            c_name = cand.name.lower()
            if c_name == arg1 or c_name.startswith(arg1):
                target = cand
                break

        if target is None:
            return

        header = target.name
        if target.title:
            header += f" {target.title}"
        desc = target.description.strip() if target.description else "You see nothing special."
        text = f"{header}\r\n{desc}\r\n"
        await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
        self.look_mark_done(character)

    async def look_finalize_count_message(self, character: Character):
        if self.look_done(character):
            return

        ctx = self._look_ctx(character)
        count = int(ctx.get("count", 0))
        number = int(ctx.get("number", 1))
        token = ctx.get("arg3", "that")

        if count > 0 and count != number:
            if count == 1:
                text = f"You only see one {token} here.\r\n"
            else:
                text = f"You only see {count} of those here.\r\n"
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message(text))
            self.look_mark_done(character)

    async def look_fallback_not_here(self, character: Character):
        if self.look_done(character):
            return
        arg1 = self._look_ctx(character).get("arg1", "")
        if arg1:
            await self.message_bus.send_to_character(character.id, self.message_bus.text_to_message("You do not see that here.\r\n"))
            self.look_mark_done(character)

    async def look_finish(self, character: Character):
        if character.loot and LOOK_CTX_KEY in character.loot:
            del character.loot[LOOK_CTX_KEY]