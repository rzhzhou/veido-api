import sys
root_mod = '/home/feng/Project/observer/app'
sys.path.append(root_mod)
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")
import requests
import ConfigParser
from datetime import datetime, timedelta, date

from django.conf import settings
from django_extensions.management.jobs import BaseJob

from observer.apps.base.catch import BaseCatch
from observer.apps.yqj.redisconnect import RedisQueryApi

class Job(BaseCatch):
    def execute(self):
        self.get(name='risk')

if __name__ == '__main__':
    Job().execute()