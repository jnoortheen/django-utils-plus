# utils-plus 
It is a simple Django app having various mixins and functions that are found commonly useful

# Installation
To install directly from the repo
```
pip install git+git://github.com/jnoortheen/django-utils-plus.git
```
and add it to your requirements.txt like this 
`-e git://github.com/jnoortheen/django-utils-plus.git@master#egg=django_utils_plus`

# Management Commands
 - clear_records
 - create_admin
 - test_mail
 - create_middleware
    
# Template tags
 - klass
 - 
 
# Middleware
 - login_required_middleware

# UrlGroup

An elegant and DRY way to define urlpatterns. It has easier to nest many levels deeper and still have the readability.
It is just a wrapper behind the standard url(), include() methods.

This is how your urls.py may look
```python
### urls.py ###
urlpatterns = [
    url(r'^studenteditordocument/(?P<doc_pk>\d+)/edit/$', DocEditorView.as_view(), name='edit-student-doc'),
    url(r'^studenteditordocument/(?P<doc_pk>\d+)/export/$', DocExporterView.as_view(), name='export-editore-doc'),

    url(r'^docs/$', Docs.as_view(), name='student-documents'),
    url(r'^publish/$', DeleteOrPublistDoc.as_view(), {'action': 'publish'}, name="publish_document"),
    url(r'^delete/$', DeleteOrPublistDoc.as_view(), name='delete_document'),
]
```

after using `UrlGroup`
```python
### urls.py ###
with UrlGroup('editor') as ug:
    with ug.int('doc_pk'):
        ug('edit', DocEditorView.as_view(), 'edit-doc')
        ug('export', DocExporterView.as_view(), 'export-doc')
ug('docs', Docs.as_view(), 'student-documents')
ug('publish', DeleteOrPublistDoc.as_view(), 'publish_document', action='publish')
ug('delete', DeleteOrPublistDoc.as_view(), 'delete_document')

urlpatterns = ug.urlpatterns
```

you could also do this if you aren't afraid of typing more letters. There is no need to define the urlpatterns variable
separately
```python
### urls.py ###
with UrlGroup('editor') as urlpatterns:
    with urlpatterns.int('doc_pk'):
        urlpatterns('edit', DocEditorView.as_view(), 'edit-doc')
        urlpatterns('export', DocExporterView.as_view(), 'export-doc')
urlpatterns('docs', Docs.as_view(), 'student-documents')
urlpatterns('publish', DeleteOrPublistDoc.as_view(), 'publish_document', action='publish')
urlpatterns('delete', DeleteOrPublistDoc.as_view(), 'delete_document')
```

see url_group_test.py for more use cases

## Config Option
 - `URL_GROUP_TRAIL_SLASH` 
    - By default all the urls generated by this class will have trailing slash
    - Set this to False in settings.py to change this behaviour
    