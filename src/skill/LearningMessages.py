class LearningMessages:
    """Transient improvement notices owned by a character, never persisted."""

    @staticmethod
    def queue(character, message):
        if character is None or not message:
            return
        messages = list(getattr(character, "_skill_improve_messages", []) or [])
        messages.append(str(message))
        character._skill_improve_messages = messages

    @staticmethod
    def take(character):
        if character is None:
            return ""
        messages = list(getattr(character, "_skill_improve_messages", []) or [])
        character._skill_improve_messages = []
        return "".join(messages)
