import sys
root_mod = '/home/feng/Project/observer/app'
sys.path.append(root_mod)
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")
import time, sched
import requests
import ConfigParser
from datetime import datetime, timedelta, date

from django.conf import settings
from django_extensions.management.jobs import BaseJob

from observer.apps.yqj.redisconnect import RedisQueryApi
reload(sys)
sys.setdefaultencoding("utf-8")

class BaseCatch(BaseJob):

    def Cache(self, datas):
        url_cfg = settings.CACHE

        url_cache = '%s/api/%s/?type=abstract&catch=0' % (url_cfg, datas['hset_name'])
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }

        res = requests.post(
            url = '%s/api/login/' % url_cfg,
            data = {
            'username': datas['username'],
            'password': datas['password']}
            )
        headers['Cookie'] = res.headers['set-cookie']
        result = requests.get(url=url_cache, headers=headers)
        RedisQueryApi().hset(datas['hset_name'], datas['hset_key'], str(result.text))

    def homePageCatch(self, name):
            datas = {
                    'hset_name' : name,
                    'hset_key' : 'abstract',
                    'username' : 'wuhan',
                    'password' : 'wuhan'
                }
            self.Cache(datas)

    def get(self, name):
        self.homePageCatch(name)


if __name__ == '__main__':
    BaseCatch().get(name='event')
