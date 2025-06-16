from contextlib import contextmanager

import pytest


@pytest.fixture
def records(db):
    from django_dynamic_fixture import G

    from .test_app.models import Book
    # create three records
    for i in range(3):
        G(Book, authors=3, name='filter')


# copied form the pytest-django as it is not available in PyPI version
@pytest.fixture(scope='function')
def django_assert_num_queries(pytestconfig):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext

    @contextmanager
    def _assert_num_queries(num):
        with CaptureQueriesContext(connection) as context:
            yield
            if num != len(context):
                msg = "Expected to perform %s queries but %s were done" % (num, len(context))
                if pytestconfig.getoption('verbose') > 0:
                    sqls = (q['sql'] for q in context.captured_queries)
                    msg += '\n\nQueries:\n========\n\n%s' % '\n\n'.join(sqls)
                else:
                    msg += " (add -v option to show queries)"
                pytest.fail(msg)

    return _assert_num_queries
