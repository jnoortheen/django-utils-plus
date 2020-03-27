import os

from django.core.management.base import AppCommand

from utils_plus.utils.misc import read_if_exists
from .create_admin import render_template

CLASS_TMPL = """\

def {{name}}(get_response):
    def middleware(request):
        # do your processing here
        return get_response(request)
    return middleware

"""


class Command(AppCommand):
    help = "Create new middleware"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-n', '--name', type=str, help='Name of the middeware', default='sample')

    def handle_app_config(self, app_config, **options):
        file = os.path.join(app_config.path, 'middleware.py')
        content = read_if_exists(file)
        mware_name = "{}_middleware".format(options['name'])

        if mware_name not in content:
            content += render_template(CLASS_TMPL, name=mware_name)

        # finaly write file contents
        if content:
            with open(file, 'w') as writer:
                writer.write(content)
