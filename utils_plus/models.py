# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from django.db import models


class QueryManager(models.Manager):
    """
        A DRYer way to set select_related, prefetch_related & filters to queryset
    """
    _args = ()
    _kwargs = {}

    def __init__(self, *args, **kwargs):
        """
            any arguments that you would pass on to filter
        """
        self._args = args
        self._kwargs = kwargs
        self._queryset_methods = OrderedDict()
        super(QueryManager, self).__init__()

    def _save_args(self, name, args):
        """

        Args:
            name (str): name of queryset method like select_related, etc.,
            args (tuple): list of arguments

        Returns:
            QueryManager:
        """
        self._queryset_methods[name] = args
        return self

    def prefetches(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's prefetch
        Returns:
            QueryManager:
        """
        return self._save_args('prefetch_related', args)

    def selects(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's select_related
        Returns:
            QueryManager:
        """
        return self._save_args('select_related', args)

    def values(self, *args):
        return self._save_args('values', args)

    def only(self, *args):
        return self._save_args('only', args)

    def order_by(self, *args):
        """

        Args:
            *args: this will be passed onto queryset's select_related

        Returns:
            QueryManager:
        """
        return self._save_args('order_by', args)

    def get_queryset(self):
        """

        Returns:
            models.QuerySet:
        """
        qs = super(QueryManager, self).get_queryset().filter(*self._args, **self._kwargs)  # type: models.QuerySet

        for method_name in self._queryset_methods:
            qs = getattr(qs, method_name)(*self._queryset_methods[method_name])

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
