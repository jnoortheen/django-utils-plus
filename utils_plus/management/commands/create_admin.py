import os

from django import template
from django.apps import AppConfig
from django.core.management.base import AppCommand, CommandParser

RES_IMPORT_TEMPLATE = """\
from import_export.resources import ModelResource
import {{ app_name }}.models

"""
RES_CLASS_TEMPLATE = """\

class {{ model_name }}Resource(ModelResource):
    class Meta:
        model = {{ model_class }}

"""
ADMIN_IMPORTS = """\
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import *
"""
ADMIN_CLASS_WITH_RES_TEMPLATE = """\

@admin.register({{ model_name }})
class {{ model_name }}Admin(ImportExportModelAdmin):
    resource_class = {{ model_name }}Resource

"""

ADMIN_CLASS_TEMPLATE = """\

@admin.register({{ model_name }})
class {{ model_name }}Admin(admin.ModelAdmin):
    pass

"""


class Command(AppCommand):
    help = "A handy command to create ModelAdmin classes (with import/export resource classes) for Models."

    def add_arguments(self, parser):
        """

        Args:
            parser (CommandParser):

        Returns:

        """
        super(Command, self).add_arguments(parser)
        parser.add_argument('--all', '-a', dest='all', default=False,
                            help='Create admin classes for all of the models in app')
        parser.add_argument('-r', dest='resource', default=True, type=bool,
                            help='Create resource classes too')

    def handle_app_config(self, app_config, **options):
        """

        Args:
            app_config (AppConfig):
            **options:

        Returns:

        """
        is_resource_pkg_installed = False
        try:
            import import_export.resources
            is_resource_pkg_installed = True
        except:
            pass

        resource_file = os.path.join(app_config.path, 'resources.py')
        admin_file = os.path.join(app_config.path, 'admin.py')
        res_file_content = ""
        admin_file_content = ""
        has_resource_class = options.get('resource') and is_resource_pkg_installed

        for model in app_config.get_models():
            if not options.get('all'):
                if input("Do you want to create for {} ? [y/n]".format(model.__name__)) == 'n':
                    continue

            # check file imports
            if not res_file_content:
                if os.path.exists(resource_file):
                    with open(resource_file) as f: res_file_content = f.read()
            if not admin_file_content:
                if os.path.exists(admin_file):
                    with open(admin_file) as f: admin_file_content = f.read()
                if ADMIN_IMPORTS not in admin_file_content:
                    admin_file_content = ADMIN_IMPORTS + admin_file_content

            # add imports if this is the first time creating this file
            if not res_file_content:
                t = template.Template(RES_IMPORT_TEMPLATE)
                res_file_content += t.render(template.Context(dict(app_name=app_config.name)))

            # add class for a model if it doesn't exist already
            model_class = model.__module__ + '.' + model.__name__
            if model_class not in res_file_content:
                t = template.Template(RES_CLASS_TEMPLATE)
                res_file_content += t.render(
                    template.Context(
                        dict(
                            model_name=model.__name__,
                            model_class=model_class,
                        )
                    )
                )
            if model.__name__ not in admin_file_content:
                tmpl = ADMIN_CLASS_WITH_RES_TEMPLATE if has_resource_class else ADMIN_CLASS_TEMPLATE
                t = template.Template(tmpl)
                admin_file_content += t.render(
                    template.Context(
                        dict(
                            model_name=model.__name__
                        )
                    )
                )

        # finaly write file contents

        if has_resource_class:
            with open(resource_file, 'w') as f:
                f.write(res_file_content)

        with open(admin_file, 'w') as f:
            f.write(admin_file_content)
