__all__ = ['Item', 'ObjectMacros']


def __getattr__(name):
    if name == "Item":
        from .Item import Item
        return Item
    if name == "ObjectMacros":
        from .ObjectMacros import ObjectMacros
        return ObjectMacros
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

