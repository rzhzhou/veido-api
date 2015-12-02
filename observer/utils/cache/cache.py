# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")
import requests

from django.conf import settings
from django_extensions.management.jobs import BaseJob

from observer.apps.config.model import CacheConf
from observer.utils.connector.redisconnector import RedisQueryApi


class BaseCatch(BaseJob):

    def cache(self, datas):
        # url_cfg = CacheConf.object.get(name='dashboard').url
        url_cfg = 'http://192.168.1.200:19980'
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }
        res = requests.post(
            url = "%s/api/token-auth" %url_cfg,
            data = {
            "username": 'wuhan',
            "password": 'wuhan'}
            )
        headers['Authorization'] = 'Bearer ' + eval(res.text)['token']
        url_cache = datas['url'] %(url_cfg)
        result = requests.get(url=url_cache, headers=headers)
        RedisQueryApi().hset(datas['hset_name'], datas['hset_key'], result.text)

    def get(self, name, url):
        datas = {'url': url,
                'hset_name' : name,
                'hset_key' : u'abstract'}
        self.cache(datas)

if __name__ == '__main__':
    BaseCatch().get(name=u'dashboard', url=u'%s/api/dashboard?cache=0')
