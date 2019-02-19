from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from django.contrib.auth.models import Group
from observer.base.models import (DMLink, CorpusCategories, Article )
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


class DMWordsData(Abstract):

    def __init__(self, user, params):
        self.user = user
        super(DMWordsData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'status', 'keyword', 'category_id', 'industry_id')

        cond = {
            'category_id': getattr(self, 'category', None),
            'status': getattr(self, 'status', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = CorpusCategories.objects.filter(**args).values(*fields)
        
        # 判断当前用户是否为武汉深度网科技有限公司成员，然后取出该用户管理的资料
        group_ids = Group.objects.filter(user=self.user).values_list('id', flat=True)
        if 4 in group_ids and 3 in group_ids:
            queryset = CorpusCategories.objects.filter(**args).filter(user_id = self.user.id).values(*fields)

        
        return queryset


class DMWordsFocusData(object):

    def __init__(self, user):
        self.user = user

    def get_all(self):

        fields = ('id', 'keyword', 'startTime', 'stopTime')
        status = 1
        queryset = CorpusCategories.objects.filter(user_id = self.user.id, status=status).values(*fields)
 
        return queryset


class DMWordsDelete(object):
    def __init__(self, user):
        self.user = user

    def delete(self, did):
        Arr_id = did

        for a_id in Arr_id.split(','):
            corCategory = CorpusCategories.objects.get(id=a_id)
            corCategory.status = 2
            corCategory.save()

        return 200

class MonitorInformationData(object):
    def __init__(self, user):
        self.user = user

    def get_all(self, did):
        fields = ('title', 'url', 'pubtime', 'source', 'areas__name')

        result = Article.objects.filter(corpus_id=did).values(*fields)

        return result

