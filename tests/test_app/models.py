from django.db import models

# Create your models here.
from utils_plus.models import QueryManager


class Author(models.Model):
    name = models.CharField(max_length=20)

    objects = QueryManager()

    def __str__(self):
        return self.name
