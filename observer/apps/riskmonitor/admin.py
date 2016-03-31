from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from observer.apps.riskmonitor.models import (Brand, Enterprise, Industry,
                                              Metrics, Product, ProductMetrics,
                                              RiskData, RiskNews,
                                              ScoreEnterprise, ScoreIndustry,
                                              ScoreProduct, UserEnterprise,
                                              UserIndustry, UserArea)


class IndustryAdmin(admin.ModelAdmin):
    fields = ('name', 'level', 'parent')
    list_display = ('name', 'level', 'parent')
    search_fields = ('name', 'level', 'parent')
    list_filter = ('name', 'level', 'parent')


class EnterpriseAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    fields = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area')
    list_display = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area')
    search_fields = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area')
    list_filter = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area')


class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'enterprise', 'industry')
    list_display = ('name', 'enterprise', 'industry')
    search_fields = ('name', 'enterprise', 'industry')
    list_filter = ('name', 'enterprise', 'industry')


class MetricsAdmin(admin.ModelAdmin):
    fields = ('name', 'level', 'parent')
    list_display = ('name', 'level', 'parent')
    search_fields = ('name', 'level', 'parent')
    list_filter = ('name', 'level', 'parent')


class ProductMetricsAdmin(admin.ModelAdmin):
    fields = ('weight', 'metrics', 'product')
    list_display = ('weight', 'metrics', 'product')
    search_fields = ('weight', 'metrics', 'product')
    list_filter = ('weight', 'metrics', 'product')


class UserIndustryAdmin(admin.ModelAdmin):
    fields = ('name', 'user', 'industry')
    list_display = ('name', 'user', 'industry')
    search_fields = ('name', 'user', 'industry')
    list_filter = ('name', 'user', 'industry')


class UserEnterpriseAdmin(admin.ModelAdmin):
    fields = ('user', 'enterprise')
    list_display = ('user', 'enterprise')
    search_fields = ('user', 'enterprise')
    list_filter = ('user', 'enterprise')


class ScoreIndustryAdmin(admin.ModelAdmin):
    fields = ('score', 'pubtime', 'industry')
    list_display = ('score', 'pubtime', 'industry')
    search_fields = ('score', 'pubtime', 'industry')
    list_filter = ('score', 'pubtime', 'industry')


class ScoreEnterpriseAdmin(admin.ModelAdmin):
    fields = ('score', 'pubtime', 'enterprise')
    list_display = ('score', 'pubtime', 'enterprise')
    search_fields = ('score', 'pubtime', 'enterprise')
    list_filter = ('score', 'pubtime', 'enterprise')


class ScoreProductAdmin(admin.ModelAdmin):
    fields = ('score', 'pubtime', 'product')
    list_display = ('score', 'pubtime', 'product')
    search_fields = ('score', 'pubtime', 'product')
    list_filter = ('score', 'pubtime', 'product')


class BrandAdmin(admin.ModelAdmin):
    fields = ('zh_name', 'en_name', 'logo')
    list_display = ('zh_name', 'en_name', 'logo')
    search_fields = ('zh_name', 'en_name', 'logo')
    list_filter = ('zh_name', 'en_name', 'logo')


class RiskDataAdmin(ForeignKeyAutocompleteAdmin):
    related_search_fields = {'area': ('name',)}
    list_display = ('user_name', 'content', 'comment', 'url', 'area', 'brand', 'industry')
    search_fields = ('user_name', 'content', 'comment', 'url', 'area', 'brand', 'industry')
    list_filter = ('user_name', 'content', 'comment', 'url', 'area', 'brand', 'industry')


class RiskNewsAdmin(admin.ModelAdmin):
    # related_search_fields = {'area': ('name',)}
    list_display = ('title', 'url', 'publisher', 'reprinted')
    search_fields = ('title', 'url', 'publisher', 'reprinted', 'industry', 'enterprise')
    list_filter = ('industry', 'enterprise', 'area')


class UserAreaAdmin(admin.ModelAdmin):
    list_display = ('user', 'area')
    search_fields = ('user', 'area')
    list_filter = ('user', 'area')


admin.site.register(Industry, IndustryAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Metrics, MetricsAdmin)
admin.site.register(ProductMetrics, ProductMetricsAdmin)
admin.site.register(UserIndustry, UserIndustryAdmin)
admin.site.register(UserEnterprise, UserEnterpriseAdmin)
admin.site.register(ScoreIndustry, ScoreIndustryAdmin)
admin.site.register(ScoreEnterprise, ScoreEnterpriseAdmin)
admin.site.register(ScoreProduct, ScoreProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(RiskData, RiskDataAdmin)
admin.site.register(RiskNews, RiskNewsAdmin)
admin.site.register(UserArea, UserAreaAdmin)
