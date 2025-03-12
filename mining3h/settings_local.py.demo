import os
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',
    }
}

LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'handlers': {
       'console': {
           'class': 'logging.StreamHandler',
       },
   },
   'loggers': {
       'django': {
           'handlers': ['console'],
           'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
       },
   },
}
