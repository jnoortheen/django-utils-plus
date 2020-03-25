"""
Usage: see tests/test_mixins.py
"""
# pylint: disable=R0201
from django.urls import path
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

__all__ = ['ContextMixinPlus', 'CreateUpdateMixin', ]


class ContextMixinPlus(ContextMixin):
    """
    This mixin will add all url parameters to context and updates context with extra_context defined in inherited
    classes
    """
    extra_context = {}  # This can be overridden by subclasses; it must be returning a dict
    kwargs = {}

    def get_extra_context(self):
        """
        this method will be overridden
        Returns:
            dict:
        """
        return {}

    def get_context_data(self, **kwargs):
        ctx = super(ContextMixinPlus, self).get_context_data(**kwargs)  # type: dict
        for k in self.kwargs:
            ctx[k] = self.kwargs[k]
        ctx.update(self.extra_context)
        ctx.update(self.get_extra_context())
        return ctx


class CreateUpdateMixin(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    """This can be used instead both CreateView and EditView.
     Please see method ``.urls`` method for more information on routing this view.
    """
    enable_add_another = False
    pk_type = "int"  # to restrict on the url-path

    def _set_object(self, kwargs):
        """

        Args:
            kwargs (dict):

        Returns:
        """
        return self.get_object() if 'pk' in kwargs else None

    def get(self, request, *args, **kwargs):
        self.object = self._set_object(kwargs)
        return super(CreateUpdateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self._set_object(kwargs)
        return super(CreateUpdateMixin, self).post(request, *args, **kwargs)

    @classmethod
    def urls(cls, **initkwargs):
        """
            since this class works like a ViewSet, it is a good idea to create a urls method which would add routes for
            create/update of a model object. This add two routes for the given namespace.
        Returns:
            list: url patterns
        Usage:
            in urls.py see tests/test_app
                urlpatterns = [
                    url(r'^xfield/', include(CreateUpdateMixin.urls(), namespace='xfield')),
                ]
        """

        urls = [
            path('add/', cls.as_view(**initkwargs), name='add'),
            path(f'edit/<{cls.pk_type}:pk>/', cls.as_view(**initkwargs), name='edit'),
        ]
        if cls.enable_add_another:
            urls.append(  # if you use `django-addanother` then this will come in handy
                path(f'edit/<{cls.pk_type}:pk>/', cls.as_view(**initkwargs), name='edit-s'),
            )
