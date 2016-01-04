# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development")

from observer.utils.cache.cache import BaseCatch


class Job(BaseCatch):
    # URL = '%s/api/event/?type=abstract&catch=0'

    def execute(self):
        self.get(name=u'dashboard', url=u'%s/api/dashboard?cache=0')


if __name__ == '__main__':
    Job().execute()

