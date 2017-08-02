from django.core.management.base import AppCommand


class Command(AppCommand):
    help = "Warning! Irreversible action. Clear all the models for the given app."

    def handle_app_config(self, app_config, **options):
        for model in app_config.get_models():
            model.objects.all().delete()
