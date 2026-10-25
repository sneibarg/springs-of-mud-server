class ArmorValues:
    """Four-category armor contract shared by the two wire-format adapters."""

    CATEGORIES = {
        "pierce": ("piercing", "pierce"),
        "bash": ("bashing", "bash"),
        "slash": ("slashing", "slash"),
        "exotic": ("magic", "exotic"),
    }

    def base_value(self, category):
        category = str(category).lower().removeprefix("dam_")
        fields = ArmorValues.CATEGORIES.get(category, ArmorValues.CATEGORIES["exotic"])
        for name in fields:
            if hasattr(self, name):
                return getattr(self, name)
        return 0

    def adjust_all(self, modifier):
        from util.GenericUtil import GenericUtil

        for fields in ArmorValues.CATEGORIES.values():
            for name in fields:
                if hasattr(self, name):
                    setattr(self, name, GenericUtil.to_int(getattr(self, name), 0) + modifier)

    def reset_all(self, value):
        for fields in ArmorValues.CATEGORIES.values():
            for name in fields:
                if hasattr(self, name):
                    setattr(self, name, value)
