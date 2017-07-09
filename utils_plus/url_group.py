from __future__ import with_statement

from django.conf.urls import include
from django.urls import RegexURLPattern, RegexURLResolver

TRAILING_SLASH_SETTING_NAME = 'URL_GROUP_TRAIL_SLASH'
TRAIL_SLASH = True
try:
    from django.conf import settings

    TRAIL_SLASH = getattr(settings, TRAILING_SLASH_SETTING_NAME, True)
except:
    pass


class UrlGroup(object):
    """
    An elegant and DRY way to define urlpatterns with so many nested levels and syntax sugars.
    It is just a wrapper behind the standard url(), include() methods.

    Usage:

    ### urls.py ###
    from utils_plus.url_group import UrlGroup
    from views import *
    with UrlGroup('editor') as ug:
        with ug.int('doc_pk'):
            ug('edit', DocEditorView.as_view(), 'edit-doc')
            ug('export', DocExporterView.as_view(), 'export-doc')
    ug('docs', Docs.as_view(), 'student-documents')
    ug('publish', DeleteOrPublistDocument.as_view(), 'publish_document', action='publish')
    ug('delete', DeleteOrPublistDocument.as_view(), 'delete_document')

    urlpatterns = ug.urlpatterns

    see url_group_test.py for more use cases
    """
    __constructed = False

    def __init__(self, path, view=None, url_name=None, **kwargs):
        self._paths = []
        self.urlpatterns = []
        self._current_path = None
        self._add_path(view, url_name, path, kwargs)

    def __call__(self, path, view=None, url_name=None, **kwargs):
        self.__constructed = True
        self._add_path(view, url_name, path, kwargs)
        return self

    def __iter__(self):
        for p in self.urlpatterns:
            yield p

    def _add_path(self, view, url_name, path, kwargs):
        """
            adds a new URL to urlpatterns
        Args:
            view (func): it is a callable function typically a django view
            url_name (str):
            path (str): the string part between the slashes.
                Ex. url('^add/$', cls.as_view(), name='add'), here the whole ^add is the path
            kwargs (dict): dict that is passed on to the view
        """
        self._paths.append(path)
        if view: self._add_url(view, url_name, kwargs)
        self._last_path = self._paths.pop()

    def _add_url(self, view, url_name, kwargs):
        """
            adds a new URL to urlpatterns
        Args:
            view (func): it is a callable function typically a django view
            url_name (str):
            kwargs (dict): dict that is passed on to the view
        """
        paths = '/'.join(p for p in self._paths if p)
        path = '^' + paths + '{}$'.format('/' if TRAIL_SLASH and paths else '')
        self.urlpatterns.append(RegexURLPattern(path, view, kwargs, name=url_name))

    def incl(self, path, module, namespace=None, **kwargs):
        """
            This is simply a wrapper around the standard include method.

            # original
            urlpatterns = [
                url(r'^document/', include('document.urls')),
                url(r'^core/', include('core.urls', namespace='core'), {'kwarg1':'kwval1', }),
            ]
            into this

            # using UrlGroup
            u = UrlGroup('')
            u.incl('document', 'document.urls')
            u.incl('core', 'core.urls', 'core', kwarg1='kwval1', )
            urlpatterns = u.urlpatterns
        Args:
            path (str): path that the module urls appended to
            module (str, list): module denoted as string or a list of urls
            namespace (str): namespace for the included urls
        """
        self._add_path(None, '', path, {})
        regex = '^' + '/'.join(self._paths) + '/'
        urlconf_module, app_name, namespace = include(module, namespace=namespace)
        self.urlpatterns.append(RegexURLResolver(regex, urlconf_module, kwargs, app_name, namespace))

    def patterns(self):
        for p in self.urlpatterns:
            yield p.regex.pattern

    def var(self, var_name, regex, view=None, url_name=None, **kwargs):
        """
            add a variable to the urlpatterns
        Args:
            view (func): callable function
            var_name (str): name of the variable
            regex (str): regex pattern. Ex. r'\d+', r'[\w-]+'
            url_name (str): url name
            **kwargs: this dic will be passed to the view as kwargs
        """
        return self.__call__(r'(?P<{}>{})'.format(var_name, regex), view, url_name, **kwargs)

    def int(self, var_name, view=None, url_name=None, **kwargs):
        """
        a wrapper around `self.var` method for integers
        Args:
            var_name (str):
            view (func):
            url_name (str):
            **kwargs:

        Returns:
            UrlGroup: self updated
        """
        return self.var(var_name, r'\d+', view, url_name, **kwargs)

    def pk(self, view=None, url_name=None, **kwargs):
        """
        a wrapper around `self.var` method for integers
        Args:
            view (func):
            url_name (str):
            **kwargs:

        Returns:
            UrlGroup:
        """
        return self.int('pk', view, url_name, **kwargs)

    def str(self, var_name, view=None, url_name=None, **kwargs):
        """
        a wrapper around `self.var` method for url-slug. It will match any words without space
        Args:
            var_name (str):
            view (func):
            url_name (str):
            **kwargs:

        Returns:
            UrlGroup: self updated
        """
        return self.var(var_name, r'[\w-]+', view, url_name, **kwargs)

    # with context manger methods
    def __enter__(self):
        self._paths.append(self._last_path)
        if not self.__constructed:
            return self

    def __exit__(self, *args):
        self._paths.pop()
