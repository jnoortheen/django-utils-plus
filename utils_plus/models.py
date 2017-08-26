# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class QueryManager(models.Manager):
    """
        A DRYer way to set select_related, prefetch_related & filters to queryset
    """
    _prefetches = ()
    _selects = ()
    _order_by = ()
    _args = ()
    _kwargs = {}

    def __init__(self, *args, **kwargs):
        """
            any arguments that you would pass on to filter
        """
        self._args = args
        self._kwargs = kwargs
        super(QueryManager, self).__init__()

    def prefetches(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's select_related
        """
        self._prefetches = args
        return self

    def selects(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's select_related
        """
        self._selects = args
        return self

    def order_by(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's select_related
        """
        self._order_by = args
        return self

    def get_queryset(self):
        qs = super(QueryManager, self).get_queryset().filter(*self._args, **self._kwargs)

        if self._selects:
            qs.select_related(*self._selects)

        if self._prefetches:
            qs.prefetch_related(*self._prefetches)

        if self._order_by:
            qs.order_by(*self._order_by)

        return qs
