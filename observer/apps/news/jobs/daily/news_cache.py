import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")

from observer.utils.cache.cache import BaseCatch


class Job(BaseCatch):
    URL = '%s/api/news/?type=abstract&catch=0'

    def execute(self):
        self.get(name='news', url=self.URL)

if __name__ == '__main__':
    Job().execute()