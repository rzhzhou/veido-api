# -*- coding: utf-8 -*-
from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from observer.apps.riskmonitor.models import (Brand, Enterprise, Industry,
                                              Metrics, Product, ProductMetrics,
                                              RiskData, RiskNews,
                                              ScoreEnterprise, ScoreIndustry,
                                              ScoreProduct, UserArea,
                                              UserEnterprise, UserIndustry,)
from import_export.admin import ImportExportActionModelAdmin
from import_export.admin import ImportExportModelAdmin


class IndustryAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'parent': ('name',)}
    fields = ('name', 'level', 'parent')
    list_display = ('name', 'level', 'parent')
    search_fields = ('name', 'level', 'parent__name')
    list_filter = ('level', )


class EnterpriseAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    fields = ('name', 'area')
    list_display = ('name', 'area')
    search_fields = ('name', 'area__name')
    list_filter = ('area', )


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
    list_filter = ('pubtime', 'user' )


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
    list_display = ('user_name', 'content', 'comment', 'url', 'area', 'brand', 'industry')
    search_fields = ('user_name', 'content', 'comment', 'url', 'area', 'brand', 'industry')
    list_filter = ('user_name', 'content', 'comment', 'url', 'area', 'brand', 'industry')


class RiskNewsAdmin(admin.ModelAdmin):
    # related_search_fields = {'area': ('name',)}
    list_display = ('title', 'url', 'publisher', 'reprinted', 'pubtime')
    search_fields = ('title', 'url', 'reprinted', 'publisher__name',
        'industry__name', 'enterprise__name', 'area__name')
    list_filter = ('pubtime', )
    actions = ['delete_selected']

    def reduce_score(self, obj):
        industrys = obj.industry.all()
        enterprises = obj.enterprise.all()
        for industry in industrys:
            items = ScoreIndustry.objects.filter(industry=industry)
            for item in items:
                if item.score < 100:
                    score = int(item.score) + 1
                    ScoreIndustry.objects.filter(id=item.id).update(score=score)
                else:
                    continue

        for enterprise in enterprises:
            items = ScoreEnterprise.objects.filter(enterprise=enterprise)
            for item in items:
                if item.score < 100:
                    score = int(item.score) + 1
                    ScoreEnterprise.objects.filter(id=item.id).update(score=score)
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


admin.site.register(Industry, IndustryAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
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
admin.site.register(RiskNews, RiskNewsAdmin)
admin.site.register(UserArea, UserAreaAdmin)
