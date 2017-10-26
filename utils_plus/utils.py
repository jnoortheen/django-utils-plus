import os

import json

IP_ADDRESS_HEADERS = ('HTTP_X_REAL_IP', 'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR')


def get_ip_address(request):
    """
        return ip address from any of the possible header address
    Args:
        request:

    Returns:
        str: ip address

    Usage:
    >>> reqf = getfixture('rf')
    >>> req = reqf.get('/')
    >>> get_ip_address(req)
    '127.0.0.1'
    """
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
    >>> reverse_url('blog-slug', 'slug-title')
    '/blog/slug-title/'
    """
    from django.urls import reverse_lazy
    return reverse_lazy(urlname, args=args, kwargs=kwargs)


def app_fixtures(*app_names):
    """
        return all fixture names inside app
    Args:
        *app_name (list):

    Returns:
        list:
    Usage:
    >>> app_fixtures('test_app')
    ['fixture_2.json', 'fixture_1.json']
    """
    from django.apps import apps
    import os

    files = []
    for app_name in app_names:
        config = apps.get_app_config(app_name)
        path = os.path.abspath(os.path.join(config.path, 'fixtures'))
        if os.path.exists(path):
            files.extend([i for i in os.listdir(path) if i.endswith('.json')])
    return files


def get_node_modules_dir():
    os.path.join(os.path.abspath(os.path.dirname(__name__)), 'node_modules')


NODE_PKGS = json.load(os.path.join(os.path.abspath(os.path.dirname(__name__)), 'package.json'))


def get_node_pkg_version(pkg):
    return (
        NODE_PKGS['dependencies'][pkg]
        if 'dependencies' in NODE_PKGS and pkg in NODE_PKGS['dependencies']
        else NODE_PKGS['devDependencies'][pkg]
        if 'devDependencies' in NODE_PKGS and pkg in NODE_PKGS['devDependencies']
        else ''
    )


def get_unpkg_url(path):
    path = path.lstrip('/')
    pkg_name, filepath = path.split('/', 1)
    pkg_version = get_node_pkg_version(pkg_name)
    return '//unpkg.com/{pkg_name}@{pkg_version}/{filepath}'.format(**locals())
