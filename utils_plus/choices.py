import enum


class StrEnum(str, enum.Enum):
    pass


class IntChoicesEnum(enum.IntEnum):
    """
    Enumerator class for use with django ORM IntegerField choices. The values must be int and will be stored in db.

    Usage:
        create a class with choices as fields like this

    >>> # choices.py
    >>> class COLOR_TYPE(IntChoicesEnum):
    ...     red_value = 0
    ...     green_value = 1

    in models.py you can use it like this
    models.SmallPositiveIntegerField('Color', choices=COLOR_TYPE.choices(), default=COLOR_TYPE.red)

    >>> COLOR_TYPE.red_value.value
    0
    >>> assert COLOR_TYPE.red_value == 0
    >>> COLOR_TYPE['red_value'].value
    0
    >>> tuple(COLOR_TYPE.choices())
    ((0, 'Red Value'), (1, 'Green Value'))
    """

    @classmethod
    def choices(cls):
        for attr in cls:
            yield (attr.value, attr.name.replace('_', ' ').title())


class ChoicesEnum(StrEnum):
    """
        Enumerator class for use with the django ORM CharField choices. The values must be string otherwise they will be
        converted to string.

    Usage:
        create a class with choices as fields like this

    >>> class COLOR_TYPE(ChoicesEnum):
    ...     red = 'RED'
    ...     green = 'GREEN'
    >>> COLOR_TYPE.red.value
    'RED'
    >>> COLOR_TYPE.red.name
    'red'
    >>> COLOR_TYPE['red'].value
    'RED'
    >>> COLOR_TYPE['red'].name
    'red'
    >>> tuple(COLOR_TYPE.choices())
    (('red', 'RED'), ('green', 'GREEN'))
    >>> COLOR_TYPE.max_length()
    5
    >>> COLOR_TYPE.red.next().name
    'green'
    >>> COLOR_TYPE.green.next().name
    'green'
    >>> COLOR_TYPE.green.prev().name
    'red'
    >>> COLOR_TYPE.red.prev().name
    'red'

    in models.py you can use it like below
    ...
    models.CharField('Color', choices=COLOR_TYPE.choices(), default=COLOR_TYPE.red.name, max_length=10)
    ...
    """

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            return self
        return members[index]

    def prev(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) - 1
        if index < 0:
            return self
        return members[index]

    @classmethod
    def max_length(cls):
        return max((len(x.name) for x in cls))

    @classmethod
    def choices(cls):
        for attr in cls:
            yield (attr.name, attr.value)
