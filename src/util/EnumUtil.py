class EnumUtil:
    @staticmethod
    def value(enum_obj, *names: str) -> int | None:
        if enum_obj is None:
            return 0

        members = getattr(enum_obj, "__members__", None)
        for name in names:
            if members is not None and name in members:
                return EnumUtil._to_int(getattr(members[name], "value", members[name]), 0)

            member = getattr(enum_obj, name, None)
            value = EnumUtil._to_int(getattr(member, "value", member), None)
            if value is not None:
                return value

        return 0

    @staticmethod
    def _to_int(value, default: int | None = 0) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default
