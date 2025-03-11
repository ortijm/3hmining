# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-09 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20170126_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicgraph',
            name='extra',
            field=models.TextField(blank=True, default=b'\n                                        {\n                                            "zoom": "14",\n                                            "series": {"y":"", "y2": ""}\n                                        }\n                                        ', help_text=b'<strong>Format:</strong> JSON</br>\n                                          <strong>Options:</strong> series, table_headers, shovels, label_x, zoom</br>\n                                          </br>\n                                          ie:<br>{<br>&nbsp;&nbsp;&nbsp;&nbsp;"label_x": "hours",\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;"table_headers": {\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"header1": ["Movimientos (kt)", "Real (kt)"]\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;},\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;"shovels": {\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"S01": {"lat": -22.124124, "lon": -69.01120}\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;},\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;"series": {\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"y": "Movimiento Mina",\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"y2": "Extraccion Mina"\n                                          </br>&nbsp;&nbsp;&nbsp;&nbsp;}</br>}\n                                          </br></br><strong>Important:</strong> Properties must to be enclosed in double quotes.\n                                          ', null=True),
        ),
    ]
