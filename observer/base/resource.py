from django.core.exceptions import ObjectDoesNotExist
from import_export.widgets import (DateWidget, ForeignKeyWidget,
                                   ManyToManyWidget, IntegerWidget, )
from import_export import widgets
from import_export import resources, fields

from observer.base.models import Industry
from observer.utils.str_format import str_to_md5str


class IndustryResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='行业编号')
    name = fields.Field(attribute='name', column_name='行业名称')
    level = fields.Field(attribute='level', column_name='行业等级')
    desc = fields.Field(attribute='desc', column_name='行业说明')
    pre = fields.Field(attribute='pre', column_name='上一级编号')

    class Meta:
        model = Industry
        fields = ('id', 'name', 'level', 'desc',)
        export_order = ('id', 'name', 'level', 'desc',)

    def before_save_instance(self, instance, dry_run, temp=''):
        if not instance.desc:
            instance.desc = ''

        pre = instance.pre
        if pre:
            try:
                industry = Industry.objects.get(id=pre)
                instance.parent = industry
            except ObjectDoesNotExist:
                pass
