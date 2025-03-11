# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from bridge.models import Minera


APP_THEME = (
    ("Orange", "Orange"),
    ("Blue", "Blue"),
    ("Lime", "Lime"),
    ("Green", "Green"),
    ("Teal", "Teal"),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    #Informacion Personal

    # Informacion Usuario
    expiration = models.DateField('Fecha Expiracion', null=False, blank=False, auto_now_add=True)
    bridge = models.ForeignKey(Minera, blank=True, null=True, on_delete=models.SET_NULL)

    # Customization
    app_theme = models.CharField('App Theme', max_length=12, choices=APP_THEME, blank=True, default="Orange'")

    @property
    def is_activo(self):
        """determina si esta activo"""
        return True if datetime.datetime.today().date() < self.expiration else False
