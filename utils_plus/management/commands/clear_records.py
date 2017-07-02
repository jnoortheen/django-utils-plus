from datetime import timedelta

from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Clear the given model records that are older than a period. The model should have a datetime field."

    def add_arguments(self, parser):
        """

        Args:
            parser (CommandParser):

        Returns:

        """
        parser.add_argument('app_label', type=str, help='Application label', )
        parser.add_argument('model', type=str, help='Name of the model', )
        parser.add_argument('--days', '-d', type=int, default=3, help='Number of days. default: 3', )
        parser.add_argument('--field-name', '-f', type=str, default='created_on',
                            help='Datetime field to filter. Def: created_on', )

    def handle(self, *args, **options):
        model = apps.get_model(options.get('app_label'), options.get('model'))
        kwargs = {
            '{}__lte'.format(options.get('field_name')): timezone.now() - timedelta(days=options.get('days'))
        }
        model.objects.filter(**kwargs).delete()
