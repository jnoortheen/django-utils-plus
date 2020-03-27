# utils-plus 
A simple reusable Django app with various mixins and utility functions.

-------

[![PyPi Version](https://img.shields.io/pypi/v/pconf.svg?style=flat)](https://pypi.python.org/pypi/pconf)
[![Python Version](https://img.shields.io/pypi/pyversions/returns.svg)](https://pypi.org/project/returns/)

-------

# Installation
install the package using the below command

```commandline
pip install django-utils-plus
```

or install the development version using 
```commandline
pip install git://github.com/jnoortheen/django-utils-plus.git@master#egg=django-utils-plus
```

# Utils

## Management Commands
 - clear_records
 - create_admin
 - test_mail
 - cleardata
 - create_middleware
    
## Template tags
 1. klass
 1. [unpkg](#unpkg)
 1. [jsdelivr](#jsdelivr) (combined support as well)
 
### serve static files using npm
 it is convenient to keep track of all external `js` libraries in project using 
 a `package.json`. It is used to keep latest version of available packages. 
 The following template tags can be used to serve these packages right from CDN on production and 
 `node_modules` during development

#### unpkg
 Alternative to standard `static` template tag. When you are using external static files/libraries
like bootstrap, jquery you may want to load them from CDNs instead of managing them yourself in production.
This tag helps you to do that. When `settings.DEBUG` is false, this will return paths that resolved from
`package.json` to versioned `unpkg.com`. Otherwise it will resolve to `node_modules` locally.

#### jsdelivr
    like `unpkg` adds support for using https://www.jsdelivr.com/

#### Usage:

load the template tags and use `unpkg` like `static` tag,

```
{% load static utils_plus_tags %}
<link rel="stylesheet" type="text/css" href="{% unpkg 'bootstrap/dist/css/bootstrap.min.css' %}"/>
<script src="{% unpkg 'bootstrap/dist/js/bootstrap.min.js' %}"></script>
<script src="{% unpkg 'jquery/dist/jquery.min.js' %}"></script>
```
#### Note:
1. the package.json should be present in the project ROOT DIR.
1. When DEBUG is True the packages must  be installed and should be available already inside `node_modules`.
 

## Middleware
 - login_required_middleware

## Urls & Routing with ease

An elegant and DRY way to define urlpatterns. It has easier to nest many levels deeper and still have the readability.
It is just a wrapper behind the standard url(), include() methods.

This is how your urls.py may look
```python
### urls.py ###
urlpatterns = [
    url(r'^studenteditordocument/(?P<doc_pk>\d+)/edit/$', EditView.as_view(), name='edit-student-doc'),
    url(r'^studenteditordocument/(?P<doc_pk>\d+)/export/$', ExportView.as_view(), name='export-editore-doc'),

    url(r'^docs/$', Docs.as_view(), name='student-documents'),
    url(r'^publish/$', PulishOrDelete.as_view(), {'action': 'publish'}, name="publish_document"),
    url(r'^delete/$', PulishOrDelete.as_view(), name='delete_document'),
]
```

after using `Url`
```python
### urls.py ###

from utils_plus.router import Url

with Url('editor') as u:
    with u.int('doc_pk'):
        u('edit', EditView.as_view(), 'edit-doc')
        u('export', ExportView.as_view(), 'export-doc')
u('docs', Docs.as_view(), 'student-documents')
u('publish', PulishOrDelete.as_view(), 'publish_document', action='publish')
u('delete', PulishOrDelete.as_view(), 'delete_document')

urlpatterns = u.urlpatterns
```

you could also do this if you aren't afraid of typing more. There is no need to define the urlpatterns variable
separately
```python
### urls.py ###

from utils_plus.router import Url

with Url('editor') as urlpatterns:
    with urlpatterns.int('doc_pk'):
        urlpatterns('edit', EditView.as_view(), 'edit-doc')
        urlpatterns('export', ExportView.as_view(), 'export-doc')
urlpatterns('docs', Docs.as_view(), 'student-documents')
urlpatterns('publish', PulishOrDelete.as_view(), 'publish_document', action='publish')
urlpatterns('delete', PulishOrDelete.as_view(), 'delete_document')
```

see `tests/test_router.py` for more use cases

## Model 

1. `CheckDeletableModelMixin`
adds a `is_deletable` method which then can be used to check any affected related records before actually deleting them.
originally it is copied from this [gist](https://gist.github.com/freewayz/69d1b8bcb3c225bea57bd70ee1e765f8)

2. `ChoicesEnum`
Enumerator class for use with the django ORM choices field

3. `QueryManager`
A DRYer way to set select_related, prefetch_related & filters to queryset.
    - this has `first_or_create` method similar to get_or_create

```python
from django.db import models
from utils_plus.models import QueryManager

class Post(models.Model):
    author = models.ForeignKey('Author')
    comments = models.ManyToManyField('Comment')
    published = models.BooleanField()
    pub_date = models.DateField()
    
    # custom managers
    objects = QueryManager() # equivalent to models.Manager
    public_posts = QueryManager(published=True).order_by('-pub_date')
    rel_objects = QueryManager().selects('author').prefetches('comments')
```

## Config Option

1. `URL_GROUP_TRAIL_SLASH`
    - By default all the urls generated by this class will have trailing slash
    - Set this to False in settings.py to change this behaviour

## Views
1. **CreateUpdateView**:
    - combines CreateView and UpdateView

## Testing the project
    - clone the repo and run migrations after installing dependencies
    - `inv test` will run all the test for the app
