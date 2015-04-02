# -*- coding: utf-8 -*-
import redis


class RedisClient(object):

    conf = None

    """docstring for RedisClient"""
    def __init__(self):
        self.conf = {
            'host': '192.168.1.118',
            'port': '6379',
            'db': 8
        }

    def connect(self):
        pool = redis.ConnectionPool(host=self.conf['host'],
            port=self.conf['port'], db=self.conf['db'])
        return redis.Redis(connection_pool=pool)


def get_instance():
    return RedisClient().connect()

class RedisQueryApi(object):
    """Redis Query Api"""
    instance = None

    def __init__(self):
        self.instance = get_instance()

    def rpop(self, name):
        return self.instance.rpop(name)

    def delete(self, name):
        return self.instance.delete(name)

    def lindex(self, name, index):
        return self.instance.lindex(name, index)

    def llen(self, name):
        return self.instance.llen(name)

    def lpush(self, name, values):
        return self.instance.lpush(name, values)

    def lrange(self, name, start, end):
        return self.instance.lrange(name, start, end)

    def hset(self, name, key, value):
        self.instance.hset(name, key, value)

    def hget(self, name, key):
        return self.instance.hget(name, key)

    def hgetall(self, name):
        return self.instance.hgetall(name)

    def hexists(self, name, key):
        return self.instance.hexists(name, key)

    def scard(self, name):
        return self.instance.scard(name)
        
    def sort(self, name, start=None, num=None, by=None, get=None, desc=False, alpha=False, store=None):
        return self.instance.sort(name, start, num, by, get, desc, alpha, store)
