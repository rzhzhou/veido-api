from observer.base.models import UserNav, Nav

from observer.base.service.abstract import Abstract

class NavBarEdit(Abstract):

    def __init__(self, user, params={}):
        super(NavBarEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        nav_ids = getattr(self, 'nav_ids', '')

        # 验证是否有操作权限
        if not self.user.is_active:
            return 203

        # 验证是否有操作权限
        if not self.user.is_superuser:
            return 204

        origin_nav_ids = list(map(str, list(UserNav.objects.filter(user_id=edit_id).exclude(nav__level=-1).values_list('nav_id', flat=True))))
        edit_nav_ids = nav_ids.split(',')

        diff_nav_ids = list(set(origin_nav_ids).difference(set(edit_nav_ids))) + list(set(edit_nav_ids).difference(set(origin_nav_ids)))

        if diff_nav_ids:
            for nav_id in diff_nav_ids:
                child_ids = Nav.objects.filter(parent_id=nav_id, level=-1).values_list('id', flat=True)

                if not UserNav.objects.filter(user_id=edit_id, nav_id=nav_id).exists():
                    UserNav(user_id=edit_id, nav_id=nav_id).save()
                    if child_ids.exists() and not UserNav.objects.filter(user_id=edit_id, nav_id__in=child_ids).exists():
                        for child_id in child_ids:
                            UserNav(user_id=edit_id, nav_id=child_id).save()
                else:
                    UserNav.objects.filter(user_id=edit_id, nav_id=nav_id).delete()
                    if child_ids.exists() and UserNav.objects.filter(user_id=edit_id, nav_id__in=child_ids).exists():
                        for child_id in child_ids:
                            UserNav(user_id=edit_id, nav_id=child_id).delete()

        return 200
