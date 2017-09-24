from django.db import models

# Create your models here.
from utils_plus.models import QueryManager


class Author(models.Model):
    name = models.CharField(max_length=20)

    objects = QueryManager()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    name = models.CharField(max_length=40)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    rel_objects = QueryManager(name__icontains='filter').selects('publisher').prefetches('authors').order_by('-id')
