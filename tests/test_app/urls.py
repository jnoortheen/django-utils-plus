from utils_plus.router import Url
from utils_plus.views import return_path_view
from .views import CreateUpdateAuthorView

with Url('blog') as u:
    u.slug(return_path_view, 'blog-slug')
    u.incl(CreateUpdateAuthorView.urls(), namespace='author', prefix='author_profile')

urlpatterns = u.urlpatterns
