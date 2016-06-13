from .base import *

DEBUG = False

ALLOWED_HOSTS = []

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    },
    'websource': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'twcustserv',
        'USER': 'twcustserv',
        'PASSWORD': 'twcustserv',
        'HOST': 'localhost',
        'PORT': '',
    }
}
