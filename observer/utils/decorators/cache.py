# -*- coding: utf-8 -*-
from observer.apps.yqj.redisconnect import RedisQueryApi

def read_cache(view_func):

    def wrapper(request, *args, **kwargs):
        data = RedisQueryApi().hget('name', 'key')
        if data:
            return Response(eval(data))
        return view_func(request, *args, **kwargs)
    return wrapper