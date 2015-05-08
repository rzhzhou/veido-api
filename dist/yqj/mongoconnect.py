from pymongo import MongoClient

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
