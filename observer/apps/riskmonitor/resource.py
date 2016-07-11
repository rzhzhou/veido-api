# -*- coding: utf-8 -*-
import pytz
import xlrd
from datetime import datetime

from django.conf import settings

from import_export.widgets import DateWidget, ForeignKeyWidget, ManyToManyWidget
from import_export import widgets
from import_export import resources, fields
from observer.apps.riskmonitor.models import ConsumeIndex, ManageIndex, SocietyIndex, Industry


class ConsumeIndexResources(resources.ModelResource):
    force = fields.Field(attribute='force', column_name=u'国家强制性要求')
    close = fields.Field(attribute='close', column_name=u'密切程度')
    consume = fields.Field(attribute='consume', column_name=u'涉及特定消费群体和特殊要求')
    year = fields.Field(attribute='year', column_name=u'年度')

    industry = fields.Field(
        column_name=u'行业',
        attribute='industry',
        widget=ForeignKeyWidget(Industry, 'name')
    )

    class Meta:
        model = ConsumeIndex
        fields = ('id', 'force', 'close', 'consume', 'year', 'industry')
        export_order = ('id', 'force', 'close', 'consume', 'year', 'industry')


class SocietyIndexResources(resources.ModelResource):
    trade = fields.Field(attribute='trade', column_name=u'贸易量')
    qualified = fields.Field(attribute='qualified', column_name=u'抽检合格率')
    accident = fields.Field(attribute='accident', column_name=u'案例发生状况')
    year = fields.Field(attribute='year', column_name=u'年度')

    industry = fields.Field(
        column_name=u'行业',
        attribute='industry',
        widget=ForeignKeyWidget(Industry, 'name')
    )

    class Meta:
        model = SocietyIndex
        fields = ('id', 'trade', 'qualified', 'accident', 'year', 'industry')
        export_order = ('id', 'trade', 'qualified',
                        'accident', 'year', 'industry')


class ManageIndexResources(resources.ModelResource):
    licence = fields.Field(attribute='licence', column_name=u'列入许可证目录')
    productauth = fields.Field(
        attribute='productauth', column_name=u'列入产品认证目录')
    encourage = fields.Field(attribute='encourage', column_name=u'是否鼓励')
    limit = fields.Field(attribute='limit', column_name=u'是否限制')
    remove = fields.Field(attribute='remove', column_name=u'是否淘汰')
    year = fields.Field(attribute='year', column_name=u'年度')

    industry = fields.Field(
        column_name=u'行业',
        attribute='industry',
        widget=ForeignKeyWidget(Industry, 'name')
    )

    class Meta:
        model = ManageIndex
        fields = ('id', 'licence', 'productauth', 'encourage',
                  'limit', 'remove', 'year', 'industry')
        export_order = ('id', 'licence', 'productauth',
                        'encourage', 'limit', 'remove', 'year', 'industry')
