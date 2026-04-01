from injector import inject
from registry.SocialRegistry import SocialRegistry
from server.messaging import MessageBus
from server.session.SessionHandler import SessionHandler


class SocialHandler:
    @inject
    def __init__(self, message_bus: MessageBus, social_registry: SocialRegistry, session_handler: SessionHandler):
        self.message_bus = message_bus
        self.social_registry = social_registry
        self.session_handler = session_handler

    async def handle_social(self, actor, raw_input: str, social=None) -> bool:
        text = (raw_input or "").strip()
        if not text:
            return False

        parts = text.split(" ", 1)
        social_name = parts[0].lower()
        target_name = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
        social = social or self.social_registry.get_social_by_name(social_name)
        if social is None:
            return False

        if not target_name:
            await self.message_bus.send_to_character(actor.id, self.message_bus.text_to_message(self._render(social.char_no_arg, actor) + "\r\n"))
            await self.message_bus.send_to_room(actor.room_id,self.message_bus.text_to_message(self._render(social.others_no_arg, actor) + "\r\n"), [actor.id])
            return True

        target = self._find_target_in_room(actor, target_name)
        if target is None:
            await self.message_bus.send_to_character(actor.id, self.message_bus.text_to_message(self._render(social.char_not_found, actor) + "\r\n"))
            return True

        if target.id == actor.id:
            await self.message_bus.send_to_character(actor.id, self.message_bus.text_to_message(self._render(social.char_auto, actor, actor) + "\r\n"))
            await self.message_bus.send_to_room(actor.room_id, self.message_bus.text_to_message(self._render(social.others_auto, actor, actor) + "\r\n"),[actor.id])
            return True

        await self.message_bus.send_to_character(actor.id, self.message_bus.text_to_message(self._render(social.char_found, actor, target) + "\r\n"))
        await self.message_bus.send_to_character(target.id, self.message_bus.text_to_message(self._render(social.vict_found, actor, target) + "\r\n"))
        await self.message_bus.send_to_room(actor.room_id, self.message_bus.text_to_message(self._render(social.others_found, actor, target) + "\r\n"),[actor.id, target.id])
        return True

    def _find_target_in_room(self, actor, target_name: str):
        wanted = target_name.lower()
        for session in self.session_handler.get_playing_sessions():
            char = session.character
            if char.room_id != actor.room_id:
                continue
            if char.name.lower() == wanted or char.name.lower().startswith(wanted):
                return char
        return None

    @staticmethod
    def _render(template: str, actor, target=None) -> str:
        if not template:
            return ""
        result = template
        actor_name = "Someone" if getattr(actor, "cloaked", False) else actor.name
        target_name = target.name if target else ""
        result = result.replace("$n", actor_name).replace("$N", target_name)
        result = result.replace("%actor%", actor_name).replace("%target%", target_name)
        return result

