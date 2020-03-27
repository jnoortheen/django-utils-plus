"""
Usage: see tests/test_mixins.py
"""
# pylint: disable=R0201
from typing import Dict, Any, Optional

from django.db.models import Model
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from utils_plus.router import url

__all__ = ['ContextMixinPlus', 'CreateUpdateMixin', ]

Ctx = Dict[str, Any]


class ContextMixinPlus(ContextMixin):
    """
    This mixin will add all url parameters to context and updates context with extra_context defined in inherited
    classes
    """
    extra_context: Ctx = {}  # This can be overridden by subclasses; it must be returning a dict
    kwargs: Ctx = {}  # the one set by View dispatch

    def get_extra_context(self) -> Ctx:
        """
        this method will be overridden
        Returns:
            dict:
        """
        return self.extra_context

    def get_context_data(self, **kwargs):
        ctx = super(ContextMixinPlus, self).get_context_data(**kwargs)  # type: dict
        for k in self.kwargs:
            ctx[k] = self.kwargs[k]
        ctx.update(self.get_extra_context())
        return ctx


class CreateUpdateMixin(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    """This can be used instead both CreateView and EditView.
     Please see method ``.urls`` method for more information on routing this view.
    """
    pk_type = "int"  # to restrict on the url-path
    url_pk_name = "pk"

    def opt_get_object(self, kwargs) -> Optional[Model]:
        """Return model-object if `pk` in url's kwargs'.
        """
        return self.get_object() if self.url_pk_name in kwargs else None

    def get(self, request, *args, **kwargs):
        self.object = self.opt_get_object(kwargs)
        return super(CreateUpdateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.opt_get_object(kwargs)
        return super(CreateUpdateMixin, self).post(request, *args, **kwargs)

    @classmethod
    def urls(cls, name_prefix: str, **initkwargs) -> url:
        """
            since this class works like a ViewSet, it is a good idea to create a urls method which would add routes for
            create/update of a model object. This add two routes for the given namespace.
        Returns:
            list: url patterns
        Usage:
            # in urls.py
            urls = url("author")[
                CreateUpdateAuthorView.urls(name_prefix='author'), # helper to use with url objects
            ],
            urlpatterns = list(urls)

            # it is equivalent to
            urlpatterns = [
                path("author/add", CreateUpdateAuthorView.as_view(), name="author-add"),
                path("author/<int:pk>/edit", CreateUpdateAuthorView.as_view(), name="author-edit"),
            ]

        See Also
            `tests/test_app/urls.py`
        """
        return (
                url('add', view=cls.as_view(**initkwargs), name=f'{name_prefix}-add') +
                url.pk()[
                    url('edit', view=cls.as_view(**initkwargs), name=f'{name_prefix}-edit', dtype=cls.pk_type)
                ]
        )
