import sys
import os
root_mod = '/home/feng/Project/observer/api'
sys.path.append(root_mod)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")
import requests

from django.conf import settings
from django_extensions.management.jobs import BaseJob

from observer.apps.yqj.redisconnect import RedisQueryApi
reload(sys)
sys.setdefaultencoding("utf-8")

class BaseCatch(BaseJob):

    def Cache(self, datas):
        url_cfg = settings.CACHE
        url_cache = '%s/api/%s/?type=abstract&catch=0' % (url_cfg, datas['hset_name'])
        result = requests.get(url=url_cache)
        RedisQueryApi().hset(datas['hset_name'], datas['hset_key'], str(result.text))

    def get(self, name):
            datas = {
                    'hset_name' : name,
                    'hset_key' : 'abstract'
                }
            self.Cache(datas)

if __name__ == '__main__':
    BaseCatch().get(name='event')
