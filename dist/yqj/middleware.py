from yqj.models import AnonymousUser, User

class UserAuthenticationMiddlerware(object):
    def process_request(self, request):
        try:
            pass_id = request.COOKIES['pass_id']
            name = response.COOKIES['name']
            user = User.objects.get(id=pass_id, username=name)
        except (KeyError, User.DoesNotExsist):
            user = AnonymousUser()
        request.myuser = user
