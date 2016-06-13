import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e4!hj8-o=-19jsqb*j7os!ipvr68#!=-9u=9o3^c4u-yy0ghy0'

# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',

    'djcelery',

    'accounts',
    'customerservice',
    'profiles',
    'purchase',
    'shows',
    'transactions'
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'twcustserv.urls'

WSGI_APPLICATION = 'twcustserv.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-AR'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.static",
                "social.apps.django_app.context_processors.backends",
                "social.apps.django_app.context_processors.login_redirect"
            ],
            'debug': True
        },
    },
]

SUIT_CONFIG = {
    'ADMIN_NAME': 'Ticketek CS Dashboard',
    'MENU_EXCLUDE': ('auth.group', 'auth'),
    'SEARCH_URL': '/admin/customerservice/thread/',
    'MENU_ICONS': {
        'customerservice': 'icon-envelope',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

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

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ayuda@ticketek.com.ar'
EMAIL_HOST_PASSWORD = 'sentidocomun'
DEFAULT_EMAIL_FROM = 'ayuda@ticketek.com.ar'

DATABASE_ROUTERS = ['customerservice.routers.AuthRouter']
