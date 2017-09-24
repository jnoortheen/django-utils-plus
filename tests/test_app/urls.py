from utils_plus.router import Url
from utils_plus.views import return_path_view

with Url('blog') as u:
    u.slug(return_path_view, 'blog-slug')

urlpatterns = u.urlpatterns
