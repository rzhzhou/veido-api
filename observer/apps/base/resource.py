import pytz
import xlrd
from datetime import datetime
from django.conf import settings
from import_export.widgets import DateWidget, ForeignKeyWidget, ManyToManyWidget, IntegerWidget
from import_export import widgets
from import_export import resources, fields
from observer.apps.base.models import Area, Industry, Enterprise, Inspection, AdministrativePenalties #InspectionPublisher, 


class EnterpriseResources(resources.ModelResource):
    name = fields.Field(attribute='name', column_name='企业名')

    area = fields.Field(
        column_name='地域',
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




class InspectionResources(resources.ModelResource):
    pubtime = fields.Field(attribute='pubtime', column_name='发布日期')
    title = fields.Field(attribute='title', column_name='标题')
    url = fields.Field(attribute='url', column_name='链接')
    qualitied = fields.Field(attribute='qualitied', column_name='合格率')
    content = fields.Field(attribute='content', column_name='正文')
    unitem = fields.Field(attribute='unitem', column_name='不合格项')
    brand = fields.Field(attribute='brand', column_name='商标')
    product = fields.Field(attribute='product', column_name='产品种类')
    publisher = fields.Field(attribute='publisher', column_name='抽检单位')
    area = fields.Field(
        column_name='地域',
        attribute='area',
        widget=ManyToManyWidget(Area, ' ', 'name'))
    industry = fields.Field(
        column_name='行业',
        attribute='industry',
        widget=ManyToManyWidget(Industry, ' ', 'name'))
    enterprise_qualified = fields.Field(
        column_name='合格企业',
        attribute='enterprise_qualified',
        widget=ManyToManyWidget(Enterprise, ' ', 'name'))
    enterprise_unqualified = fields.Field(
        column_name='不合格企业',
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
    pubtime = fields.Field(attribute='pubtime', column_name='发布日期')
    title = fields.Field(attribute='title', column_name='标题')
    url = fields.Field(attribute='url', column_name='链接')
    content = fields.Field(attribute='content', column_name='正文')
    publisher = fields.Field(attribute='publisher', column_name='发布者')
    case_name = fields.Field(attribute='case_name', column_name='案件名称')
    illegal_behavior = fields.Field(attribute='illegal_behavior', column_name='违法行为')
    punishment_basis = fields.Field(attribute='punishment_basis', column_name='处罚依据')
    punishment_result = fields.Field(attribute='punishment_result', column_name='处罚结果')
    penalty_organ = fields.Field(attribute='penalty_organ', column_name='处罚机关')
    credit_code = fields.Field(attribute='credit_code', column_name='统一社会信用代码')
    area = fields.Field(attribute='area', column_name='地域')
    industry = fields.Field(attribute='industry', column_name='行业')
    enterprise=fields.Field(attribute='enterprise', column_name='处罚企业')

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
    
        



