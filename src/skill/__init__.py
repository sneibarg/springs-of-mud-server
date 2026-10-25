__all__ = ['Ability', 'Skill', 'Spell']


def __getattr__(name):
    # Resolver and learning services must not eagerly construct the model graph.
    if name in __all__:
        from importlib import import_module
        return getattr(import_module(f".{name}", __name__), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
