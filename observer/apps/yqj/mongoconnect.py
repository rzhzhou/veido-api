from django.conf import settings
from pymongo import MongoClient
from datetime import datetime, timedelta

_CONN = None
class MongoClients(object):

    def __init__(self):
        self._conn = MongoClient(settings.MONGO_CONN_STR)
        self.db = self._conn["crawler"]

    def mongo_db(self):
        return _CONN  if _CONN else self.db


class MongodbQuerApi(object):

    def __init__(self, table):
        self.table =table
        self._db = MongoClients().mongo_db()

    def save(self, dct):

        def insert():
            self._db[self.table].insert(dct)

        insert()

    def find_one(self, dct):

        def result():
            return self._db[self.table].find_one(dct)

        return result()

    def update(self, term, dct):

        def result():
            self._db[self.table].update(term,dct)

        result()

    def delete(self, dct):

        def remove():
            self._db[self.table].remove(dct)

        remove()

class CrawlerTask(object):

    def __init__(self, key, mongo_task, task_type):
        self.key = key
        self.mongo_task = mongo_task
        self.task_type = task_type

    def insert_task(self, data):
        crawler_conf = {
            "type" : data.get('type',''),
            "status" : data.get('status', 0),
            "priority" : data.get('priority',3),
            "interval" : data.get('interval', 7200),
            "update_time" : datetime.utcnow(),
            "lastrun": datetime.utcnow(),
            "nextrun": datetime.utcnow() - timedelta(days=2),
            "crtetime": datetime.utcnow(),
            "timeout": 3600,
            "key": self.key,
            "data" : {
                "source_type" : self.task_type,
                "source" : data.get('source', '')}
        }

        if not MongodbQuerApi(self.mongo_task).find_one({'type':data.get('type',''),
                    'key': self.key}):
            MongodbQuerApi(self.mongo_task).save(crawler_conf)

    def type_task(self):
        types = {
            "baidu": "zjld.baidu.newstitle",
            "weibo": "zjld.weibo.newstitle",
            "sogou": "zjld.sogou.keywords",
            "sogou_news": "zjld.sogou.newstitle",
        }
        weibodata = {
            "interval": 21600,
            "type": types.get('weibo'),
            "source": 'weibo'
        }

        weibo = self.insert_task(weibodata)

        baidudata = {
            "type": types.get('baidu'),
            "source": 'baidu',
        }
        baidu = self.insert_task(baidudata)

        weixindata = {
            "type": types.get('sogou'),
            "source": 'sogou'
        }
        weixin = self.insert_task(weixindata)

        sogou_newsdata = {
            "type": types.get("sogou_news"),
            "source": "sogou",
        }
        sogou_news = self.insert_task(sogou_newsdata)

    def del_task(self):
        task_index = {
            "data.source_type" : self.task_type,
            "$or" : [{"key" : self.key}, {"data.key" : self.key}],
        }
        MongodbQuerApi(self.mongo_task).delete(task_index)

    def update_task(self, old_keyword):
        task_index = {
            "data.source_type" : self.task_type,
            "$or" : [{"key" : old_keyword},{"data.key" : old_keyword}],
        }
        MongodbQuerApi(self.mongo_task).delete(task_index)
        self.type_task()




