from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
import os
from observer.base.service.abstract import Abstract
from observer.base.models import NewsReport
from django.contrib.auth.models import Group


class NewsReportUpload(Abstract):

    def __init__(self, user, params={}):
        super(NewsReportUpload, self).__init__(params)
        self.user = user

    def add(self):
        group_id = getattr(self, 'group_id', '')
        year = getattr(self, 'year', '')
        period = getattr(self, 'period', '')
        news_type = getattr(self, 'news_type', '')
        publisher = getattr(self, 'publisher', '')
        file = getattr(self, 'file', '')

        NewsReport(group_id=group_id, year=year, period=period, news_type=news_type, publisher=publisher, file=file).save()

        return 200

class NewsReportData(Abstract):

    def __init__(self, user, params={}):
        super(NewsReportData, self).__init__(params)
        self.user = user

    def get_all(self):
        fields = ('id', 'group__name', 'year', 'period', 'news_type', 'pubtime', 'publisher')

        cond = {
            'group_id': getattr(self, 'group_id', None),
            'year': getattr(self, 'year', None),
            'period': getattr(self, 'period', None),
            'news_type': getattr(self, 'news_type', None),
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = NewsReport.objects.filter(**args)

        if self.user.is_active:
            group_ids = Group.objects.filter(user=self.user).values_list('id', flat=True)

        # 如果当前操作的不是'超级管理员'
        if 2 not in group_ids:
            group_list = list(group_ids)
            group_list.remove(3)
            queryset = queryset.filter(group=group_list[0])

        queryset = queryset.values(*fields).order_by('-period')

        return queryset
