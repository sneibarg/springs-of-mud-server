def dexterity_defense(character, bonus_lookup):
    from util.GenericUtil import GenericUtil

    attrs = getattr(character, "character_attributes", None)
    dexterity = getattr(attrs, "dexterity", 0)
    return GenericUtil.to_int(bonus_lookup("dexterity", str(dexterity)).get("defensive", 0), 0)


def legacy_armor_class(armor, character, category):
    """Compatibility for ArmorClass.get_ac: raw AC, before combat scaling."""
    from api.CharacterApi import CharacterApi

    if isinstance(category, int):
        category = {0: "pierce", 1: "bash", 2: "slash", 3: "exotic"}.get(category, "pierce")
    if isinstance(category, str):
        key = category.lower()
        key = "pierce" if key == "piercing" else key
        base = armor.base_value(key if key in ("pierce", "bash", "slash") else "exotic")
    else:
        base = 0
    return int(base) + dexterity_defense(character, CharacterApi.get_attribute_bonus)
