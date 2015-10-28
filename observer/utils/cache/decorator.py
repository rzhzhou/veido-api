# -*- coding: utf-8 -*-
from observer.apps.yqj.redisconnect import RedisQueryApi

class ReadCache(object):

    def __init__(self):
        pass

    def __call__(self):
        def wrapped(*args, **kargs):
            data = RedisQueryApi().hget('abstract')
            if data:
                return Response(eval(data))
        return wrapped
