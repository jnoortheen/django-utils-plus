from utils_plus.router import Url
from utils_plus.views import return_path_view as view


def test_nesting_levels():
    with Url('home', view, 'home') as g:
        g('p1', view, 'report')
        g('p2', view, 'report')
        with g('level1', view, 'sub1'):
            g('p1', view, 'level1')
            g('p2', view, 'level1')
            with g('level2', view, 'sub1'):
                g('p1', view, 'level1')
                g('p2', view, 'level1')
        g('p3', view, 'report')
    assert list(g.patterns()) == [
        '^home/$',
        '^home/p1/$',
        '^home/p2/$',
        '^home/level1/$',
        '^home/level1/p1/$',
        '^home/level1/p2/$',
        '^home/level1/level2/$',
        '^home/level1/level2/p1/$',
        '^home/level1/level2/p2/$',
        '^home/p3/$',
    ]
    assert len(list(g)) == 10


def test_variable_regex():
    with Url('home', view) as g:
        g.pk(view, 'pk')
        g.int('int_var', view, 'int')
        g.str('str_var', view, 'str')
        g.var('var_k', r'[k]+', view, )
    assert list(g.patterns()) == [
        '^home/$',
        '^home/(?P<pk>\\d+)/$',
        '^home/(?P<int_var>\\d+)/$',
        '^home/(?P<str_var>[\\w-]+)/$',
        '^home/(?P<var_k>[k]+)/$',
    ]


def test_same_level_urls():
    with Url('home', view) as g:
        g.pk(view, 'pk')
    with g('home2', view):
        g.pk(view, 'pk')
    g('home3', view)

    assert list(g.patterns()) == [
        '^home/$',
        '^home/(?P<pk>\\d+)/$',
        '^home2/$',
        '^home2/(?P<pk>\\d+)/$',
        '^home3/$',
    ]


def test_paths_without_views():
    with Url('home') as g:
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

    assert list(g.patterns()) == [
        '^home/(?P<pk>\d+)/edit/$',
        '^home/(?P<integer>\d+)/edit/$',
        '^home/(?P<string>[\\w-]+)/edit/$',
        '^home/(?P<variable>\\.+)/edit/$',
        '^home2/(?P<pk>\\d+)/$',
        '^home3/$',
    ]


def test_include_patterns_function():
    # app1 urls
    with Url('app2') as g:
        with g('post'):
            with g.pk(view):
                g('edit', view)
    # app1 urls
    with Url('app1') as u:
        with u('post'):
            with u.pk(view):
                u('edit', view)
    # root url definition
    with Url('app') as root:
        root.incl(u, prefix='app1')
        root.incl(g, prefix='app2')

    assert list(root.patterns()) == [
        '^app/app1/^app1/post/(?P<pk>\d+)/$',
        '^app/app1/^app1/post/(?P<pk>\d+)/edit/$',
        '^app/app2/^app2/post/(?P<pk>\d+)/$',
        '^app/app2/^app2/post/(?P<pk>\d+)/edit/$',
    ]


def test_paths_that_starts_with_a_blank_root():
    with Url('', view) as g:
        with g('home'):
            with g.pk():
                g('edit', view)
            with g.int('integer'):
                g('edit', view)
        with g('home2'):
            g.pk(view, 'pk')
        g('home3', view)
    assert list(g.patterns()) == [
        '^$',
        '^home/(?P<pk>\d+)/edit/$',
        '^home/(?P<integer>\d+)/edit/$',
        '^home2/(?P<pk>\\d+)/$',
        '^home3/$',
    ]


def test_multi_part_single_entry():
    with Url('nest1/nest2', view) as g:
        with g('home/coming'):
            with g.pk():
                g('edit', view)
            with g.int('integer'):
                g('edit', view)
        with g('first/nest3'):
            g.pk(view, 'pk')
        g('home3', view)

    assert list(g.patterns()) == [
        '^nest1/nest2/$',
        '^nest1/nest2/home/coming/(?P<pk>\d+)/edit/$',
        '^nest1/nest2/home/coming/(?P<integer>\d+)/edit/$',
        '^nest1/nest2/first/nest3/(?P<pk>\d+)/$',
        '^nest1/nest2/home3/$',
    ]
