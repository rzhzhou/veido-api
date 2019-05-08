from django.core.exceptions import ObjectDoesNotExist
from import_export.widgets import (DateWidget, ForeignKeyWidget,
                                   ManyToManyWidget, IntegerWidget, )
from import_export import widgets
from import_export import resources, fields

from observer.base.models import *
from observer.utils.str_format import str_to_md5str
from observer.utils.date_format import date_format


class IndustryResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='行业编号')
    level = fields.Field(attribute='level', column_name='行业等级')
    pre = fields.Field(attribute='pre', column_name='上一级编号')

    class Meta:
        model = MajorIndustries
        fields = ('id', 'level',)
        export_order = ('id', 'level',)

    def before_save_instance(self, instance, dry_run, temp=''):
        pre = instance.pre

        if pre:
            try:
                industry = MajorIndustries.objects.get(id=pre)
                instance.parent = industry
            except ObjectDoesNotExist:
                pass


class HistoryIndustriesResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id')
    name = fields.Field(attribute='name', column_name='产品名称')
    year = fields.Field(attribute='year', column_name='年份')
    status = fields.Field(attribute='status', column_name='状态')
    industry_id = fields.Field(attribute='industry_id', column_name='产品编码')

    class Meta:
        model = HistoryIndustries
        fields = ('id', 'name', 'year', 'status',)
        export_order = ('id', 'name', 'year', 'status',)

    def before_save_instance(self, instance, dry_run, temp=''):
        industry_id = instance.industry_id

        if industry_id:
            try:
                temp = MajorIndustries.objects.get(id=industry_id)
                instance.industry = temp
            except ObjectDoesNotExist:
                pass


class AreaResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    name = fields.Field(attribute='name', column_name='地域名称')
    level = fields.Field(attribute='level', column_name='地域等级')
    pre = fields.Field(attribute='pre', column_name='上一级ID')

    class Meta:
        model = Area
        fields = ('id', 'name', 'level',)
        export_order = ('id', 'name', 'level',)

    def before_save_instance(self, instance, dry_run, temp=''):
        pre = instance.pre
        if pre:
            try:
                area = Area.objects.get(id=pre)
                instance.parent = area
            except ObjectDoesNotExist:
                pass


class CategoryResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    name = fields.Field(attribute='name', column_name='类别名称')
    level = fields.Field(attribute='level', column_name='类别等级')
    pre = fields.Field(attribute='pre', column_name='上一级ID')

    class Meta:
        model = Category
        fields = ('id', 'name', 'level',)
        export_order = ('id', 'name', 'level',)

    def before_save_instance(self, instance, dry_run, temp=''):
        pre = instance.pre
        if pre:
            try:
                category = Category.objects.get(id=pre)
                instance.parent = category
            except ObjectDoesNotExist:
                pass


class ArticleResources(resources.ModelResource):
    guid = fields.Field(attribute='guid', column_name='GUID')
    title = fields.Field(attribute='title', column_name='标题')
    url = fields.Field(attribute='url', column_name='URL')
    pubtime = fields.Field(attribute='pubtime', column_name='发布时间')
    source = fields.Field(attribute='source', column_name='发布媒体')
    score = fields.Field(attribute='score', column_name='风险程度')
    area = fields.Field(attribute='area', column_name='地域')
    category = fields.Field(attribute='category', column_name='类别')
    industry_id = fields.Field(attribute='industry_id', column_name='产品类别')
    corpus_id = fields.Field(attribute='corpus_id', column_name='语料词编号')

    class Meta:
        model = Article
        import_id_fields = ('guid',)
        fields = ('guid', 'title', 'url', 'pubtime', 'source',
                  'score', 'industry_id', 'corpus_id', )
        export_order = ('guid', 'title', 'url', 'pubtime',
                        'source', 'score', 'industry_id', 'corpus_id', )

    def dehydrate_industry_id(self, obj):
        try:
            industry = ConsumerIndustry.objects.get(id=obj.industry_id)
            return industry
        except ObjectDoesNotExist:
            pass

    def before_save_instance(self, instance, using_transactions, dry_run):

        article2 = Article2.objects.filter(url=instance.url)
        if article2.exists():
            return

        areas = instance.area.split(',')
        a_ids = Area.objects.filter(
            name__in=areas).values_list('id', flat=True)
        if len(areas) != len(a_ids):
            return {
                'status': 0,
                'message': '操作失败！Excel %s 行"地域"有误！' % (i + 1, )
            }

        area = Area.objects.filter(id__in=a_ids)

        categories = instance.category.split(',')
        c_ids = Category.objects.filter(
            name__in=categories).values_list('id', flat=True)

        if len(categories) != len(c_ids):
            return {
                'status': 0,
                'message': '操作失败！Excel %s 行"类别"有误！' % (i + 1, )
            }

        category = Category.objects.filter(id__in=c_ids)

        article2.areas.add(*area)
        article2.categories.add(*category)


class InspectionResources(resources.ModelResource):
    # id = fields.Field(attribute='id', column_name='ID')
    # title = fields.Field(attribute='title', column_name='标题')
    # url = fields.Field(attribute='url', column_name='URL')
    # pubtime = fields.Field(attribute='pubtime', column_name='发布时间')
    # source = fields.Field(attribute='source', column_name='抽检单位')
    # origin_product = fields.Field(attribute='origin_product', column_name='导入产品名')
    # product_name = fields.Field(attribute='product_name', column_name='产品名称')
    # qualitied = fields.Field(attribute='qualitied', column_name='合格率')
    # unqualitied_patch = fields.Field(attribute='unqualitied_patch', column_name="不合格批次")
    # qualitied_patch = fields.Field(attribute='qualitied_patch', column_name="合格批次")
    # inspect_patch = fields.Field(attribute='inspect_patch', column_name="抽查批次")
    # category = fields.Field(attribute='category', column_name='抽查类别')

    class Meta:
        model = Inspection
        # import_id_fields = ('guid',)
        # fields = ('id', 'guid', 'title', 'url', 'pubtime', 'source', 'unitem', 'qualitied', 'category', 'level', 'industry_id', 'area_id', 'origin_product' )
        # export_order = ('id', 'guid', 'title', 'url', 'pubtime', 'source', 'unitem', 'qualitied', 'category', 'level', 'industry_id', 'area_id', 'origin_product' )


class IndustryProductsResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id')
    name = fields.Field(attribute='name', column_name='name')
    industry_id = fields.Field(
        attribute='industry_id', column_name='industry_id')

    class Meta:
        model = IndustryProducts
        fields = ('id', 'name', 'industry_id')
        export_order = fields
