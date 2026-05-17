__all__ = ['Item', 'ItemApi.py']


def __getattr__(name):
    if name == "Item":
        from .Item import Item
        return Item
    if name == "ItemApi":
        from api.ItemApi import ItemApi
        return ItemApi
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

