DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'synopsize',
        'USER': 'synopsizedbu',
        'PASSWORD': 'sHumUs0Gob',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_URL = 'http://media.snopsize.com/'
