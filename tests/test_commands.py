from django import apps
from django.core.management import call_command


def test_clear_records(records):
    from .test_app.models import Book
    assert Book.objects.count() == 3
    call_command('clear_records', 'test_app', 'book', days=0)
    assert Book.objects.count() == 0


def test_cleardata(records):
    for model in apps.apps.get_app_config('test_app').models.values():
        assert model.objects.count() > 0

    call_command('cleardata', 'test_app')

    for model in apps.apps.get_app_config('test_app').models.values():
        assert model.objects.count() == 0


def test_test_mail_command(mailoutbox):
    call_command('test_mail', to='test@mail.com')
    assert len(mailoutbox) == 1
    m = mailoutbox[0]
    assert list(m.to) == ['test@mail.com']
