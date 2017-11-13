from __future__ import absolute_import

import mimetypes

from django.http import HttpResponse, FileResponse
from django.views import View

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


class FileResponseView(View):
    def __index__(self, file_path):
        self.file_path = file_path

    def get(self, request):
        content_type, encoding = mimetypes.guess_type(self.file_path)
        f = open(self.file_path, "rb")
        response = FileResponse(f, content_type=content_type)
        if encoding:
            response["Content-Encoding"] = encoding
        return response


class CreateUpdateView(CreateUpdateMixin):
    pass
