#!/usr/bin/python
import os, sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
projet_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(root_dir)
sys.path.append(projet_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
