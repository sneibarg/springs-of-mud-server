__all__ = ['MudServer', 'LoggerFactory', 'TimeVal']


def __getattr__(name):
    # Importing logging/configuration helpers must not start the server graph.
    if name in __all__:
        from importlib import import_module
        return getattr(import_module(f".{name}", __name__), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
