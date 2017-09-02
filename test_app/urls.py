from utils_plus.router import Url
from utils_plus.views import return_path

with Url('blog') as u:
    u.slug(return_path)
