# -*- coding: utf-8 -*-
import sys
import os
root_mod = '/home/feng/Project/observer/api'
sys.path.append(root_mod)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")
import requests

from django.conf import settings
from django_extensions.management.jobs import BaseJob

from observer.apps.yqj.redisconnect import RedisQueryApi

class BaseCatch(BaseJob):

    def cache(self, datas):
        url_cfg = (settings.CACHE).decode()
        url_cache = datas['url'] %(url_cfg)
        result = requests.get(url=url_cache)
        RedisQueryApi().hset(datas['hset_name'], datas['hset_key'], result.text)

    def get(self, name, url):
        datas = {'url': url,
                'hset_name' : name,
                'hset_key' : u'abstract'}
        self.cache(datas)

if __name__ == '__main__':
    BaseCatch().get(name=u'event', url=u'%s/api/event/?type=abstract&cache=0')
