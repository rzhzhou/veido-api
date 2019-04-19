from observer.base.models import UserNav, Nav

from observer.base.service.abstract import Abstract

class NavBarData(Abstract):

    def __init__(self, user):
        self.user = user

    def get_navs(self):
        navs = []
        u_navs_ids = UserNav.objects.filter(user=self.user).values_list('nav', flat=True)
        L1 = Nav.objects.filter(id__in=u_navs_ids, level=1).values('name','id').order_by('index')
        if L1:
            for category in L1:
                navs.append({
                    'category': category['name'],
                })

                L2 = Nav.objects.filter(id__in=u_navs_ids, level=2, parent_id=category['id']).values('name', 'id', 'href', 'icon').order_by('index')
                if L2:
                    for title in L2:
                        childrens = Nav.objects.filter(id__in=u_navs_ids, level=3, parent_id=title['id']).values_list('name')
                        navs.append({
                            'icon': title['icon'],
                            'title': title['name'],
                            'href': '' if not title['href'] else title['href'],
                            'children': list(map(lambda x: {
                                'title': x['name'],
                                'href': x['href'],
                            }, Nav.objects.filter(id__in=u_navs_ids, level=3, parent_id=title['id']).values('name', 'href').order_by('index'))) if childrens else ''
                        })

        return navs


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

    # 对比用户前后路由差异
        # 用户已存在的权限id
        origin_nav_ids = list(map(str, list(UserNav.objects.filter(user_id=edit_id).exclude(nav__level=-1).values_list('nav_id', flat=True))))
        # 用户要分配权限id
        edit_nav_ids = nav_ids.split(',')

        diff_nav_ids = list(set(origin_nav_ids).difference(set(edit_nav_ids))) + list(set(edit_nav_ids).difference(set(origin_nav_ids)))

        if diff_nav_ids:
            for nav_id in diff_nav_ids:
                child_ids = Nav.objects.filter(parent_id=nav_id, level=-1).values_list('id', flat=True)

                if not UserNav.objects.filter(user_id=edit_id, nav_id=nav_id).exists():
                    UserNav(user_id=edit_id, nav_id=nav_id).save()
                    if child_ids.exists():
                        if not UserNav.objects.filter(user_id=edit_id, nav_id__in=child_ids).exists():
                            for child_id in child_ids:
                                UserNav(user_id=edit_id, nav_id=child_id).save()
                else:
                    UserNav.objects.filter(user_id=edit_id, nav_id=nav_id).delete()
                    if child_ids.exists():
                        if UserNav.objects.filter(user_id=edit_id, nav_id__in=child_ids).exists():
                            for child_id in child_ids:
                                UserNav.objects.filter(user_id=edit_id, nav_id=child_id).delete()

        return 200

class RouteData(Abstract):

    def __init__(self, user):
        self.user = user

    def get_routers(self):
        routers = []
        u_navs_ids = UserNav.objects.filter(user=self.user).values_list('nav', flat=True)
        routes = Nav.objects.filter(id__in=u_navs_ids).exclude(level=1).values('id', 'href', 'component', 'nav_type').order_by('index')
        j = 0
        for i, route in enumerate(routes):
            if route['href'] == '':
                j+=1
            else:
                routers.append({
                    'path': route['href'],
                    'alias': '/' if i - j == 0 else '',
                    'component': route['component'],
                    'meta': { 'pageAside': True } if route['nav_type'] else { 'pageAside': False },
                })

        return routers
