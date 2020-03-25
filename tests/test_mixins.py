from unittest.mock import Mock

from django.urls import reverse
from django.views import View

from utils_plus.mixins import ContextMixinPlus, CreateUpdateMixin, ProcessFormView


def test_generic_view():
    class GenricView(ContextMixinPlus, View):
        three = 0
        four = 0
        kwargs = {'one': 1, 'two': 2}

    view = GenricView()
    assert set(view.get_context_data(six=6, five=5).keys()) == {'six', 'five', 'view', 'one', 'two'}


class test_CreateUpdateMixin:
    def test_get(self, monkeypatch):
        c = CreateUpdateMixin()
        monkeypatch.setattr(c, "get_object", Mock())
        monkeypatch.setattr(ProcessFormView, "get", Mock())
        c.get(request='')
        c.get_object.assert_called_once()

    def test_post(self, monkeypatch):
        c = CreateUpdateMixin()
        monkeypatch.setattr(c, "get_object", Mock())
        monkeypatch.setattr(ProcessFormView, "post", Mock())
        c.post(request='', pk=1)
        c.get_object.assert_called_once()

    def test_urls(self):
        # the urls are defined in test-app
        assert reverse('author:add') == '/blog/author_profile/add/'
        assert reverse('author:edit', args=[12]) == '/blog/author_profile/edit/12/'
