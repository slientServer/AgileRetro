from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'agileretro',
        'USER': 'root',
        'PASSWORD': 'toor',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

