from pymongo import MongoClient
from datetime import datetime, timedelta

_CONN = None
class MongoClient(object):

    MONGO_CONN_STR = "mongodb://192.168.1.118:27017"
    _conn = MongoClient(MONGO_CONN_STR)
    db = _conn["crawler"]

def mongo_db():
    return _CONN  if _CONN else MongoClient().db

_db = mongo_db()
class MongodbQuerApi(object):

    def __init__(self, table):
        self.table =table


    def save(self, dct):

        def insert():
            _db[self.table].insert(dct)

        insert()

    def find_one(self, dct):

        def result():
            return _db[self.table].find_one(dct)

        return result()

    def update(self, term, dct):

        def result():
            _db[self.table].update(term,dct)

        result()

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
