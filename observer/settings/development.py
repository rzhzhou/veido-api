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
import sys
import re
from ConfigParser import SafeConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(BASE_DIR))
sys.path.append(BASE_DIR)
from observer.utils.connector.mysql import query_one


login_user = 'wuhan'


def _load_config():
    global DEBUG, TEMPLATE_DEBUG, ALLOWED_HOSTS
    global COMPANY_NAME, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ, NEWS_PAGE_LIMIT,\
                 RISK_PAGE_LIMIT, EVENT_PAGE_LIMIT, WEIXIN_TABLE_LIMIT, WEIBO_TABLE_LIMIT,\
                 LOCATION_WEIXIN_LIMIT, LOCATION_WEIBO_LIMIT, EVENT_WEIXIN_LIMIT, EVENT_WEIBO_LIMIT,\
                 RISK_WEIXIN_LIMIT, RISK_WEIBO_LIMIT, CUSTOM_NEWS_LIMIT, CUSTOM_WEIXIN_LIMIT, PRODUCT_LIMIT, SEARCH_LIMIT
    global MYSQL_CONN_STR_DEFAULT, MYSQL_CONN_STR_MASTER, MYSQL_CONN_STR_CORPUS, MONGO_CONN_STR, REDIS_CONN_STR
    global MEDIA_ROOT, STATIC_ROOT
    global NEWS_PAGE_LIMIT
    global CONF


################数据库配置########################
    ALLOWED_HOSTS = query_one(user=login_user, confname='ALLOWED_HOSTS')

    DEBUG = query_one(user=login_user, confname='DEBUG')

    TEMPLATE_DEBUG = DEBUG

    COMPANY_NAME = query_one(user=login_user, confname='COMPANY_NAME')

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = query_one(user=login_user, confname='LANGUAGE_CODE')

    TIME_ZONE = query_one(user=login_user, confname='TIME_ZONE')

    USE_I18N = query_one(user=login_user, confname='USE_I18N')

    USE_L10N = query_one(user=login_user, confname='USE_L10N')

    USE_TZ = query_one(user=login_user, confname='USE_TZ')

    MEDIA_ROOT = query_one(user=login_user, confname='MEDIA_ROOT')

    STATIC_ROOT = query_one(user=login_user, confname='STATIC_ROOT')

    NEWS_PAGE_LIMIT = query_one(user=login_user, confname='NEWS_PAGE_LIMIT')

    EVENT_PAGE_LIMIT = query_one(user=login_user, confname='EVENT_PAGE_LIMIT')

    RISK_PAGE_LIMIT = query_one(user=login_user, confname='RISK_PAGE_LIMIT')

    WEIXIN_TABLE_LIMIT = query_one(user=login_user, confname='WEIXIN_TABLE_LIMIT')

    WEIBO_TABLE_LIMIT = query_one(user=login_user, confname='WEIBO_TABLE_LIMIT')

    LOCATION_WEIXIN_LIMIT = query_one(user=login_user, confname='LOCATION_WEIXIN_LIMIT')

    LOCATION_WEIBO_LIMIT = query_one(user=login_user, confname='LOCATION_WEIBO_LIMIT')

    EVENT_WEIXIN_LIMIT = query_one(user=login_user, confname='EVENT_WEIXIN_LIMIT')

    EVENT_WEIBO_LIMIT = query_one(user=login_user, confname='EVENT_WEIBO_LIMIT')

    RISK_WEIXIN_LIMIT = query_one(user=login_user, confname='RISK_WEIXIN_LIMIT')

    RISK_WEIBO_LIMIT = query_one(user=login_user, confname='RISK_WEIBO_LIMIT')

    CUSTOM_NEWS_LIMIT = query_one(user=login_user, confname='CUSTOM_NEWS_LIMIT')

    CUSTOM_WEIXIN_LIMIT = query_one(user=login_user, confname='CUSTOM_WEIXIN_LIMIT')

    CUSTOM_WEIBO_LIMIT = query_one(user=login_user, confname='CUSTOM_WEIBO_LIMIT')

    PRODUCT_LIMIT = query_one(user=login_user, confname='PRODUCT_LIMIT')

    SEARCH_LIMIT = query_one(user=login_user, confname='SEARCH_LIMIT')

    # MySQL
    mysql_conn_str_default = query_one(user=login_user, confname='mysql_default')
    mysql_conn_str_master = query_one(user=login_user, confname='mysql_master')
    mysql_conn_str_corpus = query_one(user=login_user, confname='mysql_corpus')
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
    MONGO_CONN_STR = query_one(user=login_user, confname='mongo_conn')

    # Redis
    redis_conn_str = query_one(user=login_user, confname='redis_conn')
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
    'observer.apps.base',
    'observer.apps.yqj',
    'observer.apps.event',
    'observer.apps.analytics',
    'observer.apps.collection',
    'observer.apps.config',
    'rest_framework',
    'django_extensions',
    'import_export',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'observer.apps.yqj.middleware.UserAuthenticationMiddlerware',
)

ROOT_URLCONF = 'observer.urls'

WSGI_APPLICATION = 'observer.wsgi.application'


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

DATABASE_ROUTERS = ['observer.apps.corpus.router.MyDB2Router',]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static/build/"),
)


TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)


if not MEDIA_ROOT:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
