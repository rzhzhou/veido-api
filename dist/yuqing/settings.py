# -*- coding: utf-8 -*-
"""
Django settings for yuqing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re
from ConfigParser import SafeConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def _load_config():
    global DEBUG, TEMPLATE_DEBUG, ALLOWED_HOSTS
    global COMPANY_NAME, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ, NEWS_PAGE_LIMIT
    global MYSQL_CONN_STR_DEFAULT, MYSQL_CONN_STR_MASTER, MONGO_CONN_STR, REDIS_CONN_STR
    global MEDIA_ROOT, STATIC_ROOT
    global NEWS_PAGE_LIMIT

_load_config()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6f-lqyij0+64*exps#yyni+%@)6aryv56ooe)2h+$$vvvkdcm8'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'yqj',
    'analytics',
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

ROOT_URLCONF = 'base.urls'

WSGI_APPLICATION = 'yuqing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': MYSQL_CONN_STR_DEFAULT['host'],
        'NAME': MYSQL_CONN_STR_DEFAULT['name'],
        'USER': MYSQL_CONN_STR_DEFAULT['username'],
        'PASSWORD': MYSQL_CONN_STR_DEFAULT['password'],
    },
    'master': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': MYSQL_CONN_STR_MASTER['host'],
        'NAME': MYSQL_CONN_STR_MASTER['name'],
        'USER': MYSQL_CONN_STR_MASTER['username'],
        'PASSWORD': MYSQL_CONN_STR_MASTER['password'],
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)


if not MEDIA_ROOT:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
