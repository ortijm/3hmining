#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import taskIn,taskOut,hi3H,taskUp
urlpatterns = [
    re_path(r'^up/$', taskUp),
    re_path(r'^taskIn/$', taskIn),
    re_path(r'^taskOut/$', taskOut),
    re_path(r'^hi3H/', hi3H)
]
