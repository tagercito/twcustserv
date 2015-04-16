"""
Django settings for twcustserv project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e4!hj8-o=-19jsqb*j7os!ipvr68#!=-9u=9o3^c4u-yy0ghy0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'customerservice',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'twcustserv.urls'

WSGI_APPLICATION = 'twcustserv.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'Ticketek CS Dashboard',
    'MENU_EXCLUDE': ('auth.group', 'auth'),
    'MENU_ICONS': {
        'customerservice': 'icon-envelope',
    }
}

TEMPLATES_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)        
  
print TEMPLATES_DIRS 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
   
##### SETTINGS for the Twitter Customer Service Account : @apimtechtest ##### 

CONTINUA=' (cont)' #Add this string to every splitted replied message that Representative sends

CONSUMER_KEY = 'Fbve1E4JqZ0cnb9ouVoOycbgp'
CONSUMER_SECRET = '2HOEHzTR2E6LAbWmglkFwOzq2WCZ3X2LJwguHFq0eUVZIWNmRX'
ACCESS_TOKEN_KEY = '3129661635-wjyM6RYKSWQ37LDhNOtmvDmNNq0JkL1n1SI75EJ'
ACCESS_TOKEN_SECRET = 'vnDCKDf1ILaZMuJaTgO4cvaFdFr3oP7AXMsBanblyLU84'

APPS_TWITTER_USERNAME = 'apimtechtest'


POST_MENTION_UPDATE = 'Hola @%s, por favor mandanos un mensaje directo con tus datos y el problema, que te contestaremos a la brevedad.'
ANSWER_TO_DIRECT_MESSAGE = 'Gracias @%s por contactarnos, te responderemos a la brevedad con una solucion a tu consulta.'

OPEN = 'OP'
PENDING = 'PE'       
CLOSED = 'CL' 
