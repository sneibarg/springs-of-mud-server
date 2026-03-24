from dataclasses import dataclass


@dataclass
class PromptFormat:
    hp: bool
    max_hp: bool
    mana: bool
    max_mana: bool
    movement: bool
    max_movement: bool
    xp: bool
    max_xp: bool
    gold: bool
    silver: bool

    def format_prompt(self):
        pass
