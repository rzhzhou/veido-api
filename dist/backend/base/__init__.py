import os
from ConfigParser import ConfigParser, RawConfigParser

from django.conf import settings
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect

from base.models import User, AnonymousUser, hash_password


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
            #next_url = '/login/' if request.path == '/' else '/login/?next=%s' % request.path
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
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    user = request.myuser
    conf = ConfigParser()
    conf.read(os.path.join(BASE_DIR, "../../sidebar.cfg"))
    username = user.username
    if not conf.has_section(username):
        username = 'test'

    sidebar_name = {
        "news": conf.get(username, "news"),
        "event": conf.get(username, "event"),
        "location": conf.get(username, "location"),
        "custom": conf.get(username, "custom"),
        "site": conf.get(username, "site"),
        "business": eval(conf.get(username, "business"))
    }
    return sidebar_name
