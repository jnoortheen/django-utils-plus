# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest.mock import Mock

from django.conf.urls import url

# Create your views here.
from django.views import View
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

__all__ = ['ContextMixinPlus', 'CreateUpdateMixin', ]


class ContextMixinPlus(ContextMixin):
    """
    This mixin will add all url parameters to context and updates context with extra_context defined in inherited
    classes

    Usage:

    >>> class GenricView(ContextMixinPlus, View):
    ...     three = 0;four = 0;
    ...     kwargs = {'one':1, 'two':2}
    >>> view = GenricView()
    >>> view.get_context_data(six=6, five=5).keys()
    dict_keys(['six', 'five', 'view', 'one', 'two'])
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
        c = super(ContextMixinPlus, self).get_context_data(**kwargs)  # type: dict
        for k in self.kwargs:
            c[k] = self.kwargs[k]
        c.update(self.extra_context)
        c.update(self.get_extra_context())
        return c


class CreateUpdateMixin(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    """This can be used instead both CreateView and EditView. Please see ``urls`` method for more information on routing
     this view.
    """

    def _set_object(self, kwargs):
        """

        Args:
            kwargs (dict):

        Returns:
        """
        return self.get_object() if 'pk' in kwargs else None

    def get(self, request, *args, **kwargs):
        """

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        >>> c = CreateUpdateMixin()
        >>> c.get_object = Mock()
        >>> ProcessFormView.get = Mock()
        >>> obj = c.get(request='', pk=1)
        >>> c.get_object.assert_called_once()
        """
        self.object = self._set_object(kwargs)
        return super(CreateUpdateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        >>> c = CreateUpdateMixin()
        >>> c.get_object = Mock()
        >>> ProcessFormView.post = Mock()
        >>> obj = c.post(request='', pk=1)
        >>> c.get_object.assert_called_once()
        """
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

        >>> from django.urls import reverse
        >>> reverse('author:add')
        '/blog/author_profile/add/'
        >>> reverse('author:edit', args=[12])
        '/blog/author_profile/edit/12/'
        """
        return [
            url('^add/$', cls.as_view(**initkwargs), name='add'),
            url('^edit/(?P<pk>\d+)/$', cls.as_view(**initkwargs), name='edit'),

            # if you use `django-addanother` then this will come in handy
            url('^edit/(?P<pk>__fk__)/$', cls.as_view(**initkwargs), name='edit-s'),
        ]
