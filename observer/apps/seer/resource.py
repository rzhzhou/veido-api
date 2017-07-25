# -*- coding: utf-8 -*-
import pytz
import xlrd
from datetime import datetime

from django.conf import settings

from import_export.widgets import (DateTimeWidget, ForeignKeyWidget,
                                   IntegerWidget, ManyToManyWidget)
from import_export import widgets
from import_export import resources, fields
from observer.apps.origin.models import Area, Enterprise, Industry
from observer.apps.seer.models import (Area, ConsumeIndex, ManageIndex, SocietyIndex,
                                              RiskNews, RiskNewsPublisher)


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


class ConsumeIndexResources(resources.ModelResource):
    force = fields.Field(attribute='force', column_name=u'国家强制性要求')
    close = fields.Field(attribute='close', column_name=u'密切程度')
    consume = fields.Field(attribute='consume', column_name=u'涉及特定消费群体和特殊要求')
    year = fields.Field(attribute='year', column_name=u'年度')

    industry = fields.Field(
        attribute='industry',
        column_name=u'行业',
        widget=ForeignKeyWidget(Industry, 'name')
    )

    area = fields.Field(
        attribute='area',
        column_name=u'地域',
        widget=ForeignKeyWidget(Area, 'name')
    )

    class Meta:
        model = ConsumeIndex
        fields = ('id', 'force', 'close', 'consume',
                  'year', 'industry', 'area')
        export_order = ('id', 'force', 'close', 'consume',
                        'year', 'industry', 'area')


class SocietyIndexResources(resources.ModelResource):
    trade = fields.Field(attribute='trade', column_name=u'贸易量')
    qualified = fields.Field(attribute='qualified', column_name=u'抽检合格率')
    accident = fields.Field(attribute='accident', column_name=u'案例发生状况')
    year = fields.Field(attribute='year', column_name=u'年度')

    industry = fields.Field(
        attribute='industry',
        column_name=u'行业',
        widget=ForeignKeyWidget(Industry, 'name')
    )
    area = fields.Field(
        attribute='area',
        column_name=u'地域',
        widget=ForeignKeyWidget(Area, 'name')
    )

    class Meta:
        model = SocietyIndex
        fields = ('id', 'trade', 'qualified',
                  'accident', 'year', 'industry', 'area')
        export_order = ('id', 'trade', 'qualified',
                        'accident', 'year', 'industry', 'area')


class ManageIndexResources(resources.ModelResource):
    licence = fields.Field(attribute='licence', column_name=u'列入许可证目录')
    productauth = fields.Field(
        attribute='productauth', column_name=u'列入产品认证目录')
    encourage = fields.Field(attribute='encourage', column_name=u'是否鼓励')
    limit = fields.Field(attribute='limit', column_name=u'是否限制')
    remove = fields.Field(attribute='remove', column_name=u'是否淘汰')
    year = fields.Field(attribute='year', column_name=u'年度')

    industry = fields.Field(
        attribute='industry',
        column_name=u'行业',
        widget=ForeignKeyWidget(Industry, 'name')
    )
    area = fields.Field(
        attribute='area',
        column_name=u'地域',
        widget=ForeignKeyWidget(Area, 'name')
    )

    class Meta:
        model = ManageIndex
        fields = ('id', 'licence', 'productauth', 'encourage',
                  'limit', 'remove', 'year', 'industry', 'area')
        export_order = ('id', 'licence', 'productauth',
                        'encourage', 'limit', 'remove', 'year', 'industry', 'area')
