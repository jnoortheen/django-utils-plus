# pylint: disable=C0103,R0201
from typing import Tuple, Union, Callable, Optional, Any

from django.http import HttpResponse
from django.urls import re_path, path, URLPattern, URLResolver

# in case of include we get a tuple
ViewType = Optional[Union[Callable[..., HttpResponse], Tuple[Any, Any, Any]]]


class url:
    """
    An elegant and DRY way to define urlpatterns with so many nested levels and syntax sugars.
    It is just a wrapper behind the standard re_path/path functions.

    Usage:

    ### urls.py ###

    urlpatterns = list(
        url('editor')[
            url.int('doc_pk')[
                url('edit', DocEditorView.as_view(), 'edit-doc'),
                url('export', DocExporterView.as_view(), 'export-doc'),
            ]
        ]
        + url('docs', Docs.as_view(), 'student-documents')
        + url('publish', DeleteOrPublistDocument.as_view(), 'publish_document', action='publish')
        + url('delete', DeleteOrPublistDocument.as_view(), 'delete_document')
    )

    see tests/test_router.py for more use cases
    """

    def __init__(self, prefix: str, view: ViewType = None, name=None, is_regex=False, **kwargs):
        slash = "" if (not prefix or prefix.endswith("/")) else "/"
        self.prefix = f"{prefix}{slash}"
        self.view = view
        self.name = name
        self.kwargs = kwargs
        self.is_regex = is_regex  # regex path
        self.others: Tuple["url", ...] = ()

    def __repr__(self):
        return f"url`{self.prefix}`" + (f".({len(self.others)})" if self.others else "")

    def _prefix(self, other: "url"):
        slash = "" if not self.prefix or self.prefix.endswith("/") or other.prefix.startswith("/") else "/"
        end_slash = "" if not other.prefix or other.prefix.endswith("/") else "/"
        other.prefix = f"{self.prefix}{slash}{other.prefix}{end_slash}"
        return other

    def __getitem__(self, uobjs: Union['url', Tuple['url', ...]]) -> 'url':
        if not isinstance(uobjs, tuple):
            uobjs = (uobjs,)
        for obj in uobjs:
            self.others += (self._prefix(obj),) + tuple(self._prefix(innu) for innu in obj.others)
        return self

    def __add__(self, other: "url") -> 'url':
        self.others += (other,) + other.others
        return self

    def _path(self) -> Union[URLPattern, URLResolver]:
        if self.is_regex:
            func = re_path
        else:
            func = path
        return func(self.prefix, self.view, kwargs=self.kwargs, name=self.name)

    def __iter__(self):
        uobjs = (self,) + self.others
        for obj in uobjs:
            if obj.view:
                yield obj._path()

    @classmethod
    def re(cls, var_name: str, regex: str, view: ViewType = None, name=None, **kwargs) -> "url":
        """implements urls.re_path"""
        return cls(rf'(?P<{var_name}>{regex})', view, name=name, is_regex=True, **kwargs)

    @classmethod
    def var(cls, var_name, view=None, name=None, dtype=None, **kwargs) -> "url":
        """Implements having url-arguments. dtype is the casting argument.
        the default cast-type is str as Django."""
        route = f"{dtype}:{var_name}" if dtype else str(var_name)
        return cls(f"<{route}>", view, name, **kwargs)

    @classmethod
    def int(cls, var_name, view=None, name=None, **kwargs) -> "url":
        """Implements
            ..
                path("<int:var_name>", view, )
        """
        return cls.var(var_name, view, name, dtype="int", **kwargs)

    @classmethod
    def slug(cls, view=None, name=None, var_name="slug", **kwargs) -> "url":
        """Implements
            ..
                path("<slug:slug>", view, )
        """
        return cls.var(var_name=var_name, view=view, name=name, dtype='slug', **kwargs)

    @classmethod
    def uuid(cls, view=None, name=None, var_name="uuid", **kwargs) -> "url":
        """Implements
            ..
                path("<uuid:uuid>", view, )
        """

        return cls.var(var_name, view, name, dtype="uuid", **kwargs)

    @classmethod
    def path(cls, var_name, view=None, name=None, **kwargs) -> "url":
        return cls.var(var_name, view, name, dtype="path", **kwargs)

    @classmethod
    def pk(cls, view=None, name=None, dtype="int", **kwargs) -> "url":
        return cls.var('pk', view=view, name=name, dtype=dtype, **kwargs)


__all__ = ['url', ]
