from .base import *

DEBUG = False

ADMINS = (
    ('Presento Being', 'presentobeing@gmail.com'),
)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vizvasrj0004',
        'USER': 'root',
        'PASSWORD': 'icandoit10!',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}