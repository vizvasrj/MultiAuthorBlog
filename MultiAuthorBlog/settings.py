"""
Django settings for MultiAuthorBlog project.

Generated by 'django-admin startproject' using Django 2.2.22.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

filepath = Path("MultiAuthorBlog/secret.py")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!

if filepath.is_file():
    from .secret import SECRET_KEY as key
    SECRET_KEY = key
else:
    SECRET_KEY = 'opk#ocn6$638cwa&&w(_v^&$e-%_8f2=^ph+ok!+9v1bb64fu^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.4', '*', 'ello.com', '.mysite.com', 'www.mysite.com']

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]

# Application definition

INSTALLED_APPS = [
    'account',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    # 3rd party
    'crispy_forms',
    'colorfield',
    'easy_thumbnails',
    'autoslug',
    'taggit',
    'taggit_autosuggest',
    'mptt',
    'django_editorjs_fields',
    # 'ckeditor_uploader',
    'django_extensions',
    # 'tempus_dominus',
    'django_select2',
    'actions',
    'parler',
    'django_user_agents',
    'django_hosts',
    # 'django_social_share',
    'debug_toolbar',

    # local
    'blog',
    'comment',
    'about',
    'image_uploader',
    'flag',
    'publication',

    # translates
    'translates.hindi_translate',
    'translates.french_translate',
    'translates.chinese_translate',
    'translates.spanish_translate',
    'translates.arabic_translate',
    'translates.indonesian_translate',
    'translates.portuguese_translate',
    'translates.japanese_translate',
    'translates.russian_translate',
    'translates.german_translate',
    'translates.korean_translate',
    'translates.norwegian_translate',
    'translates.vietnamese_translate',
    'translates.filipino_translate',
    'translates.italian_translate',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'account.middleware.subdomain_course_middleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'MultiAuthorBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MultiAuthorBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

if filepath.is_file():
    from .secret import DATABASES
    DATABASES = DATABASES

else:
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




# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_ROOT = ''
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/edit/'


# fixing Errors
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

APPEND_SLASH = False

EDITORJS_DEFAULT_CONFIG_TOOLS = {
        'Image': {
            'class': 'ImageTool',
            'inlineToolbar': True,
            "config": {"endpoints": {"byFile": "/editorjs/image_upload/"}},
        },
        'Header': {
            'class': 'Header',
            'inlineToolbar': True,
            'config': {
                'placeholder': 'Enter a tilte',
                'levels': [2, 3, 4],
                'defaultLevel': 2,
            }
        },
        'Checklist': {'class': 'Checklist', 'inlineToolbar': True},
        'List': {'class': 'List', 'inlineToolbar': True},
        'Quote': {'class': 'Quote', 'inlineToolbar': True},
        # 'Raw': {'class': 'RawTool'},
        'Code': {'class': 'CodeTool'},
        'InlineCode': {'class': 'InlineCode'},
        'Embed': {'class': 'Embed'},
        'Delimiter': {'class': 'Delimiter'},
        'Warning': {'class': 'Warning', 'inlineToolbar': True},
        'LinkTool': {'class': 'LinkTool'},
        'Marker': {'class': 'Marker', 'inlineToolbar': True},
        'Table': {'class': 'Table', 'inlineToolbar': True},
    }



CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    }
}


TAGGIT_CASE_INSENSITIVE = True

# tempus_dominus
# TEMPUS_DOMINUS_LOCALIZE = True


# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


# for django_Select2
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    # 'default-cache': {
    #     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #     'LOCATION': '127.0.0.1:11211',
    # }
}

SELECT2_CACHE_BACKEND = "select2"

SELECT2_CSS = 'css/select2.css'
# SELECT2_JS = ''

TAGGIT_AUTOSUGGEST_MAX_SUGGESTIONS = 8

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# mail
# if filepath.is_file():
#     from .secret import (EMAIL_HOST, 
#     EMAIL_HOST_PASSWORD, EMAIL_HOST_USER,
#     EMAIL_PORT, EMAIL_USE_TLS,
#     DEFAULT_FROM_EMAIL
#     )
#     EMAIL_HOST = EMAIL_HOST
#     EMAIL_HOST_USER = EMAIL_HOST_USER
#     EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
#     EMAIL_PORT = EMAIL_PORT
#     EMAIL_USE_TLS = EMAIL_USE_TLS
#     DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
# else:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


from django.utils.translation import gettext_lazy as _

LANGUAGES = (
    ('en', _('English')),
    ('ar', _('Arabic')),
    ('zh-hans', _('Chinese')),
    ('ta', _('Filipino')),#ta is not tl,  tl is tagalog ta is just another lanugae 
    ('fr', _('French')),
    ('de', _('German')),
    ('hi', _('Hindi')),
    ('id', _('Indonesian')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    ('nn', _('Norwegian')),
    ('pt', _('Portuguese')),
    ('ru', _('Russian')),
    ('es', _('Spanish')),
    ('vi', _('Vietnamese')),

)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
    os.path.join(BASE_DIR, 'taggit_autosuggest/locale/'),
)
PARLER_LANGUAGES = {
    1:(
        {'code': 'en'},
        {'code': 'ar'},
        {'code': 'zh-hans'},
        {'code': 'ta'},
        {'code': 'fr'},
        {'code': 'de'},
        {'code': 'hi'},
        {'code': 'id'},
        {'code': 'it'},
        {'code': 'ja'},
        {'code': 'ko'},
        {'code': 'nn'},
        {'code': 'pt'},
        {'code': 'ru'},
        {'code': 'es'},
        {'code': 'vi'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}

# My uploader
IMAGE_UPLOADER_MAX_FILE_SIZE = 3011000

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = True

# DEBUG = False
# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = False
# SECURE_HSTS_PRELOAD = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


ROOT_HOSTCONF = 'MultiAuthorBlog.hosts'


DEFAULT_HOST = 'www'

# Django Debug Tool
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
def show_toolbar_handler(request):
    if request.user and request.user.id == 1:
        return True
    return False

