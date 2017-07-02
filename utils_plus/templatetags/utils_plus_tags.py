from django import template

register = template.Library()


@register.filter
def klass(obj):
    """
        returns class name of the object. Might be useful when rendering widget class names
    Args:
        obj:

    Returns:

    """
    return obj.__class__.__name__
