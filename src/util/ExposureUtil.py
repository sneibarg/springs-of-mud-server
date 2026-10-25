def exposure_chance(level, damage):
    """ROM's unclamped collateral chance, before element-specific modifiers."""
    chance = level // 4 + damage // 10
    if chance > 25:
        chance = (chance - 25) // 2 + 25
    if chance > 50:
        chance = (chance - 50) // 2 + 50
    return chance


def item_kind(item, item_table):
    raw = str(item.item_type).lower()
    return item_table.get(raw, {}).get("type", raw).lower().removeprefix("item_")
