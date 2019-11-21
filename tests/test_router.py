from utils_plus.router import u
from utils_plus.views import return_path_view as view


def test_nesting_levels():
    urls = u("home")[
        u("p1", view, "report"),
        u("p2", view, "report"),
        u("level1", view, "sub1")[
            u("p1", view, "level1"),
            u("p2", view, "level1"),
            u("level2", view, "sub1")[
                u("p1", view, "level1"), u("p2", view, "level1"),
            ],
        ],
        u("p3", view, "report"),
    ]

    assert urls == [
        r"^home/$",
        r"^home/p1/$",
        r"^home/p2/$",
        r"^home/level1/$",
        r"^home/level1/p1/$",
        r"^home/level1/p2/$",
        r"^home/level1/level2/$",
        r"^home/level1/level2/p1/$",
        r"^home/level1/level2/p2/$",
        r"^home/p3/$",
    ]
    assert len(list(g)) == 10


def test_variable_regex():
    with Url("home", view) as g:
        g.pk(view, "pk")
        g.int("int_var", view, "int")
        g.str("str_var", view, "str")
        g.var(
            "var_k", r"[k]+", view,
        )
    assert list(g.patterns()) == [
        r"^home/$",
        r"^home/(?P<pk>\\d+)/$",
        r"^home/(?P<int_var>\\d+)/$",
        r"^home/(?P<str_var>[\\w-]+)/$",
        r"^home/(?P<var_k>[k]+)/$",
    ]


def test_same_level_urls():
    with Url("home", view) as g:
        g.pk(view, "pk")
    with g("home2", view):
        g.pk(view, "pk")
    g("home3", view)

    assert list(g.patterns()) == [
        r"^home/$",
        r"^home/(?P<pk>\\d+)/$",
        r"^home2/$",
        r"^home2/(?P<pk>\\d+)/$",
        r"^home3/$",
    ]


def test_paths_without_views():
    with Url("home") as g:
        with g.pk():
            g("edit", view)
        with g.int("integer"):
            g("edit", view)
        with g.str("string"):
            g("edit", view)
        with g.var("variable", r"\.+"):
            g("edit", view)
    with g("home2"):
        g.pk(view, "pk")
    g("home3", view)
    # for p in g.patterns():
    #     print p, '-'

    assert list(g.patterns()) == [
        r"^home/(?P<pk>\d+)/edit/$",
        r"^home/(?P<integer>\d+)/edit/$",
        r"^home/(?P<string>[\\w-]+)/edit/$",
        r"^home/(?P<variable>\\.+)/edit/$",
        r"^home2/(?P<pk>\\d+)/$",
        r"^home3/$",
    ]


def test_include_patterns_function():
    # app1 urls
    with Url("app2") as g:
        with g("post"):
            with g.pk(view):
                g("edit", view)
    # app1 urls
    with Url("app1") as u:
        with u("post"):
            with u.pk(view):
                u("edit", view)
    # root url definition
    with Url("app") as root:
        root.incl(u, prefix="app1")
        root.incl(g, prefix="app2")

    assert list(root.patterns()) == [
        r"^app/app1/^app1/post/(?P<pk>\d+)/$",
        r"^app/app1/^app1/post/(?P<pk>\d+)/edit/$",
        r"^app/app2/^app2/post/(?P<pk>\d+)/$",
        r"^app/app2/^app2/post/(?P<pk>\d+)/edit/$",
    ]


def test_paths_that_starts_with_a_blank_root():
    with Url("", view) as g:
        with g("home"):
            with g.pk():
                g("edit", view)
            with g.int("integer"):
                g("edit", view)
        with g("home2"):
            g.pk(view, "pk")
        g("home3", view)
    assert list(g.patterns()) == [
        r"^$",
        r"^home/(?P<pk>\d+)/edit/$",
        r"^home/(?P<integer>\d+)/edit/$",
        r"^home2/(?P<pk>\\d+)/$",
        r"^home3/$",
    ]


def test_multi_part_single_entry():
    with Url("nest1/nest2", view) as g:
        with g("home/coming"):
            with g.pk():
                g("edit", view)
            with g.int("integer"):
                g("edit", view)
        with g("first/nest3"):
            g.pk(view, "pk")
        g("home3", view)

    assert list(g.patterns()) == [
        r"^nest1/nest2/$",
        r"^nest1/nest2/home/coming/(?P<pk>\d+)/edit/$",
        r"^nest1/nest2/home/coming/(?P<integer>\d+)/edit/$",
        r"^nest1/nest2/first/nest3/(?P<pk>\d+)/$",
        r"^nest1/nest2/home3/$",
    ]
