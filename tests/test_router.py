from utils_plus.router import url
from utils_plus.views import return_path_view as view


def str_iter(x):
    return list(map(str, x))


def test_nesting_levels():
    urls = list(
        url("home")[
            url("p1", view, "report1"),
            url("p2", view, "report2"),
            url("level1", view, "sub1")[
                url("p1", view, "level1"),
                url("p2", view, "level2"),
                url("level2", view, "sub2")[url("p1", view, "lp1"), url("p2", view, "lp2")],
            ],
            url("p3", view, "report3"),
        ]
    )

    assert str_iter(urls) == [
        "<URLPattern 'home/p1/' [name='report1']>",
        "<URLPattern 'home/p2/' [name='report2']>",
        "<URLPattern 'home/level1/' [name='sub1']>",
        "<URLPattern 'home/level1/p1/' [name='level1']>",
        "<URLPattern 'home/level1/p2/' [name='level2']>",
        "<URLPattern 'home/level1/level2/' [name='sub2']>",
        "<URLPattern 'home/level1/level2/p1/' [name='lp1']>",
        "<URLPattern 'home/level1/level2/p2/' [name='lp2']>",
        "<URLPattern 'home/p3/' [name='report3']>",
    ]
    assert len(urls) == 9


def test_variable_regex():
    g = url("home")[
        url.pk(view, "pk"),
        url.int("int_var", view, "int"),
        url.var("str_var", view, "str"),
        url.re("reg_x", r"[x]+", view, "regex"),
    ]
    assert str_iter(g) == [
        "<URLPattern 'home/<int:pk>/' [name='pk']>",
        "<URLPattern 'home/<int:int_var>/' [name='int']>",
        "<URLPattern 'home/<str_var>/' [name='str']>",
        "<URLPattern 'home/(?P<reg_x>[x]+)/' [name='regex']>",
    ]


def test_same_level_urls():
    g = url("home", view)[
            url.pk(view)
        ] + url("about", view)[
            url.pk(view)[
                url("pdf", view)
            ]
        ] + url("contact", view)[
            url.pk(view)
        ]
    assert str_iter(g) == ["<URLPattern 'home/'>",
                           "<URLPattern 'home/<int:pk>/'>",
                           "<URLPattern 'about/'>",
                           "<URLPattern 'about/<int:pk>/'>",
                           "<URLPattern 'about/<int:pk>/pdf/'>",
                           "<URLPattern 'contact/'>",
                           "<URLPattern 'contact/<int:pk>/'>"]


def test_paths_without_views():
    g = url("home")[
        url.pk()[url("edit", view)],
        url.int("integer")[url("edit", view)],
        url.var("variable")[url("edit", view)],
        url.re("regex", r"\.+")[url("edit", view)],
        url("home2")[url.pk(view, "pk")],
        url("home3", view),
    ]

    assert str_iter(g) == [
        "<URLPattern 'home/<int:pk>/edit/'>",
        "<URLPattern 'home/<int:integer>/edit/'>",
        "<URLPattern 'home/<variable>/edit/'>",
        "<URLPattern 'home/(?P<regex>\\.+)/edit/'>",
        "<URLPattern 'home/home2/<int:pk>/' [name='pk']>",
        "<URLPattern 'home/home3/'>",
    ]


def test_include_patterns():
    # app1 urls
    app2 = url("app2/")[url("post")[url.pk(view)[url("edit", view)]]]
    # app1 urls
    app1 = url("app1/")[url("post")[url.pk(view)[url("edit", view)]]]
    # root url definition
    app = url("app/")[app1, app2]
    assert str_iter(app) == [
        "<URLPattern 'app/app1/post/<int:pk>/'>",
        "<URLPattern 'app/app1/post/<int:pk>/edit/'>",
        "<URLPattern 'app/app2/post/<int:pk>/'>",
        "<URLPattern 'app/app2/post/<int:pk>/edit/'>",
    ]


def test_paths_that_starts_with_a_blank_root():
    g = url("", view)[
        url("home")[url.pk()[url("edit", view)], url.int("integer")[url("edit", view)]],
        url("home2")[url.pk(view, "pk")],
        url("home3", view),
    ]
    assert str_iter(g) == [
        "<URLPattern ''>",
        "<URLPattern 'home/<int:pk>/edit/'>",
        "<URLPattern 'home/<int:integer>/edit/'>",
        "<URLPattern 'home2/<int:pk>/' [name='pk']>",
        "<URLPattern 'home3/'>"
    ]


def test_multi_part_single_entry():
    g = url("nest1/nest2", view)[
        url("home/coming")[
            url.pk()[
                url("edit", view)
            ],
            url.int("integer")[
                url("edit", view),
            ],
        ],
        url("first/nest3")[
            url.pk(view, "pk")
        ],
        url("home3", view),
    ]

    assert str_iter(g) == [
        "<URLPattern 'nest1/nest2/'>",
        "<URLPattern 'nest1/nest2/home/coming/<int:pk>/edit/'>",
        "<URLPattern 'nest1/nest2/home/coming/<int:integer>/edit/'>",
        "<URLPattern 'nest1/nest2/first/nest3/<int:pk>/' [name='pk']>",
        "<URLPattern 'nest1/nest2/home3/'>"
    ]
