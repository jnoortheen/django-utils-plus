import os

from django.urls import reverse_lazy

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
    return reverse_lazy(urlname, args=args, kwargs=kwargs)


def app_fixtures(*app_names):
    """
        return all fixture names inside app
    Args:
        *app_name (list):

    Returns:
        list:
    >>> app_fixtures('messaging')
    ['communication.json', 'classcommunication.json', 'mailuser.json', 'mailclass.json', 'communicationuser.json', 'notificationtype.json', 'notification.json', 'mail.json']
    """
    files = []
    for app_name in app_names:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', app_name, 'fixtures'))
        if os.path.exists(path):
            files.extend([i for i in os.listdir(path) if i.endswith('.json')])
    return files