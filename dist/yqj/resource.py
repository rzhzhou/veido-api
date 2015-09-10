# -*- coding: utf-8 -*-
from import_export.widgets import DateWidget
from import_export import resources, fields


class InspectionResources(resources.ModelResource):
    pubtime = fields.Field(attribute='pubtime', column_name=u'发布日期', widget=DateWidget(format='%Y-%m-%d'))
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