from tests.test_app.models import Author
from utils_plus.views import CreateUpdateView


class CreateUpdateAuthorView(CreateUpdateView):
    model = Author
