import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")

from observer.utils.cache.cache import BaseCatch
from observer.apps.yqj.redisconnect import RedisQueryApi


class Job(BaseCatch):
    URL = '%s/api/dashboard/local-inspection/?cache=0'

    def execute(self):
        self.get(name='risk', url=self.URL)

if __name__ == '__main__':
    Job().execute()