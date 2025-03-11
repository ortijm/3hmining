# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-18 22:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0021_auto_20161118_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridgeresponse',
            name='typeTask',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bridge.TypeBridgeTask'),
        ),
        migrations.AlterField(
            model_name='bridgetask',
            name='typeTask',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bridge.TypeBridgeTask'),
        ),
    ]
