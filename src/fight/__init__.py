from .CombatRegistry import CombatRegistry

__all__ = ["CombatRegistry", "FightHandler"]


def __getattr__(name):
    if name == "FightHandler":
        from .FightHandler import FightHandler
        return FightHandler
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
