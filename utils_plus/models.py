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
            *args: this will be passed onto queryset's prefetch
        Returns:
            QueryManager:

        >>> objects = QueryManager().prefetches('m2m_field', 'rel_model_field')
        >>> objects._prefetches
        ('m2m_field', 'rel_model_field')
        """
        self._prefetches = args
        return self

    def selects(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's select_related
        Returns:
            QueryManager:

        >>> objects = QueryManager().selects('fk_field', 'rel_model_field')
        >>> objects._selects
        ('fk_field', 'rel_model_field')
        """
        self._selects = args
        return self

    def order_by(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's select_related

        Returns:
            QueryManager:

        >>> objects = QueryManager().order_by('-id', '-field_name')
        >>> objects._order_by
        ('-id', '-field_name')
        """
        self._order_by = args
        return self

    def get_queryset(self):
        """

        Returns:
            models.QuerySet:
        """
        qs = super(QueryManager, self).get_queryset().filter(*self._args, **self._kwargs)  # type: models.QuerySet

        if self._selects:
            qs = qs.select_related(*self._selects)

        if self._prefetches:
            qs = qs.prefetch_related(*self._prefetches)

        if self._order_by:
            qs = qs.order_by(*self._order_by)

        return qs

    def first_or_create(self, **kwargs):
        """
            return first record that matches the query if exists else create a record and return
        Args:
            **kwargs: class attributes and values

        Returns:
            (models.Model, bool): object & created_or_not

        Usage:

        >>> db = getfixture('db')
        >>> from django.db import models
        >>> from tests.test_app.models import Author
        >>> Author.objects.first_or_create(name='Firstone')
        (<Author: Firstone>, True)
        >>> Author.objects.first_or_create(name='Firstone')
        (<Author: Firstone>, False)
        """
        # try fetching first record that marches the query
        obj = self.filter(**kwargs).first()
        if obj:
            return obj, False

        # create and return that record
        return self.create(**kwargs), True
