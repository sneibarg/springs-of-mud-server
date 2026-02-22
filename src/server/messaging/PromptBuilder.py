from server.protocol import Message, MessageType


class PromptBuilder:
    """
    Builds game prompts for players.
    Supports different prompt styles and customization.
    """

    @staticmethod
    def build_standard_prompt(health: int, mana: int, movement: int) -> Message:
        """Build standard MUD prompt: <hp m mv>"""
        text = f"<{health}hp {mana}m {movement}mv>\r\n"

        return Message(
            type=MessageType.PROMPT,
            data={
                'text': text,
                'health': health,
                'mana': mana,
                'movement': movement
            }
        )

    @staticmethod
    def build_percentage_prompt(health: int, max_health: int, mana: int, max_mana: int,
                               movement: int, max_movement: int) -> Message:
        """Build prompt with percentages"""
        hp_pct = int((health / max_health) * 100) if max_health > 0 else 0
        mana_pct = int((mana / max_mana) * 100) if max_mana > 0 else 0
        mv_pct = int((movement / max_movement) * 100) if max_movement > 0 else 0

        text = f"<{hp_pct}% hp {mana_pct}% m {mv_pct}% mv>\r\n"

        return Message(
            type=MessageType.PROMPT,
            data={
                'text': text,
                'health': health,
                'max_health': max_health,
                'mana': mana,
                'max_mana': max_mana,
                'movement': movement,
                'max_movement': max_movement
            }
        )

    @staticmethod
    def build_custom_prompt(template: str, **kwargs) -> Message:
        """Build a custom prompt from template"""
        text = template.format(**kwargs)

        if not text.endswith('\r\n'):
            text += '\r\n'

        return Message(
            type=MessageType.PROMPT,
            data={'text': text, **kwargs}
        )
