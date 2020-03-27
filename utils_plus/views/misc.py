from __future__ import absolute_import

import mimetypes
from typing import Optional

from django.http import HttpResponse, FileResponse
from django.views import View

from ..mixins import CreateUpdateMixin


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
    file_path: Optional[str] = None

    def get(self, request):
        if not self.file_path:
            raise NotImplementedError("file_path should be filled")
        content_type, encoding = mimetypes.guess_type(self.file_path)
        file = open(self.file_path, "rb")
        response = FileResponse(file, content_type=content_type)
        if encoding:
            response["Content-Encoding"] = encoding
        return response


class CreateUpdateView(CreateUpdateMixin):
    pass
