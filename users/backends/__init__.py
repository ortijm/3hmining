#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

class EmailBackend(object):
    """
    Backend email authentication class.
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if not user.is_active:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
