# -*- coding: utf-8 -*-
from rest_framework.response import Response
from observer.apps.yqj.redisconnect import RedisQueryApi

def read_cache(view_func):

    def wrapper(view_class, *args, **kwargs):
        data = RedisQueryApi().hget('event', 'abstract')
        if data:
            return Response(eval(data))
        return view_func(request, *args, **kwargs)
    return wrapper