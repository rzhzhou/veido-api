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


''' set token black list,  when user logout  '''
def token(view_func):

    def wrapper(request, *args, **kwargs):
        username = request.user.username
        jwt = eval(request.body)['token']
        data = RedisQueryApi().keys(username + '*')
        if data:
            for item in data:
                value = RedisQueryApi().get(item)
                if jwt == value:
                    return HttpResponse(status=403)
        else:
            return view_func(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return wrapper