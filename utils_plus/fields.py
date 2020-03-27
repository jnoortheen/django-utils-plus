from django.db import models
from .choices import ChoicesEnum


class ChoicesEnumField(models.CharField):
    """
        A wrapper around the standars models.CharField to ease the use of choices.ChoicesEnum.
    Features:
     - set max-length from the choices given if not set
     - Give the choices using the Enum class
     - When reading from database, it returns ChoicesEnum instance instead of the str
    """

    def __init__(self, enum_class, *args, **kwargs):
        """

        Args:
            enum_class (T[ChoicesEnum]):
            *args:
            **kwargs:
        """
        assert issubclass(enum_class, ChoicesEnum)
        kwargs['choices'] = tuple(enum_class.choices())
        if 'max_length' not in kwargs:
            kwargs['max_length'] = enum_class.max_length()
        self.enum_class = enum_class

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args.insert(0, self.enum_class)
        if 'choices' in kwargs:
            del kwargs['choices']
        return name, path, args, kwargs

    def to_python(self, value) -> ChoicesEnum:
        if not isinstance(value, self.enum_class):
            return self.enum_class[value]

        return value

    def clean(self, value, model_instance):
        data = self.to_python(value)
        return data

    def from_db_value(self, value, _, __):
        return value if value is None else self.enum_class[value]

    def get_prep_value(self, value):
        return value.name if isinstance(value, self.enum_class) else value
