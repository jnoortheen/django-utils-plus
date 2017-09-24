def test_queryset_manager_filters(records):
    from tests.test_app.models import Book
    assert str(
        Book.objects.filter(
            name__icontains='filter'
        ).select_related('publisher').prefetch_related('authors').order_by('-id').query
    ) == str(Book.rel_objects.all().query)
