from __future__ import unicode_literals

from django.db import models

class MineOverview(models.Model):
    movement_total = models.IntegerField(blank=True)
    extraction = models.IntegerField(blank=True)
    min_extracted = models.IntegerField(blank=True)
    min_plant = models.IntegerField(blank=True)
    law_cu_plant = models.IntegerField(blank=True)
    as_ppm = models.IntegerField(blank=True)
