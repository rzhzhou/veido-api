from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import DMLink
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class DMLinkData():  # 获取系统用户

    def __init__(self, user):
        self.user = user

    def get_all(self):
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_active', 'is_superuser', 'last_login', 'date_joined')

        queryset = DMLink.objects.values(*fields)

        if self.user.is_active:
            if self.user.is_superuser:
                list(map(lambda x: x.update({'flag': 1}), queryset))
            else:
                q1 = queryset.exclude(id=self.user.id)
                list(map(lambda x: x.update({'flag': 0}), q1))

                q2 = queryset.filter(id=self.user.id)
                list(map(lambda x: x.update({'flag': 1}), q2))
                queryset = list(chain(q1, q2))
        else:
            list(map(lambda x: x.update({'flag': 0}), queryset))

        return queryset


class DMLinkAdd(Abstract):

    def __init__(self, user, params={}):
        super(DMLinkAdd, self).__init__(params)
        self.user = user

    def add_user(self):
        name = getattr(self, 'name')
        link = getattr(self, 'link')
        kwords = getattr(self, 'kwords', '')
        fwords = getattr(self, 'fwords', '')
        remarks = getattr(self, 'remarks', '')

        if not name:
            return -1

        if not link:
            return -2

        try:
            DMLink(
                name=name,
                link=link,
                kwords=kwords,
                fwords=fwords,
                create_at=datetime.now(),
                update_at=datetime.now(),
                status=0,
                create_by=self.user,
            ).save()
            return 1
        except Exception as e:
            print(e)
            return 0


class DMLinkEdit(Abstract):  # 修改用户

    def __init__(self, params={}):
        super(DMLinkEdit, self).__init__(params)

    def edit_user(self, did):
        edit_id = did
        name = getattr(self, 'name')
        link = getattr(self, 'link')
        kwords = getattr(self, 'kwords', '')
        fwords = getattr(self, 'fwords', '')
        remarks = getattr(self, 'remarks', '')

        if not name:
            return -1

        if not link:
            return -2

        try:
            dmlink = DMLink.objects.get(id=edit_id)
            dmlink.name = name
            dmlink.link = link
            dmlink.kwords = kwords
            dmlink.fwords = fwords
            dmlink.update_at = datetime.now()
            dmlink.status = 0
            dmlink.save()
            return 1
        except Exception as e:
            print(e)
            return 0


class DMLinkDelete(Abstract):  # 删除用户

    def __init__(self, user):
        self.user = user

    def del_user(self, did):
        del_id = did

        try:
            DMLink.objects.get(id=del_id).delete()
            return 1
        except Exception as e:
            print(e)
            return 0


