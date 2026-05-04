__all__ = ['Item', 'ItemMacros.py']


def __getattr__(name):
    if name == "Item":
        from .Item import Item
        return Item
    if name == "ObjectMacros":
        from .ItemMacros import ObjectMacros
        return ObjectMacros
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

