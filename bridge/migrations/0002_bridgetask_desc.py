# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-14 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bridgetask',
            name='desc',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
