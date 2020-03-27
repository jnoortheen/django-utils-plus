import os
import sys

from django import template
from django.apps import AppConfig
from django.core.management.base import AppCommand, CommandParser

from utils_plus.utils.misc import read_if_exists

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


def render_template(tmpl: str, **ctx) -> str:
    tmplt = template.Template(tmpl)
    return tmplt.render(template.Context(ctx))


class Command(AppCommand):
    help = "A handy command to create ModelAdmin classes (with import/export resource classes) for Models."

    def add_arguments(self, parser: CommandParser):
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

    def handle_app_config(self, app_config: AppConfig, **options):
        """

        Args:
            app_config (AppConfig):
            **options:

        Returns:

        """
        is_resource_pkg_installed = "import_export" in sys.modules
        resource_file = os.path.join(app_config.path, 'resources.py')
        admin_file = os.path.join(app_config.path, 'admin.py')
        res_file_content = ""
        admin_file_content = ""
        has_resource_class = bool(options.get('resource') and is_resource_pkg_installed)

        for model in app_config.get_models():
            if not options.get('all'):
                if input("Do you want to create for {} ? [y/n]".format(model.__name__)) == 'n':
                    continue

            # check file imports
            if not res_file_content:
                res_file_content = read_if_exists(resource_file)
                # add imports if this is the first time creating this file
                res_file_content += render_template(RES_IMPORT_TEMPLATE, app_name=app_config.name)

            if not admin_file_content:
                admin_file_content = read_if_exists(admin_file)
                if ADMIN_IMPORTS not in admin_file_content:
                    admin_file_content = ADMIN_IMPORTS + admin_file_content

            # add class for a model if it doesn't exist already
            model_class = model.__module__ + '.' + model.__name__
            if model_class not in res_file_content:
                res_file_content += get_resource_cls(model, model_class)
            if model.__name__ not in admin_file_content:
                admin_file_content += get_admin_cls(has_resource_class, model)

        # finaly write file contents
        if has_resource_class:
            with open(resource_file, 'w') as writer:
                writer.write(res_file_content)
        with open(admin_file, 'w') as writer:
            writer.write(admin_file_content)


def get_resource_cls(model, model_class) -> str:
    return render_template(
        RES_CLASS_TEMPLATE,
        model_name=model.__name__,
        model_class=model_class,
    )


def get_admin_cls(has_resource_class: bool, model) -> str:
    tmpl = ADMIN_CLASS_WITH_RES_TEMPLATE if has_resource_class else ADMIN_CLASS_TEMPLATE
    return render_template(
        tmpl,
        model_name=model.__name__
    )
