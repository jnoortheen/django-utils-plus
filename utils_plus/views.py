from __future__ import absolute_import
from django.http import HttpResponse
from .mixins import CreateUpdateMixin


def return_path_view(request, *args, **kwargs):
    """
        utility view for quick test. return the path and arguments as string
    Args:
        request:
        *args:
        **kwargs:

    Returns:
        HttpResponse:
    Usage:
    >>> reqf = getfixture('rf')
    >>> req = reqf.get('/')
    >>> return_path_view(req, 'arg1', 'arg2', kwarg=1).content
    b"Requested / with Args: ('arg1', 'arg2') {'kwarg': 1}"
    """
    return HttpResponse("Requested " + request.path + " with Args: {} {}".format(args, kwargs))


class CreateUpdateView(CreateUpdateMixin):
    pass
