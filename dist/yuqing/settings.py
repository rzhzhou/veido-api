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
    global COMPANY_NAME, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ, NEWS_PAGE_LIMIT,\
                 RISK_PAGE_LIMIT, EVENT_PAGE_LIMIT, WEIXIN_TABLE_LIMIT, WEIBO_TABLE_LIMIT,\
                 LOCATION_WEIXIN_LIMIT, LOCATION_WEIBO_LIMIT, EVENT_WEIXIN_LIMIT, EVENT_WEIBO_LIMIT,\
                 RISK_WEIXIN_LIMIT, RISK_WEIBO_LIMIT, CUSTOM_NEWS_LIMIT, CUSTOM_WEIXIN_LIMIT, PRODUCT_LIMIT, SEARCH_LIMIT
    global MYSQL_CONN_STR_DEFAULT, MYSQL_CONN_STR_MASTER, MYSQL_CONN_STR_CORPUS, MONGO_CONN_STR, REDIS_CONN_STR
    global MEDIA_ROOT, STATIC_ROOT
    global NEWS_PAGE_LIMIT

    cp = SafeConfigParser()
    cp.read(os.path.join(BASE_DIR, "../config.cfg"))

    SECTION = cp.get('deploy', 'environment')

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = cp.getboolean(SECTION, 'DEBUG')

    TEMPLATE_DEBUG = DEBUG

    ALLOWED_HOSTS = eval(cp.get(SECTION, 'ALLOWED_HOSTS'))

    COMPANY_NAME = cp.get(SECTION, 'COMPANY_NAME')

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = cp.get(SECTION, 'LANGUAGE_CODE')

    TIME_ZONE = cp.get(SECTION, 'TIME_ZONE')

    USE_I18N = cp.get(SECTION, 'USE_I18N')

    USE_L10N = cp.get(SECTION, 'USE_L10N')

    USE_TZ = cp.get(SECTION, 'USE_TZ')

    MEDIA_ROOT = cp.get(SECTION, 'MEDIA_ROOT')

    STATIC_ROOT = cp.get(SECTION, 'STATIC_ROOT')

    NEWS_PAGE_LIMIT = cp.get('constant', 'NEWS_PAGE_LIMIT')

    EVENT_PAGE_LIMIT = cp.get('constant', 'EVENT_PAGE_LIMIT')

    RISK_PAGE_LIMIT = cp.get('constant', 'RISK_PAGE_LIMIT')

    WEIXIN_TABLE_LIMIT = cp.get('constant', 'WEIXIN_TABLE_LIMIT')

    WEIBO_TABLE_LIMIT = cp.get('constant', 'WEIBO_TABLE_LIMIT')

    LOCATION_WEIXIN_LIMIT = cp.get('constant', 'LOCATION_WEIXIN_LIMIT')

    LOCATION_WEIBO_LIMIT = cp.get('constant', 'LOCATION_WEIBO_LIMIT')

    EVENT_WEIXIN_LIMIT = cp.get('constant', 'EVENT_WEIXIN_LIMIT')

    EVENT_WEIBO_LIMIT = cp.get('constant', 'EVENT_WEIBO_LIMIT')

    RISK_WEIXIN_LIMIT = cp.get('constant', 'RISK_WEIXIN_LIMIT')

    RISK_WEIBO_LIMIT = cp.get('constant', 'RISK_WEIBO_LIMIT')

    CUSTOM_NEWS_LIMIT = cp.get('constant', 'CUSTOM_NEWS_LIMIT')

    CUSTOM_WEIXIN_LIMIT = cp.get('constant', 'CUSTOM_WEIXIN_LIMIT')

    CUSTOM_WEIBO_LIMIT = cp.get('constant', 'CUSTOM_WEIBO_LIMIT')

    PRODUCT_LIMIT = cp.get('constant', 'PRODUCT_LIMIT')

    SEARCH_LIMIT = cp.get('constant', 'SEARCH_LIMIT')

    # MySQL
    mysql_conn_str_default = cp.get(SECTION, 'mysql_conn_str_default')
    mysql_conn_str_master = cp.get(SECTION, 'mysql_conn_str_master')
    mysql_conn_str_corpus = cp.get(SECTION, 'mysql_conn_str_corpus')
    MYSQL_CONN_STR_DEFAULT = re.match(
        r"mysql://(?P<username>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/(?P<name>.+)",
        mysql_conn_str_default).groupdict()
    MYSQL_CONN_STR_MASTER = re.match(
        r"mysql://(?P<username>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/(?P<name>.+)",
        mysql_conn_str_master).groupdict()
    MYSQL_CONN_STR_CORPUS = re.match(
        r"mysql://(?P<username>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/(?P<name>.+)",
        mysql_conn_str_corpus).groupdict()

    # MongoDB
    MONGO_CONN_STR = cp.get(SECTION, 'mongo_conn_str')

    # Redis
    redis_conn_str = cp.get(SECTION, 'redis_conn_str')
    REDIS_CONN_STR = re.match(
        r"redis://(?P<host>.+):(?P<port>\d+)/(?P<db>.+)",
        redis_conn_str).groupdict()

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
    'django_extensions',
    'import_export',
    'collection',
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
    'corpus':{
        'ENGINE': 'django.db.backends.mysql',
        'HOST': MYSQL_CONN_STR_CORPUS['host'],
        'NAME': MYSQL_CONN_STR_CORPUS['name'],
        'USER': MYSQL_CONN_STR_CORPUS['username'],
        'PASSWORD': MYSQL_CONN_STR_CORPUS['password'],
    },
}

DATABASE_ROUTERS = ['corpus.router.MyDB2Router',]

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
