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
import datetime
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
    global CONF, CACHE
    global NEWS, EVENT, LOCATION, CUSTOM, SITE, BUSINESS


################数据库配置########################
    confdb = query_one(user=login_user)

    ALLOWED_HOSTS = confdb['allowed_hosts']

    DEBUG = confdb['debug']

    TEMPLATE_DEBUG = DEBUG

    COMPANY_NAME = confdb['company_name']

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = confdb['language_code']

    TIME_ZONE = confdb['time_zone']

    USE_I18N = confdb['use_i18n']

    USE_L10N = confdb['use_l10n']

    USE_TZ = confdb['use_tz']

    MEDIA_ROOT = confdb['media_root']

    STATIC_ROOT = confdb['static_root']

    NEWS_PAGE_LIMIT = confdb['news_page_limit']

    EVENT_PAGE_LIMIT = confdb['event_page_limit']

    RISK_PAGE_LIMIT = confdb['risk_page_limit']

    WEIXIN_TABLE_LIMIT = confdb['weixin_table_limit']

    WEIBO_TABLE_LIMIT = confdb['weibo_table_limit']

    LOCATION_WEIXIN_LIMIT = confdb['location_weixin_limit']

    LOCATION_WEIBO_LIMIT = confdb['location_weibo_limit']

    EVENT_WEIXIN_LIMIT = confdb['event_weixin_limit']

    EVENT_WEIBO_LIMIT = confdb['event_weibo_limit']

    RISK_WEIXIN_LIMIT = confdb['risk_weixin_limit']

    RISK_WEIBO_LIMIT = confdb['risk_weibo_limit']

    CUSTOM_NEWS_LIMIT = confdb['custom_news_limit']

    CUSTOM_WEIXIN_LIMIT = confdb['custom_weixin_limit']

    CUSTOM_WEIBO_LIMIT = confdb['custom_weibo_limit']

    PRODUCT_LIMIT = confdb['product_limit']

    SEARCH_LIMIT = confdb['search_limit']

    #sidebar
    NEWS = confdb['news']

    EVENT = confdb['event']

    LOCATION = confdb['location']

    CUSTOM = confdb['custom']

    SITE = confdb['site']

    BUSINESS = confdb['business']

    # MySQL
    mysql_conn_str_default = confdb['mysql_default']
    mysql_conn_str_master = confdb['mysql_master']
    mysql_conn_str_corpus = confdb['mysql_corpus']
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
    MONGO_CONN_STR = confdb['mongo_conn']

    # Redis
    redis_conn_str = confdb['redis_conn']
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
    'observer.apps.riskmonitor',
    'tinymce',
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


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': 'P@55word',
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

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
