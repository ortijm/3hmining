# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 14:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0078_auto_20170317_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridgeresponse',
            name='typeTask',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bridge.TypeBridgeTask'),
        ),
        migrations.AlterField(
            model_name='bridgetask',
            name='rows',
            field=models.IntegerField(default=300),
        ),
        migrations.AlterField(
            model_name='bridgetask',
            name='typeTask',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='bridge.TypeBridgeTask'),
        ),
    ]
