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
    return os.path.join(os.path.abspath(os.path.dirname(__name__)), 'node_modules')


NODE_PKGS = {}


def get_node_pkgs_path():
    from django.conf import settings
    root = getattr(settings, 'NODE_PKG_DIR', os.path.abspath(os.path.dirname(__name__)))
    return os.path.join(root, 'package.json')


def load_node_pkgs():
    """read and parse package.json"""
    # todo: handle file not being found
    import codecs
    with codecs.open(get_node_pkgs_path(), 'r', 'utf-8') as f:
        pkg_json = json.loads(f.read())
        NODE_PKGS.update(pkg_json.get('dependencies', {}))
        NODE_PKGS.update(pkg_json.get('devDependencies', {}))


def get_node_pkg_version(pkg):
    if not NODE_PKGS:
        load_node_pkgs()
    return NODE_PKGS.get(pkg, '')


def get_unpkg_url(path):
    """

    Args:
        path (str):

    Returns:
        str:


    """
    path = path.lstrip('/')
    pkg_name, filepath = path.split('/', 1)
    pkg_version = get_node_pkg_version(pkg_name)
    return '//unpkg.com/{pkg_name}@{pkg_version}/{filepath}'.format(**locals())
