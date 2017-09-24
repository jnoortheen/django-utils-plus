from django import template

register = template.Library()


@register.filter
def klass(obj):
    """
        returns class name of the object. Might be useful when rendering widget class names
    Args:
        obj: any python class object

    Returns:
        str: name of the class

    >>> from tests.test_app.models import Author
    >>> klass(Author)
    'ModelBase'
    """
    return obj.__class__.__name__
