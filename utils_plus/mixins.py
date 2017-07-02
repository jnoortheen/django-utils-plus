# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

# Create your views here.
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

__all__ = ['ContextMixinPlus', 'CreateUpdateMixin', ]


class ContextMixinPlus(ContextMixin):
    """This mixin will add all url parameters to context and updates context with extra_context defined in inherited
    classes"""
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() if kwargs.has_key('pk') else None
        return super(CreateUpdateMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() if kwargs.has_key('pk') else None
        return super(CreateUpdateMixin, self).post(request, *args, **kwargs)

    @classmethod
    def urls(cls):
        """
            since this class works like a ViewSet, it is a good idea to create a urls method which would add routes for
            create/update of a model object. This add two routes for the given namespace.
        Returns:
            list: url patterns
        Usage:
            urls.py ~
                urlpatterns = [
                    url(r'^xfield/', include(CreateUpdateMixin.urls(), namespace='xfield')),
                ]
            views/templates  or any
                reverse('xfield:add') = '/xfield/add/'
                reverse('xfield:edit', args=[12]) = '/xfield/edit/12'
        """
        return [
            url('^add/$', cls.as_view(), name='add'),
            url('^edit/(?P<pk>\d+)/$', cls.as_view(), name='edit'),

            # if you use `django-addanother` then this will come in handy
            url('^edit/(?P<pk>__fk__)/$', cls.as_view(), name='edit-s'),
        ]
