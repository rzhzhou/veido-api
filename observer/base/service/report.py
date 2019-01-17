import os
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F
from django.contrib.auth.models import Group

from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from observer.base.service.abstract import Abstract
from observer.base.models import NewsReport


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
            'pubtime__lte': getattr(self, 'endtime', None),
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

        queryset = queryset.values(*fields).order_by('-year', '-period')

        return queryset


class NewsReportSuzhou(Abstract):

    def __init__(self, params={}):
        super(NewsReportSuzhou, self).__init__(params)

    def get_news_report_list(self, search_value):
        fields = ('id', 'group__name', 'year', 'period', 'news_type', 'pubtime', 'publisher')

        args = {}

        # 显示苏州市质监局的舆情报告
        group_id = Group.objects.get(name='苏州市质监局').id

        if not search_value:
            queryset = NewsReport.objects.filter(group_id=group_id).values(*fields).order_by('-year', '-period')
        else:
            queryset = NewsReport.objects.filter(Q(year=search_value) | Q(period=search_value) | Q(news_type=search_value)).values(*fields)
            queryset = queryset.filter(group_id=group_id).order_by('-year', '-period')

        return queryset


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

class NewsReportDelete(Abstract):

    def __init__(self, user, params={}):
        super(NewsReportDelete, self).__init__(params)
        self.user = user

    def delete(self, cid):
        file = NewsReport.objects.filter(id=cid).values_list('file', flat=True)[0]
        # 删除指定目录的文件
        os.remove(file)
        # 删除数据库记录
        NewsReport.objects.filter(id=cid).delete()
