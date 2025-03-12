# -*- coding: utf-8 -*-
from django.contrib.sessions.backends.cache import SessionStore as DjangoSessionStore
from django.core.cache import cache


class SessionStore(DjangoSessionStore):
    """
    A cache-based session store on it's own cache instance
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)
        self._cache = cache.get('session')
