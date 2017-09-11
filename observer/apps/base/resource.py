# -*- coding: utf-8 -*-
import pytz
import xlrd
from datetime import datetime
from django.conf import settings
from import_export.widgets import DateWidget, ForeignKeyWidget, ManyToManyWidget
from import_export import widgets
from import_export import resources, fields
from observer.apps.base.models import Area, Industry, Enterprise, InspectionPublisher, Inspection


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

    def save_instance(self, instance, dry_run=False, temp=""):
        queryset = Enterprise.objects.filter(name=instance.name)
        if not queryset:
            instance.save()


class InspectionPublisherResources(resources.ModelResource):
    name = fields.Field(attribute='name', column_name=u'抽检单位')

    class Meta:
        model = InspectionPublisher
        fields = ('id', 'name')
        export_order = ('id', 'name')

    def save_instance(self, instance, dry_run, temp=""):
        queryset = InspectionPublisher.objects.filter(name=instance.name)
        if not queryset:
            instance.save()


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
    enterprise_qualified = fields.Field(
        column_name=u'合格企业',
        attribute='enterprise_qualified',
        widget=ManyToManyWidget(Enterprise, ' ', 'name'))
    enterprise_unqualified = fields.Field(
        column_name=u'不合格企业',
        attribute='enterprise_unqualified',
        widget=ManyToManyWidget(Enterprise, ' ', 'name'))

    class Meta:
        model = Inspection
        fields = ('id', 'pubtime', 'title', 'url', 'qualitied', 'publisher',
                  'area', 'industry', 'enterprise_qualified', 'enterprise_unqualified')
        export_order = ('id', 'pubtime', 'title', 'url', 'qualitied', 'publisher',
                        'area', 'industry', 'enterprise_qualified', 'enterprise_unqualified')

    def before_save_instance(self, instance, dry_run, temp=''):
        if instance.qualitied < 0 or instance.qualitied >1:
            qualitied=str(instance.qualitied)
            raise ValueError('当前合格率:'+qualitied+',合格率区间应在(0 ~ 1)!')
        if not instance.pubtime:
            instance.pubtime = datetime.now()
        elif isinstance(instance.pubtime, basestring):
            instance.pubtime=str(instance.pubtime).split('+')[0]
            instance.pubtime = datetime.strptime(
                str(instance.pubtime), '%Y-%m-%d %H:%M:%S')
        elif isinstance(instance.pubtime, float):
            instance.pubtime = xlrd.xldate.xldate_as_datetime(
                instance.pubtime, 0)



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
    
        

class RiskNewsResources(resources.ModelResource):
    title = fields.Field(
        attribute='title',
        column_name=u'标题'
    )
    url = fields.Field(
        attribute='url',
        column_name=u'网站链接'
    )
    content = fields.Field(
        attribute='content',
        column_name=u'正文'
    )
    pubtime = fields.Field(
        attribute='pubtime',
        column_name=u'发布时间'
    )
    reprinted = fields.Field(
        attribute='reprinted',
        column_name=u'转载数',
        widget=IntegerWidget()
    )
    status = fields.Field(
        attribute='status',
        column_name=u'是否删除',
    )
    risk_keyword = fields.Field(
        attribute='risk_keyword',
        column_name=u'风险新闻关键词',
    )
    invalid_keyword = fields.Field(
        attribute='invalid_keyword',
        column_name=u'无效关键词',
    )
    publisher = fields.Field(
        attribute='publisher',
        column_name=u'文章发布者',
        widget=ForeignKeyWidget(RiskNewsPublisher, 'name')
    )
    area = fields.Field(
        attribute='area',
        column_name=u'地域',
        widget=ManyToManyWidget(Area, ' ', 'name')
    )
    industry = fields.Field(
        attribute='industry',
        column_name=u'行业',
        widget=ManyToManyWidget(Industry, ' ', 'name')
    )
    enterprise = fields.Field(
        attribute='enterprise',
        column_name=u'企业',
        widget=ManyToManyWidget(Enterprise, ' ', 'name')
    )

    class Meta:
        model = RiskNews
        fields = ('id', 'title', 'url', 'content', 'pubtime', 'reprinted',
                  'publisher', 'area', 'industry', 'enterprise', 'status', 'risk_keyword', 'invalid_keyword',)
        export_order = ('id', 'title', 'url', 'content', 'pubtime', 'reprinted',
                        'publisher', 'area', 'industry', 'enterprise', 'status', 'risk_keyword', 'invalid_keyword',)

    def before_save_instance(self, instance, dry_run, temp=''):
        if not instance.pubtime:
            instance.pubtime = datetime.now()
        elif isinstance(instance.pubtime, basestring):
            instance.pubtime = datetime.strptime(
                instance.pubtime, '%Y-%m-%d %H:%M:%S')
        elif isinstance(instance.pubtime, float):
            instance.pubtime = xlrd.xldate.xldate_as_datetime(
                instance.pubtime, 0)

