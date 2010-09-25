import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SERVER_EMAIL = 'errors@synopsize.com'
DEFAULT_FROM_EMAIL = 'no-reply@synopsize.com'

ADMINS = (
    ('Taylan Pince', 'taylanpince@gmail.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Canada/Eastern'

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'

SITE_ID = 1

MEDIA_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'media/')
MEDIA_URL = '/media/'

SECRET_KEY = '#r+cbwct32=+uhcl-$)_!2op5c$t0#^!7+1fn)sb%f9xxf)2ff'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

AUTHENTICATION_BACKENDS = (
    'profiles.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'synopsize.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.realpath(os.path.dirname(__file__)), 'templates/'),
)

AUTH_PROFILE_MODULE = 'profiles.UserProfile'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/register-or-login/'
LOGOUT_URL = '/account/logout/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.markup',

    'django_extensions',
    'sorl.thumbnail',
    'south',

    'profiles',
)

try:
    from settings_local import *
except:
    pass

ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
