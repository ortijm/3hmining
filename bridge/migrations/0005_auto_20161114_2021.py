# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-14 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0004_merge_20161114_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bridgetask',
            name='desc',
        ),
        migrations.AlterField(
            model_name='bridgetask',
            name='ping',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='bridgetask',
            name='query',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
