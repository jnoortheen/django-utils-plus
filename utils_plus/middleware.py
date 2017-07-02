from django.conf import settings
from django.contrib.auth.decorators import login_required
import re

LOGIN_REQ_URLS = []
if hasattr(settings, 'LOGIN_REQUIRED_URLS'):
    LOGIN_REQ_URLS += [re.compile(expr) for expr in settings.LOGIN_REQUIRED_URLS]


def login_required_middleware(get_response):
    """
       settings.LOGIN_REQ_URLS holds a list of ``re`` patterns. Those request are wrapped with login_required decorator
    This is extremely useful when you don't have to litter your code with lots of decorators and checks
    Args:
        get_response:

    Returns:

    """
    def middleware(request):
        if any(m.match(request.path) for m in LOGIN_REQ_URLS):
            return login_required(get_response)(request)
        return get_response(request)

    return middleware
