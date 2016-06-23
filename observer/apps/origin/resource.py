# -*- coding: utf-8 -*-
import pytz
import xlrd
from datetime import datetime

from django.conf import settings

from import_export.widgets import DateWidget, ForeignKeyWidget, ManyToManyWidget
from import_export import widgets
from import_export import resources, fields
from observer.apps.base.models import Area
from observer.apps.origin.models import Industry, Enterprise, InspectionPublisher, Inspection


class EnterpriseResources(resources.ModelResource):
    name = fields.Field(attribute='name', column_name=u'企业名')

    area = fields.Field(
        column_name=u'地域',
        attribute='area',
        widget=ForeignKeyWidget(Area, 'name'))

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'area')
        export_order = ('id', 'name', 'area')

    def before_save_instance(self, instance, dry_run):
        queryset = Enterprise.objects.filter(name=instance.name)
        if queryset:
            return


class InspectionPublisherResources(resources.ModelResource):
    name = fields.Field(attribute='name', column_name=u'抽检单位')

    class Meta:
        model = InspectionPublisher
        fields = ('id', 'name')
        export_order = ('id', 'name')

    def before_save_instance(self, instance, dry_run):
        queryset = InspectionPublisher.objects.filter(name=instance.name)
        if queryset:
            return


class InspectionResources(resources.ModelResource):
    pubtime = fields.Field(attribute='pubtime', column_name=u'发布日期')
    title = fields.Field(attribute='title', column_name=u'标题')
    url = fields.Field(attribute='url', column_name=u'链接')
    qualitied = fields.Field(attribute='qualitied', column_name=u'合格率')
    content = fields.Field(attribute='content', column_name=u'正文')
    unitem = fields.Field(attribute='unitem', column_name=u'不合格项')
    brand = fields.Field(attribute='brand', column_name=u'商标')
    product = fields.Field(attribute='product', column_name=u'产品种类')
    publisher = fields.Field(
        column_name=u'抽检单位',
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
        if not instance.pubtime:
            instance.pubtime = datetime.now()
        elif isinstance(instance.pubtime, basestring):
            instance.pubtime = datetime.strptime(
                instance.pubtime, '%Y-%m-%d %H:%M:%S')
        elif isinstance(instance.pubtime, float):
            instance.pubtime = xlrd.xldate.xldate_as_datetime(
                instance.pubtime, 0)
