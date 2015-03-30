from django.http import HttpResponseRedirect
from yqj.models import User, AnonymousUser, hash_password

def authenticate(username, raw_password):
    try:
        user = User.objects.get(username=username)
        coded = hash_password(raw_password, user.salt)
        if user.password == coded:
            return user
        else:
            return AnonymousUser()
    except User.DoesNotExsis:
        return AnonymousUser()


def login_required(view_func):
    
    def wrapper(request, *args, **kwargs):
        if not request.myuser.is_authenticated():
            #next_url = '/login/' if request.path == '/' else '/login/?next=%s' % request.path
            next_url = '/login/'
            return HttpResponseRedirect(next_url)
        return view_func(request, *args, **kwargs)
    return wrapper
