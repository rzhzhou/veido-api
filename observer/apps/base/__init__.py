import os

from django.conf import settings
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect

from observer.apps.base.models import User, AnonymousUser, hash_password
from observer.utils.connector.mysql import query_one


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
    user = request.myuser
    username = user.username

    sidebar_name = {
        "news": query_one(user=login_user, confname='news'),
        "event": query_one(user=login_user, confname='event'),
        "location": query_one(user=login_user, confname='location'),
        "custom": query_one(user=login_user, confname='custom'),
        "site": query_one(user=login_user, confname='site'),
        "business": eval(query_one(user=login_user, confname='business'))
    }
    return sidebar_name
