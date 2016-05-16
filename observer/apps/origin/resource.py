# -*- coding: utf-8 -*-
import pytz, xlrd
from datetime import datetime

from django.conf import settings

from import_export.widgets import DateWidget, ForeignKeyWidget, ManyToManyWidget
from import_export import widgets
from import_export import resources, fields
from observer.apps.base.models import Area
from observer.apps.origin.models import InspectionPublisher, Inspection
from observer.apps.riskmonitor.models import Industry, Enterprise


class InspectionResources(resources.ModelResource):
    pubtime = fields.Field(attribute='pubtime', column_name=u'发布日期')
    title = fields.Field(attribute='title', column_name=u'标题')
    author = fields.Field(attribute='author', column_name=u'作者')
    url = fields.Field(attribute='url', column_name=u'链接')
    qualitied = fields.Field(attribute='qualitied', column_name=u'合格率')
    reprinted = fields.Field(attribute='reprinted', column_name=u'转载数')
    content = fields.Field(attribute='content', column_name=u'正文')
    publisher = fields.Field(
        column_name=u'文章发布者',
        attribute='publisher',
        widget=ForeignKeyWidget(InspectionPublisher, 'name'))
    area = fields.Field(
        column_name=u'地域',
        attribute='area',
        widget=ManyToManyWidget(Area, ' ', 'name'))
    industry = fields.Field(
        column_name=u'行业',
        attribute='industry',
        widget=ManyToManyWidget(Industry, ' ', 'name'))
    enterprise = fields.Field(
        column_name=u'企业',
        attribute='enterprise',
        widget=ManyToManyWidget(Enterprise, ' ', 'name'))

    class Meta:
        model = Inspection
        fields = ('id', 'pubtime', 'title', 'url', 'qualitied', 'publisher',
            'area', 'industry', 'enterprise')
        export_order = ('id', 'pubtime', 'title', 'url', 'qualitied', 'publisher',
            'area', 'industry', 'enterprise')

    def before_save_instance(self, instance, dry_run):
        if isinstance(instance.pubtime, basestring):
            instance.pubtime = datetime.strptime(instance.pubtime, '%Y-%m-%d %H:%M:%S')
        elif isinstance(instance.pubtime, float):
            instance.pubtime = xlrd.xldate.xldate_as_datetime(instance.pubtime, 0)

