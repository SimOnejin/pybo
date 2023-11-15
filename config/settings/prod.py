from .base import *
import environ

ALLOWED_HOSTS = ['43.202.220.99', 'onejin.link']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': 'g6AgbzF6#grN#zhGmh!#2lz<4&z8%;ns',
        'HOST': 'ls-928cdf55379927d357b9fee1be084643f786671e.cf5myg7wocco.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}