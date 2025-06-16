from utils_plus.router import url
from utils_plus.views import return_path_view

from .views import CreateUpdateAuthorView

urlpatterns = list(
    url('blog')[
        url.slug(view=return_path_view, name='blog-slug'),
        url("author")[
            CreateUpdateAuthorView.urls(name_prefix='author')
        ],
    ]
)
