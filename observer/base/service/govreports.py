from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from observer.apps.hqi.models import GovReports, Area
import os
from observer.base.service.abstract import Abstract


class GovReportsData(Abstract):

    def __init__(self, params={}):
        super(GovReportsData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'title', 'content', 'year', 'area_id', 'area__level')

        cond = {
            'area__level': getattr(self, 'level', None),
            'year': getattr(self, 'year', None),
            'area': getattr(self, 'area', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = GovReports.objects.using('hqi').filter(**args)

        return queryset.values(*fields).order_by('-year')


class GovReportsAdd(Abstract):

    def __init__(self, user, params={}):
        super(GovReportsAdd, self).__init__(params)
        self.user = user

    def add(self):
        title = getattr(self, 'title', '')
        content = getattr(self, 'content', '')
        year = getattr(self, 'year', '')
        areas = getattr(self, 'areas', '')

        if not title or not areas or not content or not year:
            return 400
        govreports = GovReports(
            title = title,
            content = content,
            year = year,
            area_id = areas,
        )
        govreports.save(using='hqi')
        return 200


class GovReportsDelete(Abstract):
    def __init__(self, user, params={}):
        super(GovReportsDelete, self).__init__(params)
        self.user = user

    def delete(self, cid):
        del_ids = cid
        print(del_ids)

        for id in del_ids.split(","):
            GovReports.objects.using('hqi').filter(id=id).delete()


class GovReportsEdit(Abstract):

    def __init__(self, user, params={}):
        super(GovReportsEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid

        title = getattr(self, 'title', '')
        content = getattr(self, 'content', '')
        year = getattr(self, 'year', '')
        areas = getattr(self, 'areas', '')
        if not title or not areas or not content or not year:
            return 400

        area = Area.objects.using('hqi').filter(id=areas)    #返回单个id

        govreports = GovReports.objects.using('hqi').get(id=edit_id)
        govreports.title = title
        govreports.content = content
        govreports.year = year
        govreports.save()
        return 200
