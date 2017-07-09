import unittest

from utils_plus.url_group import UrlGroup


def view(request):
    return


class UrlGroupTest(unittest.TestCase):
    def test_nesting_levels(self):
        with UrlGroup('home', view, 'home') as g:
            g('p1', view, 'report')
            g('p2', view, 'report')
            with g('level1', view, 'sub1'):
                g('p1', view, 'level1')
                g('p2', view, 'level1')
                with g('level2', view, 'sub1'):
                    g('p1', view, 'level1')
                    g('p2', view, 'level1')
            g('p3', view, 'report')
        patterns = g.patterns()
        self.assertEqual(next(patterns), '^home/$')
        self.assertEqual(next(patterns), '^home/p1/$')
        self.assertEqual(next(patterns), '^home/p2/$')
        self.assertEqual(next(patterns), '^home/level1/$')
        self.assertEqual(next(patterns), '^home/level1/p1/$')
        self.assertEqual(next(patterns), '^home/level1/p2/$')
        self.assertEqual(next(patterns), '^home/level1/level2/$')
        self.assertEqual(next(patterns), '^home/level1/level2/p1/$')
        self.assertEqual(next(patterns), '^home/level1/level2/p2/$')
        self.assertEqual(next(patterns), '^home/p3/$')

    def test_variable_regex(self):
        with UrlGroup('home', view) as g:
            g.pk(view, 'pk')
            g.int('int_var', view, 'int')
            g.str('str_var', view, 'str')
            g.var('var_k', r'[k]+', view, )
        patterns = g.patterns()
        self.assertEqual(next(patterns), '^home/$')
        self.assertEqual(next(patterns), '^home/(?P<pk>\\d+)/$')
        self.assertEqual(next(patterns), '^home/(?P<int_var>\\d+)/$')
        self.assertEqual(next(patterns), '^home/(?P<str_var>[\\w-]+)/$')
        self.assertEqual(next(patterns), '^home/(?P<var_k>[k]+)/$')

    def test_same_level_urls(self):
        with UrlGroup('home', view) as g:
            g.pk(view, 'pk')
        with g('home2', view):
            g.pk(view, 'pk')
        g('home3', view)

        patterns = g.patterns()
        self.assertEqual(next(patterns), '^home/$')
        self.assertEqual(next(patterns), '^home/(?P<pk>\\d+)/$')
        self.assertEqual(next(patterns), '^home2/$')
        self.assertEqual(next(patterns), '^home2/(?P<pk>\\d+)/$')
        self.assertEqual(next(patterns), '^home3/$')

    def test_paths_without_views(self):
        with UrlGroup('home') as g:
            with g.pk():
                g('edit', view)
            with g.int('integer'):
                g('edit', view)
            with g.str('string'):
                g('edit', view)
            with g.var('variable', r'\.+'):
                g('edit', view)
        with g('home2'):
            g.pk(view, 'pk')
        g('home3', view)
        # for p in g.patterns():
        #     print p, '-'

        patterns = g.patterns()
        self.assertEqual(next(patterns), '^home/(?P<pk>\d+)/edit/$')
        self.assertEqual(next(patterns), '^home/(?P<integer>\d+)/edit/$')
        self.assertEqual(next(patterns), '^home/(?P<string>[\\w-]+)/edit/$')
        self.assertEqual(next(patterns), '^home/(?P<variable>\\.+)/edit/$')
        self.assertEqual(next(patterns), '^home2/(?P<pk>\\d+)/$')
        self.assertEqual(next(patterns), '^home3/$')

    def test_include_patterns_function(self):
        raise NotImplementedError
        # with UrlGroup('home') as g:
        #     with g.pk():
        #         g.incl('edit', 'url_conf_module')
        # with g('home2'):
        #     g.pk(view, 'pk')
        # g('home3', view)
        #
        # for p in g.patterns():
        #     print p, '-'
        #
        # patterns = g.patterns()
        # self.assertEqual(next(patterns), '^home/(?P<pk>\d+)/edit/$')
        # self.assertEqual(next(patterns), '^home2/(?P<pk>\\d+)/$')
        # self.assertEqual(next(patterns), '^home3/$')

    def test_paths_that_starts_with_a_blank_root(self):
        # raise NotImplementedError
        with UrlGroup('', view) as g:
            with g('home'):
                with g.pk():
                    g('edit', view)
                with g.int('integer'):
                    g('edit', view)
            with g('home2'):
                g.pk(view, 'pk')
            g('home3', view)
        patterns = g.patterns()
        self.assertEqual(next(patterns), '^$')
        self.assertEqual(next(patterns), '^home/(?P<pk>\d+)/edit/$')
        self.assertEqual(next(patterns), '^home/(?P<integer>\d+)/edit/$')
        self.assertEqual(next(patterns), '^home2/(?P<pk>\\d+)/$')
        self.assertEqual(next(patterns), '^home3/$')
