#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import re_path
from .views import (
    usuarios_ingreso,
    overview,
    mineview,
    bridgeResponse,
    dynamic_endpoint,
    get_endpoints,
    logout,
)

urlpatterns = [
    re_path(r'^user/login/$', usuarios_ingreso),
    re_path(r'^user/logout/$', logout),
    re_path(r'^user/endpoints/$', get_endpoints),
    #re_path(r'^user/me/$', 'user_me', name='user_me'),
    # data
    re_path(r'^data/(?P<endpoint>\w+)/$', dynamic_endpoint),
    re_path(r'^data/bridgeResponse/(?P<responseTaskName>\w+)$', bridgeResponse),
    re_path(r'^data/overview/$', overview),
    re_path(r'^data/mineview/$', mineview),
]
