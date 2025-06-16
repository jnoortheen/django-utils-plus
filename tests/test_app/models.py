from django.db import models

# Create your models here.
from utils_plus.abstracts import CheckDeletableModelMixin
from utils_plus.choices import ChoicesEnum
from utils_plus.fields import ChoicesEnumField
from utils_plus.models import QueryManager


class Title(ChoicesEnum):
    mr = 'Mr.'
    ms = 'Ms.'
    mrs = 'Mrs.'


class Author(CheckDeletableModelMixin, models.Model, ):
    title = ChoicesEnumField(Title, default=Title.mr)
    name = models.CharField(max_length=20)

    objects = QueryManager()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    rel_objects = QueryManager(name__icontains='filter').selects('publisher').prefetches('authors').order_by('-id')
