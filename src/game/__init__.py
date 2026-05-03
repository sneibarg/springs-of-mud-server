from .GameData import GameData, Version, Integrity, BuildInfo

__all__ = ['GameData', 'GameService', 'Version', 'Integrity', 'BuildInfo']


def __getattr__(name):
    if name == "GameService":
        from .GameService import GameService
        return GameService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
