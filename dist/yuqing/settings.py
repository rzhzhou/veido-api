#coding=utf-8
"""
Django settings for yuqing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6f-lqyij0+64*exps#yyni+%@)6aryv56ooe)2h+$$vvvkdcm8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['192.168.1.161', '27.17.61.26', 'cnshendu.com', 'www.cnshendu.com']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yqj',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'yqj.middleware.UserAuthenticationMiddlerware',
)

ROOT_URLCONF = 'yuqing.urls'

WSGI_APPLICATION = 'yuqing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.1.101',
        'NAME': 'yqj2',
        'USER': 'root',
        'PASSWORD': '123456',
    },
    'master': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.1.161',
        'NAME': 'yqj',
        'USER': 'shendu',
        'PASSWORD': 'P@55word',
    },
}

MONGO_CONN_STR = "mongodb://192.168.1.202:27017"

REDIS_CONF = {
            'host': '192.168.1.161',
            'port': '6379',
            'db': 8
        }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA_ROOT = '/var/www/media'
STATIC_ROOT = '/var/www/static'

MEDIA_URL = '/media/'





COMPANY_NAME = u'质监局'
