import enum


class ChoicesEnum(enum.Enum):
    @classmethod
    def choices_gen(cls):
        for attr in cls:
            yield (attr.name, attr.value)

    @classmethod
    def choices(cls):
        return tuple(cls.choices_gen())
