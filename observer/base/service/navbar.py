from observer.base.models import UserNav

from observer.base.service.abstract import Abstract

class NavBarEdit(Abstract):

    def __init__(self, user, params={}):
        super(NavBarEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        nav_ids = getattr(self, 'nav_ids', '')

        for nav_id in nav_ids.split(","):
            if not UserNav.objects.filter(user_id=edit_id, nav_id=nav_id).exists():
                UserNav(
                user_id = edit_id,
                nav_id = nav_id,
                ).save()

        return 200
