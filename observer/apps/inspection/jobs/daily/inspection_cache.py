import sys
root_mod = '/home/feng/Project/observer/app'
sys.path.append(root_mod)
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")
reload(sys)
sys.setdefaultencoding( "utf-8" )
import requests
import ConfigParser
from datetime import datetime, timedelta, date

from django.conf import settings
from django_extensions.management.jobs import BaseJob

from observer.apps.yqj.redisconnect import RedisQueryApi

class Job(BaseJob):

    def Cache(self, datas):
        url_cfg = settings.CATCH
        url_cache = '%s/api/dashboard/local-inspection/?catch=0' % (url_cfg)
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

    def homePageCatch(self):
            datas = {
                    'hset_name' : 'inspection',
                    'hset_key' : 'abstract',
                    'username' : 'wuhan',
                    'password' : 'wuhan'
                }
            self.Cache(datas)

    def execute(self):
        # while True:
        self.homePageCatch()
if __name__ == '__main__':
    Job().execute()