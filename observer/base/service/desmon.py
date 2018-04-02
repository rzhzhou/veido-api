from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import (DMLink, Corpus, )
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class DMLinkData():

    def __init__(self, user):
        self.user = user

    def get_all(self):
        fields = ('id', 'name', 'link', 'kwords', 'fwords', 'status',)

        queryset = DMLink.objects.filter(create_by=self.user).values(*fields).order_by('-update_at')

        return queryset


class DMLinkAdd(Abstract):

    def __init__(self, user, params={}):
        super(DMLinkAdd, self).__init__(params)
        self.user = user

    def add_dmlink(self):
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


class DMLinkEdit(Abstract): 

    def __init__(self, params={}):
        super(DMLinkEdit, self).__init__(params)

    def edit_dmlink(self, did):
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


class DMLinkDelete(Abstract): 

    def __init__(self, user):
        self.user = user

    def del_dmlink(self, did):
        del_id = did

        try:
            DMLink.objects.get(id=del_id).delete()
            return 1
        except Exception as e:
            print(e)
            return 0


class DMWordsData(): 

    def get_all(self):
        fields = ('id', 'riskword', 'invalidword', 'industry__name', )

        queryset = Corpus.objects.all().values(*fields)

        return queryset
