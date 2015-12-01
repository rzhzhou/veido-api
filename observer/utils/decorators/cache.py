# -*- coding: utf-8 -*-
from rest_framework.response import Response
from observer.utils.connector.redisconnector import RedisQueryApi

def read_cache(view_func):

    def wrapper(view_class, *args, **kwargs):
        data = RedisQueryApi().hget('event', 'abstract')
        if data:
            return Response(eval(data))
        return view_func(view_class, *args, **kwargs)
    return wrapper
