from dataclasses import dataclass


@dataclass
class CharacterFlags:
    auto_assist: bool
    auto_exit: bool
    auto_loot: bool
    auto_sacrifice: bool
    auto_gold: bool
    auto_split: bool
    holy_light: bool
    can_loot: bool
    no_summon: bool
    no_follow: bool
    color: bool
    permit: bool
    log: bool
    deny: bool
    freeze: bool
    thief: bool
    killer: bool

    @classmethod
    def from_json(cls, data) -> CharacterFlags:
        from util.GenericUtil import GenericUtil
        return cls(**GenericUtil.camel_to_snake_case(data))
