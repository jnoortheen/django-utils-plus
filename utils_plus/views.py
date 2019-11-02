from django.views.generic import UpdateView


class CreateUpdateView(UpdateView):

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None
