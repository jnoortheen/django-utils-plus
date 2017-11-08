from collections import OrderedDict


def test_queryset_manager_filters(records):
    from tests.test_app.models import Book
    assert str(
        Book.objects.filter(
            name__icontains='filter'
        ).select_related('publisher').prefetch_related('authors').order_by('-id').query
    ) == str(Book.rel_objects.all().query)


def test_is_deletable_mixin(records):
    from tests.test_app.models import Author
    auth = Author.objects.first()
    deletable, books = auth.is_deletable()
    assert not deletable
    assert books.count() == 1


def test_choices_enum_field(records):
    from tests.test_app.models import Author
    from utils_plus.choices import ChoicesEnum

    author = Author.objects.first()
    assert isinstance(author.title, ChoicesEnum)


def test_querymanager():
    from utils_plus.models import QueryManager
    objects = (QueryManager()
        .selects('fk_field', 'rel_model_field')
        .prefetches('m2m_field', 'rel_model_field')
        .only('field1', 'field2')
        .values('field1', 'field2')
        .order_by('-id', '-field_name')
        )

    assert objects._queryset_methods == OrderedDict(
        [('select_related', ('fk_field', 'rel_model_field')),
         ('prefetch_related', ('m2m_field', 'rel_model_field')),
         ('only', ('field1', 'field2')),
         ('values', ('field1', 'field2')),
         ('order_by', ('-id', '-field_name'))])
