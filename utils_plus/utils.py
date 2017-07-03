import os

import django.urls
import django.apps

IP_ADDRESS_HEADERS = ('HTTP_X_REAL_IP', 'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR')


def get_ip_address(request):
    for header in IP_ADDRESS_HEADERS:
        addr = request.META.get(header)
        if addr:
            return addr.split(',')[0].strip()


def reverse_url(urlname, *args, **kwargs):
    """
        utility method to wrap arguments & kwargs passed to reverse_lazy for url construction elegantly
    Args:
        urlname (str):
        *args:
        **kwargs:

    Returns:
        str: reverse matched URL path
    """
    return django.urls.reverse_lazy(urlname, args=args, kwargs=kwargs)


def app_fixtures(*app_names):
    """
        return all fixture names inside app
    Args:
        *app_name (list):

    Returns:
        list:
    Usage:
    >>> app_fixtures('test_app')
    ['communication.json', 'classcommunication.json', ]
    """
    files = []
    for app_name in app_names:
        config = django.apps.apps.get_app_config(app_name)
        path = os.path.abspath(os.path.join(config.path, 'fixtures'))
        if os.path.exists(path):
            files.extend([i for i in os.listdir(path) if i.endswith('.json')])
    return files
