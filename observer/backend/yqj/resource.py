# -*- coding: utf-8 -*-
from import_export.widgets import DateWidget
from datetime import datetime
from import_export import resources, fields
from django.conf import settings
import pytz, xlrd


class InspectionResources(resources.ModelResource):
    pubtime = fields.Field(attribute='pubtime', column_name=u'发布日期')
    name = fields.Field(attribute='name', column_name=u'标题')
    url = fields.Field(attribute='url', column_name=u'链接')
    source = fields.Field(attribute='source', column_name=u'发布者')
    qualitied = fields.Field(attribute='qualitied', column_name=u'合格率')
    product = fields.Field(attribute='product', column_name=u'产品种类')
    province = fields.Field(attribute='province', column_name=u'省份')
    city = fields.Field(attribute='city', column_name=u'市')

    class Meta:
    	from admin import ZJInspection
        model = ZJInspection
        fields = ('id', 'name', 'url', 'source', 'product', 'pubtime', 'province', 'city', 'qualitied')
        export_order = ('id', 'name', 'url', 'source', 'pubtime', 'province', 'city', 'qualitied', 'product')

    def dehydrate_pubtime(self, zjinspection):
        if isinstance(zjinspection.pubtime, datetime):
            if zjinspection.pubtime.tzinfo is None:
                return zjinspection.pubtime.strftime('%Y-%m-%d %H:%M:%S')
            elif zjinspection.pubtime.tzinfo == pytz.utc:
                return zjinspection.pubtime.astimezone(
                    pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ""

    def before_save_instance(self, instance, dry_run):
        if instance.create_at is None:
            instance.create_at = datetime.now()
        instance.update_at = datetime.now()
        if isinstance(instance.pubtime, basestring):
            instance.pubtime = datetime.strptime(instance.pubtime, '%Y-%m-%d %H:%M:%S')
        elif isinstance(instance.pubtime, float):
            instance.pubtime = xlrd.xldate.xldate_as_datetime(instance.pubtime, 0)