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
        fields = ('guid', 'title', 'url', 'pubtime', 'source', 'score', 'industry_id', 'corpus_id', )
        export_order = ('guid', 'title', 'url', 'pubtime', 'source', 'score', 'industry_id', 'corpus_id', )

    def dehydrate_industry_id(self, obj):
        try:
            industry = ConsumerIndustry.objects.get(id=obj.industry_id)
            return industry
        except ObjectDoesNotExist:
            pass


    def before_save_instance(self, instance, using_transactions, dry_run):
        a_guid = str_to_md5str(instance.url)
        instance.guid = a_guid

        if Article.objects.filter(guid=a_guid).exists():
            return

        areas = instance.area.split(' ')
        a_ids = Area.objects.filter(name__in=areas).values_list('id', flat=True)
        categorys = instance.category.split(' ')
        c_ids = Category.objects.filter(name__in=categorys).values_list('id', flat=True)

        for a_id in a_ids:
            if not ArticleArea.objects.filter(article_id=a_guid, area_id=a_id).exists():
                ArticleArea(
                    article_id=a_guid,
                    area_id=a_id,
                ).save()

        for c_id in c_ids:
            if not ArticleCategory.objects.filter(article_id=a_guid, category_id=c_id).exists():
                ArticleCategory(
                    article_id=a_guid,
                    category_id=c_id,
                ).save()


class InspectionResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID')
    guid = fields.Field(attribute='guid', column_name='GUID')
    title = fields.Field(attribute='title', column_name='标题')
    url = fields.Field(attribute='url', column_name='URL')
    pubtime = fields.Field(attribute='pubtime', column_name='发布时间')
    source = fields.Field(attribute='source', column_name='抽检单位')
    unitem = fields.Field(attribute='unitem', column_name='不合格项')
    qualitied = fields.Field(attribute='qualitied', column_name='合格率')
    category = fields.Field(attribute='category', column_name='抽查类别')
    level = fields.Field(attribute='level', column_name='抽查级别')
    industry_id = fields.Field(attribute='industry_id', column_name='行业ID')
    area_id = fields.Field(attribute='area_id', column_name='地域ID')
    origin_product = fields.Field(attribute='origin_product', column_name='导入产品名')

    class Meta:
        model = Inspection
        import_id_fields = ('guid',)
        fields = ('id', 'guid', 'title', 'url', 'pubtime', 'source', 'unitem', 'qualitied', 'category', 'level', 'industry_id', 'area_id', 'origin_product' )
        export_order = ('id', 'guid', 'title', 'url', 'pubtime', 'source', 'unitem', 'qualitied', 'category', 'level', 'industry_id', 'area_id', 'origin_product' )

    def before_save_instance(self, instance, using_transactions, dry_run):
        i_guid = str_to_md5str(instance.url)
        instance.guid = i_guid

        if Article.objects.filter(guid=i_guid).exists():
            return


class IndustryProductsResources(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id')
    name = fields.Field(attribute='name', column_name='name')
    industry_id = fields.Field(attribute='industry_id', column_name='industry_id')

    class Meta:
        model = IndustryProducts
        fields = ('id', 'name', 'industry_id')
        export_order = fields
