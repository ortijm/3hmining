# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-18 17:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0015_auto_20161118_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridgeresponse',
            name='dateResponse',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 11, 18, 17, 19, 55, 953587)),
        ),
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
