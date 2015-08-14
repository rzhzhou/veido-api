import os

from django.conf import settings
from django.http import HttpResponseRedirect

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
            image_url = os.path.join('/media', filename)
    if image_url is None:
        image_url = '/static/img/avatar.jpg'
    return image_url
