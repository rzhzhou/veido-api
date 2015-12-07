import os

from django.conf import settings
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response

from observer.apps.base.models import User, AnonymousUser, hash_password
from observer.apps.config.models import SettingsOne
from observer.utils.connector.mysql import query_one
from observer.utils.connector.redisconnector import RedisQueryApi
from rest_framework.response import Response


def authenticate(username, raw_password):
    try:
        user = User.objects.get(username=username)
        coded = hash_password(raw_password, user.salt)
        if user.password == coded:
            return user
        else:
            return AnonymousUser()
    except User.DoesNotExist:
        return AnonymousUser()


def login_required(view_func):

    def wrapper(request, *args, **kwargs):
        if not request.myuser.is_authenticated():
            # next_url = '/login/' if request.path == '/' else '/login/?next=%s' % request.path
            next_url = '/login/'
            return HttpResponseRedirect(next_url)
        return view_func(request, *args, **kwargs)
    return wrapper


def get_user_image(user):
    image_url = None
    for filename in os.listdir(settings.MEDIA_ROOT):
        if os.path.splitext(filename)[0] == str(user.id):
            image_url = os.path.join('/../media', filename)
    if image_url is None:
        image_url = '/static/img/avatar.jpg'
    return image_url


def set_logo(obj):
    if isinstance(obj, dict):
        obj['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
    else:
        obj.publisher.photo = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
    return obj


def xls_to_response(wb, fname):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


def sidebarUtil(request):
    user = request.user
    try:
        user = User.objects.get(username=user.username)
        sidebar = SettingsOne.objects.filter(user=user)
        result = {}
        for i in sidebar:
            items = {}
            items[i.name] = i.value
            result.update(items)
        result.update({'user': user.username})
        return result
    except:
        return {
        'user': user.username,
        'news': '',
        'event': '',
        'location': '',
        'custom': '',
        'site': '',
        'business': []
        }


def token(view_func):

    def wrapper(view_class, *args, **kwargs):
        parameter = view_class.request
        username = parameter.user.username
        jwt = parameter.META['HTTP_AUTHORIZATION']
        data = RedisQueryApi().keys(username+'*')
        if data:
            for item in data:
                value = RedisQueryApi().get(item)
                if jwt == value:
                    return HttpResponse(status=403)
        else:
            return view_func(view_class, *args, **kwargs)
        return view_func(view_class, *args, **kwargs)
    return wrapper