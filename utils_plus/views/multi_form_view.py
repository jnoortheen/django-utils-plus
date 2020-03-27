from typing import Dict, Any, Type, TYPE_CHECKING, List

from django.forms.forms import Form
from django.http import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.edit import ProcessFormView

FormClsTypes = Dict[str, Type[Form]]
FormTypes = Dict[str, Form]

CLS = object
if TYPE_CHECKING:
    CLS = ProcessFormView  # type: ignore


class MultiFormMixin(ContextMixin, CLS):
    form_classes: FormClsTypes = {}
    '''map of name- > form-cls'''
    grouped_forms: Dict[str, List[str]] = {}
    '''map to group -> {name -> form-cls} '''

    prefix: str = ""
    prefixes: Dict[str, str] = {}
    '''map to formname -> prefix. By default form-name is used as prefix'''

    success_url: Any = None
    success_urls: Dict[str, Any] = {}
    '''map to formname -> success_url. '''

    initial: Dict[str, Dict] = {}
    '''map to formname -> initial-kwargs'''

    request: HttpRequest
    '''will be setup during View.dispatch'''

    def get_form_classes(self) -> FormClsTypes:
        """return pair of {form-name: form-class}"""
        return self.form_classes

    def get_forms(self, form_classes, form_names=(), bind_all=False) -> FormTypes:
        return {
            key: self._create_form(key, klass, (form_names and key in form_names) or bind_all)
            for key, klass in form_classes.items()
        }

    def get_form_kwargs(self, form_name, bind_form=False) -> Dict[str, Any]:
        kwargs = {}
        kwargs.update(self.get_initial(form_name))
        kwargs.update({'prefix': self.get_prefix(form_name)})

        if bind_form:
            kwargs.update(self._bind_form_data())

        return kwargs

    def forms_valid(self, forms, form_name) -> HttpResponse:
        form_valid_method = '%s_form_valid' % form_name
        if hasattr(self, form_valid_method):
            return getattr(self, form_valid_method)(forms[form_name])
        return HttpResponseRedirect(self.get_success_url(form_name))

    def forms_invalid(self, forms) -> HttpResponse:
        raise NotImplementedError

    def get_initial(self, form_name) -> Dict[str, Any]:
        """initial data to pass to the form when created"""
        initial_method = 'get_%s_initial' % form_name
        if hasattr(self, initial_method):
            return getattr(self, initial_method)()
        return self.initial.copy()

    def get_prefix(self, form_name) -> str:
        return self.prefixes.get(form_name, self.prefix)

    def get_success_url(self, form_name=None) -> Any:
        return self.success_urls.get(form_name, self.success_url)

    def _create_form(self, form_name, klass, bind_form) -> Form:
        form_kwargs = self.get_form_kwargs(form_name, bind_form)
        form_create_method = 'create_%s_form' % form_name
        if hasattr(self, form_create_method):
            form = getattr(self, form_create_method)(**form_kwargs)
        else:
            form = klass(**form_kwargs)
        return form

    def _bind_form_data(self) -> Dict[str, Any]:
        if self.request.method in ('POST', 'PUT'):
            return {'data': self.request.POST,
                    'files': self.request.FILES, }
        return {}


class MultiFormsView(TemplateResponseMixin, MultiFormMixin, ProcessFormView):
    """A view for displaying several forms, and rendering a template response.
    """

    def get(self, request, *args, **kwargs) -> HttpResponse:
        form_classes = self.get_form_classes()
        forms = self.get_forms(form_classes)
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form_classes = self.get_form_classes()
        form_name = request.POST.get('action')
        if self._individual_exists(form_name):
            return self._process_individual_form(form_name, form_classes)
        if self._group_exists(form_name):
            return self._process_grouped_forms(form_name, form_classes)
        return self._process_all_forms(form_classes)

    def _individual_exists(self, form_name) -> bool:
        return form_name in self.form_classes

    def _group_exists(self, group_name) -> bool:
        return group_name in self.grouped_forms

    def _process_individual_form(self, form_name, form_classes) -> HttpResponse:
        forms = self.get_forms(form_classes, (form_name,))
        form = forms.get(form_name)
        if not form:
            return HttpResponseForbidden()
        if form.is_valid():
            return self.forms_valid(forms, form_name)

        return self.forms_invalid(forms)

    def _process_grouped_forms(self, group_name, form_classes) -> HttpResponse:
        form_names = self.grouped_forms[group_name]
        forms = self.get_forms(form_classes, form_names)
        if all([forms[form_name].is_valid() for form_name in form_names]):
            return self.forms_valid(forms, None)

        return self.forms_invalid(forms)

    def _process_all_forms(self, form_classes) -> HttpResponse:
        forms = self.get_forms(form_classes, bind_all=True)
        if all([form.is_valid() for form in forms.values()]):
            for form_name in forms:
                self.forms_valid(forms, form_name)
            return self.forms_valid(forms, None)
        return self.forms_invalid(forms)

    def forms_invalid(self, forms) -> HttpResponse:
        return self.render_to_response(self.get_context_data(forms=forms))
