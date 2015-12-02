# -*- coding: utf-8 -*-
from rest_framework.response import Response
from observer.utils.connector.redisconnector import RedisQueryApi


null = ''
def read_cache(view_func):
    global null

    def wrapper(view_class, *args, **kwargs):
        parameter = view_class.request.GET
        cache = parameter['cache'] if parameter.has_key('cache') else 1

        ''' if cache=1,read redis,else read mysql'''
        if cache:
            data = RedisQueryApi().hget('dashboard', 'abstract')
            if data:
                return Response(eval(data))
        return view_func(view_class, *args, **kwargs)
    return wrapper