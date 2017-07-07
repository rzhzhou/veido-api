# -*- coding: utf-8 -*-
import pytz
import xlrd
from datetime import datetime

from django.conf import settings

from import_export.widgets import DateWidget, ForeignKeyWidget
from import_export import widgets
from import_export import resources, fields
from observer.apps.penalty.models import AdministrativePenalties

class AdministrativePenaltiesResources(resources.ModelResource):
    pubtime = fields.Field(attribute='pubtime', column_name=u'发布日期')
    title = fields.Field(attribute='title', column_name=u'标题')
    url = fields.Field(attribute='url', column_name=u'链接')
    content = fields.Field(attribute='content', column_name=u'正文')
    publisher = fields.Field(attribute='publisher', column_name=u'发布者')
    case_name = fields.Field(attribute='case_name', column_name=u'案件名称')
    illegal_behavior = fields.Field(attribute='illegal_behavior', column_name=u'违法行为')
    punishment_basis = fields.Field(attribute='punishment_basis', column_name=u'处罚依据')
    punishment_result = fields.Field(attribute='punishment_result', column_name=u'处罚结果')
    penalty_organ = fields.Field(attribute='penalty_organ', column_name=u'处罚机关')
    credit_code = fields.Field(attribute='credit_code', column_name=u'统一社会信用代码')
    area = fields.Field(attribute='area', column_name=u'地域')
    industry = fields.Field(attribute='industry', column_name=u'行业')
    enterprise=fields.Field(attribute='enterprise', column_name=u'处罚企业')

    class Meta:
        model = AdministrativePenalties
        fields = ('id','title', 'url', 'publisher', 'pubtime', 'credit_code', 'area','industry','enterprise','penalty_organ','case_name','illegal_behavior','punishment_basis','punishment_result')
        export_order = ('id','title', 'url', 'publisher', 'pubtime', 'credit_code', 'area','industry','enterprise','penalty_organ','case_name','illegal_behavior','punishment_basis','punishment_result')

    def before_save_instance(self, instance, dry_run, temp=''):
        if not instance.pubtime:
            instance.pubtime = datetime.now()
        elif isinstance(instance.pubtime, basestring):
            instance.pubtime=str(instance.pubtime).split('+')[0]
            instance.pubtime = datetime.strptime(
                str(instance.pubtime), '%Y-%m-%d %H:%M:%S')
        elif isinstance(instance.pubtime, float):
            instance.pubtime = xlrd.xldate.xldate_as_datetime(
                instance.pubtime, 0)
