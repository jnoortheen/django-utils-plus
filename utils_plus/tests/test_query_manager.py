from django.test import TestCase

from test_app.models import *


class QueryManagerTest(TestCase):
    def test_first_or_create_function(self):
        assert Author.objects.count() == 0
        Author.objects.first_or_create(name='FirstOne')
        assert Author.objects.count() == 1
        Author.objects.first_or_create(name='FirstOne')
        assert Author.objects.count() == 1
