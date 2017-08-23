import enum


class ChoicesEnum(enum.Enum):
    """
        Enumerator class for use with the django ORM choices field

    Usage:
        create a class with choices as fields like this

        # choices.py
        class COLOR_TYPE(ChoicesEnum):
            red = 'Green'
            green = 'Red'

        # models.py
        ...
        models.CharField('Color', choices=COLOR_TYPE.choices(), default=COLOR_TYPE.red.name, max_length=10)
        ...
    """

    @classmethod
    def choices_gen(cls):
        for attr in cls:
            yield (attr.name, attr.value)

    @classmethod
    def choices(cls):
        return tuple(cls.choices_gen())
