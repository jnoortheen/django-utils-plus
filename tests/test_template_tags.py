from utils_plus.templatetags.utils_plus_tags import (
    jsdelivr_combine_css,
    jsdelivr_combine_js,
    unpkg,
)


def test_jsdelivr_combine_js(settings):
    # when DEBUG is false it returns unpkg url
    assert jsdelivr_combine_js(
        'bootstrap/dist/js/bootstrap.min.js',
        'jquery/dist/jquery.min.js'
    ) == """<script src="//cdn.jsdelivr.net/combine//npm/bootstrap@3.4.1/dist/js/bootstrap.min.js,npm/jquery@3.5.0/dist/jquery.min.js"></script>"""


def test_jsdelivr_combine_css(settings):
    # when DEBUG is false it returns unpkg url
    assert jsdelivr_combine_css(
        'bootstrap/dist/css/bootstrap.min.css',
        'malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.css'
    ) == """<link href="//cdn.jsdelivr.net/combine//npm/bootstrap@3.4.1/dist/css/bootstrap.min.css,npm/malihu-custom-scrollbar-plugin@3.1.5/jquery.mCustomScrollbar.css" rel="stylesheet" type="text/css"/>"""


def test_jsdelivr_combine_js_debug_mode(settings):
    # when DEBUG is false it returns unpkg url
    settings.DEBUG = True
    assert jsdelivr_combine_js(
        'bootstrap/dist/js/bootstrap.min.js',
        'jquery/dist/jquery.min.js'
    ) == """<script src="/static/bootstrap/dist/js/bootstrap.min.js"></script><script src="/static/jquery/dist/jquery.min.js"></script>"""


def test_unpkg_tag(settings):
    # when DEBUG is false it returns unpkg url
    assert unpkg('bootstrap/dist/js/bootstrap.min.js') == '//unpkg.com/bootstrap@3.4.1/dist/js/bootstrap.min.js'


def test_unpkg_tag_debug_mode(settings):
    # when DEBUG is true it adds node_modules to statis directory and returns static url
    settings.DEBUG = True
    assert unpkg('bootstrap/dist/js/bootstrap.min.js') == '/static/bootstrap/dist/js/bootstrap.min.js'
    assert 'node_modules' in ''.join(settings.STATICFILES_DIRS)
