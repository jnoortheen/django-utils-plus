import os

from django import template
from django.core.management.base import AppCommand

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
        content = ""
        mware_name = "{}_middleware".format(options['name'])

        if os.path.exists(file):
            with open(file) as f: content = f.read()

        if mware_name not in content:
            t = template.Template(CLASS_TMPL)
            content += t.render(template.Context(dict(name=mware_name)))

        # finaly write file contents
        if content:
            with open(file, 'w') as f: f.write(content)
