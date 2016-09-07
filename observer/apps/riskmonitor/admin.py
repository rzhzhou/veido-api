# -*- coding: utf-8 -*-
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from observer.apps.riskmonitor.resource import (
    ConsumeIndexResources, ManageIndexResources, SocietyIndexResources, RiskNewsResources)
from observer.apps.riskmonitor.models import (Brand, Enterprise, Industry,
                                              Metrics, Product, ProductMetrics,
                                              RiskData, RiskNewsPublisher, RiskNews,
                                              ScoreEnterprise, ScoreIndustry,
                                              ScoreProduct, UserArea,
                                              UserEnterprise, UserIndustry,
                                              SocietyIndex, ConsumeIndex,
                                              ManageIndex, Cache, CacheConf)


# class ProductAdmin(admin.ModelAdmin):
#     fields = ('name', 'enterprise', 'industry')
#     list_display = ('name', 'enterprise', 'industry')
#     search_fields = ('name', 'enterprise', 'industry')
#     list_filter = ('name', 'enterprise', 'industry')


# class MetricsAdmin(admin.ModelAdmin):
#     fields = ('name', 'level', 'parent')
#     list_display = ('name', 'level', 'parent')
#     search_fields = ('name', 'level', 'parent')
#     list_filter = ('name', 'level', 'parent')


# class ProductMetricsAdmin(admin.ModelAdmin):
#     fields = ('weight', 'metrics', 'product')
#     list_display = ('weight', 'metrics', 'product')
#     search_fields = ('weight', 'metrics', 'product')
#     list_filter = ('weight', 'metrics', 'product')

class UserIndustryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'industry': ('name',)}
    fields = ('name', 'user', 'industry')
    list_display = ('name', 'user', 'industry')
    search_fields = ('name', 'user__username', 'industry__name')
    list_filter = ('user', 'industry__level')


# class UserEnterpriseAdmin(admin.ModelAdmin):
#     fields = ('user', 'enterprise')
#     list_display = ('user', 'enterprise')
#     search_fields = ('user', 'enterprise')
#     list_filter = ('user', 'enterprise')


class ScoreIndustryAdmin(admin.ModelAdmin):

    def show_putime(self, obj):
        return obj.pubtime.strftime("%Y-%m-%d %H:%M")

    show_putime.short_description = u'发布时间'

    fields = ('score', 'pubtime', 'industry', 'user')
    list_display = ('score', 'industry', 'user', 'show_putime')
    search_fields = ('score', 'industry__name', 'user__username',)
    list_filter = ('pubtime', 'user', )


class ScoreEnterpriseAdmin(admin.ModelAdmin):

    def show_putime(self, obj):
        return obj.pubtime.strftime("%Y-%m-%d %H:%M")

    show_putime.short_description = u'发布时间'
    fields = ('score', 'enterprise', 'pubtime',)
    list_display = ('score', 'enterprise', 'user', 'show_putime')
    search_fields = ('score', 'enterprise__name', 'user__username')
    list_filter = ('pubtime', 'user')


# class ScoreProductAdmin(admin.ModelAdmin):
#     fields = ('score', 'pubtime', 'product')
#     list_display = ('score', 'pubtime', 'product')
#     search_fields = ('score', 'pubtime', 'product')
#     list_filter = ('score', 'pubtime', 'product')


# class BrandAdmin(admin.ModelAdmin):
#     fields = ('zh_name', 'en_name', 'logo')
#     list_display = ('zh_name', 'en_name', 'logo')
#     search_fields = ('zh_name', 'en_name', 'logo')
#     list_filter = ('zh_name', 'en_name', 'logo')


class RiskDataAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    list_display = ('user_name', 'content', 'comment',
                    'url', 'area', 'brand', 'industry')
    search_fields = ('user_name', 'content', 'comment',
                     'url', 'area', 'brand', 'industry')
    list_filter = ('user_name', 'content', 'comment',
                   'url', 'area', 'brand', 'industry')


class RiskNewsAdmin(ImportExportActionModelAdmin):
    resource_class = RiskNewsResources

    # related_search_fields = {'area': ('name',)}
    list_display = ('title', 'url', 'publisher', 'reprinted', 'pubtime')
    search_fields = ('title', 'content', 'url', 'reprinted', 'publisher__name',
                     'industry__name', 'enterprise__name', 'area__name')
    list_filter = ('pubtime', 'industry__name')
    actions = ['delete_selected']

    def reduce_score(self, obj):
        industrys = obj.industry.all()
        enterprises = obj.enterprise.all()
        for industry in industrys:
            items = ScoreIndustry.objects.filter(industry=industry)
            for item in items:
                if item.score < 100:
                    score = int(item.score) + 1
                    ScoreIndustry.objects.filter(
                        id=item.id).update(score=score)
                else:
                    continue

        for enterprise in enterprises:
            items = ScoreEnterprise.objects.filter(enterprise=enterprise)
            for item in items:
                if item.score < 100:
                    score = int(item.score) + 1
                    ScoreEnterprise.objects.filter(
                        id=item.id).update(score=score)
                else:
                    continue
        return

    def delete_model(self, request, obj):
        self.reduce_score(obj)
        obj.delete()

    def delete_selected(self, request, objs):
        for obj in objs:
            self.reduce_score(obj)
            obj.delete()


class UserAreaAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    list_display = ('user', 'area')
    search_fields = ('user__username', 'area__name')
    # list_filter = ('user', 'area')


class ConsumeIndexAdmin(ImportExportModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = ConsumeIndexResources

    related_search_fields = {'industry': ('name',)}

    fields = ('force', 'close', 'consume', 'year', 'industry')
    list_display = ('force', 'close', 'consume', 'year', 'industry')
    search_fields = ('force', 'industry__name', 'year')
    list_filter = ('year', 'force', 'close', 'consume')


class SocietyIndexAdmin(ImportExportModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = SocietyIndexResources

    related_search_fields = {'industry': ('name',)}

    fields = ('trade', 'qualified', 'accident', 'year', 'industry')
    list_display = ('trade', 'qualified', 'accident', 'year', 'industry', )
    search_fields = ('trade', 'industry__name', 'year')
    list_filter = ('year', 'trade', 'qualified', 'accident')


class ManageIndexAdmin(ImportExportModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = ManageIndexResources

    related_search_fields = {'industry': ('name',)}

    fields = ('licence', 'productauth', 'encourage', 'limit', 'remove',
              'year', 'industry')
    list_display = ('licence', 'productauth', 'encourage', 'limit',
                    'remove', 'year', 'industry', )
    search_fields = ('licence', 'productauth', 'encourage', 'limit', 'remove',
                     'industry__name', 'year')
    list_filter = ('year', 'productauth',)


class CacheAdmin(admin.ModelAdmin):
    fields = ('k', 'v', 'update_at')
    list_display = ('k', 'update_at')
    list_filter = ('k',)
    search_fields = ('k',)
    readonly_fields = ('update_at',)


class CacheConfAdmin(admin.ModelAdmin):
    fields = ('name', 'days', 'params')
    list_display = ('name', 'days', 'params')
    list_filter = ('name', 'days')
    search_fields = ('name',)


# admin.site.register(Product, ProductAdmin)
# admin.site.register(Metrics, MetricsAdmin)
# admin.site.register(ProductMetrics, ProductMetricsAdmin)
admin.site.register(UserIndustry, UserIndustryAdmin)
# admin.site.register(UserEnterprise, UserEnterpriseAdmin)
admin.site.register(ScoreIndustry, ScoreIndustryAdmin)
admin.site.register(ScoreEnterprise, ScoreEnterpriseAdmin)
# admin.site.register(ScoreProduct, ScoreProductAdmin)
# admin.site.register(Brand, BrandAdmin)
# admin.site.register(RiskData, RiskDataAdmin)
admin.site.register(RiskNewsPublisher)
admin.site.register(RiskNews, RiskNewsAdmin)
admin.site.register(UserArea, UserAreaAdmin)
admin.site.register(SocietyIndex, SocietyIndexAdmin)
admin.site.register(ConsumeIndex, ConsumeIndexAdmin)
admin.site.register(ManageIndex, ManageIndexAdmin)
admin.site.register(Cache, CacheAdmin)
admin.site.register(CacheConf, CacheConfAdmin)
