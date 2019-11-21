from __future__ import with_statement

from dataclasses import dataclass
from typing import Tuple, Union

from django.conf.urls import include
from django.urls.resolvers import URLPattern, URLResolver
from django.conf import settings
from django.urls import path, re_path

TRAILING_SLASH_SETTING_NAME = 'URL_GROUP_TRAIL_SLASH'

TRAIL_SLASH = getattr(settings, TRAILING_SLASH_SETTING_NAME, True)


class UrlGroup:
    def __init__(self, route: str):
        self.route = route

    def __getitem__(self, item: Tuple[Union[URLResolver, URLPattern]]):
        for p in item:
            print(p)


class _UrlBuilder:
    """
    An elegant and DRY way to define urlpatterns with so many nested levels and syntax sugars.
    It is just a wrapper behind the standard url(), include() methods.

    Usage:

    ### urls.py ###

    urlpatterns = [
        u('editor')[
            u.int('doc_pk')[
                u('edit', DocEditorView.as_view(), 'edit-doc'),
                u('export', DocExporterView.as_view(), 'export-doc'),
            ]
        ],
        u('docs', Docs.as_view(), 'student-documents'),
        u('publish', DeleteOrPublistDocument.as_view(), 'publish_document', action='publish'),
        u('delete', DeleteOrPublistDocument.as_view(), 'delete_document'),
    ]

    see tests/test_router.py for more use cases
    """

    def __call__(self, route: str, view: callable = None, url_name: str = None, **kwargs):
        if view:
            return path(route, view, url_name, kwargs)
        else:
            return UrlGroup(route)

    def re(self, var_name, regex, view=None, url_name=None, **kwargs):
        return re_path(r'(?P<{}>{})'.format(var_name, regex), view, url_name, **kwargs)

    def var(self, var_name, view=None, url_name=None, dtype=None, **kwargs):
        route = f"{dtype}:{var_name}" if dtype else str(var_name)
        return self.__call__(f"<{route}>", view, url_name, **kwargs)

    def int(self, var_name, view=None, url_name=None, **kwargs):
        return self.var(var_name, view, url_name, dtype="int", **kwargs)

    def pk(self, view=None, url_name=None, dtype="int", **kwargs):
        return self.var('pk', view, url_name, dtype=dtype, **kwargs)

    def slug(self, var_name, view=None, url_name=None, **kwargs):
        return self.var(var_name, view, url_name, dtype='slug', **kwargs)


u = _UrlBuilder()
__all__ = ['u', ]
