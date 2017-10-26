from __future__ import absolute_import

from django import template
from django.conf import settings
from django.templatetags.static import static

from ..utils import get_node_modules_dir, get_unpkg_url

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


if settings.DEBUG:
    # add node_modules to list of static folders to find and load in local development
    settings.STATICFILES_DIRS = settings.STATICFILES_DIRS + [
        get_node_modules_dir()
    ]


@register.simple_tag
def unpkg(path):
    """
        Alternative to standard `static` template tag. When you are using external static files/libraries
        like bootstrap, jquery you may want to load them from CDNs instead of managing them yourself in production.
        This tag helps you to do that. When `settings.DEBUG` is false, this will return paths that resolved from
        `package.json` to versioned `unpkg.com`. Otherwise it will resolve to `node_modules` locally.
    Args:
        path (str):

    Returns:
        str: assets path resolved either to node_modules directory or https://unpkg.com/#/ in production.

    Usage:

        load the template tags and use `unpkg` like `static` tag,

        ```
        {% load static utils_plus_tags %}
        <link rel="stylesheet" type="text/css" href="{% unpkg 'bootstrap/dist/css/bootstrap.min.css' %}"/>
        <script src="{% unpkg 'bootstrap/dist/js/bootstrap.min.js' %}"></script>
        <script src="{% unpkg 'jquery/dist/jquery.min.js' %}"></script>
        ```
    Note:
        1. the package.json should be present in the project ROOT DIR.
        2. When DEBUG is True the packages must  be installed and should be available already inside `node_modules`.
    """

    return (
        static(path)
        if settings.DEBUG
        else get_unpkg_url(path)
    )
