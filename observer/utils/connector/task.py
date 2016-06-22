#coding:utf-8

from datetime import datetime, timedelta
import sys
import os
root_mod = '/home/jshliu/Project/observer/api'
sys.path.append(root_mod)
import django#--Django 1.7--
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
django.setup()#--Django 1.7--


from observer.apps.base.models import Task

_CONN = None


class CrawlerTask(object):

    def __init__(self, key, mongo_task, task_type):
        self.key = key
        self.mongo_task = mongo_task
        self.task_type = task_type

    def insert_task(self, data):
        crawler_conf = {
            "app": 'observer',
            "status": data.get('status', 0),
            "priority": data.get('priority', 3),
            "update_time": datetime.utcnow(),
            "lastrun": datetime.utcnow(),
            "nextrun": datetime.utcnow() - timedelta(days=2),
            "crtetime": datetime.utcnow(),
            "timeout": 3600,
            "key": self.key,
            "data": {
                "source_type": self.task_type,
                "source": data.get('source', '')}}

        if not MongodbQuerApi(self.mongo_task).find_one({
                'type': data.get('type', ''),
                'key': self.key}):
            MongodbQuerApi(self.mongo_task).save(crawler_conf)

    def type_task(self):

        baidudata = {
            "type": types.get('baidu'),
            "source": 'baidu'}
        baidu = self.insert_task(baidudata)


    def del_task(self):
        task_index = {
            "data.source_type": self.task_type,
            "$or": [{"key": self.key}, {"data.key": self.key}]}
        MongodbQuerApi(self.mongo_task).delete(task_index)

    def update_task(self, old_keyword):
        task_index = {
            "data.source_type": self.task_type,
            "$or": [{"key": old_keyword}, {"data.key": old_keyword}]}
        MongodbQuerApi(self.mongo_task).delete(task_index)
        self.type_task()

if __name__ == '__main__':
    print Task.objects.filter(id=999).using("crawler")