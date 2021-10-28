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
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(
            os.path.join(__file__, os.pardir)
        )
    )
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'opk#ocn6$638cwa&&w(_v^&$e-%_8f2=^ph+ok!+9v1bb64fu^'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.4', '*', 'ello.com']

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
    'tempus_dominus',
    'django_select2',
    'actions',
    'parler',
    'django_user_agents',
    "compressor",

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
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'MultiAuthorBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

