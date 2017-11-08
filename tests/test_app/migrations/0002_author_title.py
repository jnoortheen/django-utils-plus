# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 17:53
from __future__ import unicode_literals

from django.db import migrations
import tests.test_app.models
import utils_plus.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='title',
            field=utils_plus.fields.ChoicesEnumField(tests.test_app.models.Title, default=tests.test_app.models.Title('Mr.'), max_length=3),
        ),
    ]