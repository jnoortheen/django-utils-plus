def test_unpkg_tag(settings):
    # when DEBUG is false it returns unpkg url
    from utils_plus.templatetags.utils_plus_tags import unpkg
    assert unpkg('bootstrap/dist/js/bootstrap.min.js') == '//unpkg.com/bootstrap@^3.3.7/dist/js/bootstrap.min.js'


def test_unpkg_tag_debug_mode(settings):
    # when DEBUG is true it adds node_modules to statis directory and returns static url
    from utils_plus.templatetags.utils_plus_tags import unpkg
    settings.DEBUG = True
    assert unpkg('bootstrap/dist/js/bootstrap.min.js') == '/static/bootstrap/dist/js/bootstrap.min.js'
    assert 'node_modules' in ''.join(settings.STATICFILES_DIRS)
