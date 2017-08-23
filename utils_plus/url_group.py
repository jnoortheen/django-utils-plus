import warnings

warnings.warn(
    'Usage of utils_plus.url_group.UrlGroup is deprecated. Use utils_plus.router.Url instead',
)
from .router import Url as UrlGroup  # for backward compatiblity
