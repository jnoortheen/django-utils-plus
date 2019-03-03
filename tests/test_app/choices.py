from utils_plus.choices import ChoicesOrderEnum


class COLOR_TYPE(ChoicesOrderEnum):
    red = 'RED'
    green = 'GREEN'
    blue = 'BLUE'
    vars = ['Vario', 'Varied']

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_, obj.alt = value if isinstance(value, list) else (value, value)
        return obj
