from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import DMLink
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


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

