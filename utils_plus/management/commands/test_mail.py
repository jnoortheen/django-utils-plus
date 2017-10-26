from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = "Test sending mail from django."

    def add_arguments(self, parser):
        """

        Args:
            parser (CommandParser):

        Returns:

        """
        parser.add_argument(
            '-to', type=str, default='',
            help='To email ID e.g. person@testmail.com. Default will be the settings.MANGERS if not given',
        )

    def handle(self, *args, **options):
        to_email = options.get('to') or settings.MANAGERS[0][1]
        send_mail("It works!", "Test email plain text content", settings.DEFAULT_FROM_EMAIL, [to_email])
