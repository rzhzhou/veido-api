from django.contrib import admin

from observer.apps.riskmonitor.models import(
    Score, Industry, Enterprise, Product, EnterpriseProduct,
    Metrics, MetricsProduct)

# Register your models here.
class ScoreAdmin(admin.ModelAdmin):
    fields = ('score', 'pubtime')
    list_display = ('score', 'pubtime')
    search_fields = ('score', 'pubtime')
    list_filter = ('score', 'pubtime')


class IndustryAdmin(admin.ModelAdmin):
    fields = ('name', 'level', 'parent', 'score')
    list_display = ('name', 'level', 'parent', 'score')
    search_fields = ('name', 'level', 'parent', 'score')
    list_filter = ('name', 'level', 'parent', 'score')


class EnterpriseAdmin(admin.ModelAdmin):
    fields = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area', 'score')
    list_display = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area', 'score')
    search_fields = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area', 'score')
    list_filter = ('name', 'locate_x', 'locate_y', 'scale', 'ccc', 'area', 'score')


class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'score')
    list_display = ('name', 'score')
    search_fields = ('name', 'score')
    list_filter = ('name', 'score')


class EnterpriseProductAdmin(admin.ModelAdmin):
    fields = ('alias', 'enterprise', 'product', 'score')
    list_display = ('alias', 'enterprise', 'product', 'score')
    search_fields = ('alias', 'enterprise', 'product', 'score')
    list_filter = ('alias', 'enterprise', 'product', 'score')


class MetricsAdmin(admin.ModelAdmin):
    fields = ('name', 'level', 'parent')
    list_display = ('name', 'level', 'parent')
    search_fields = ('name', 'level', 'parent')
    list_filter = ('name', 'level', 'parent')


class MetricsProductAdmin(admin.ModelAdmin):
    fields = ('weight', 'metrics', 'product')
    list_display = ('weight', 'metrics', 'product')
    search_fields = ('weight', 'metrics', 'product')
    list_filter = ('weight', 'metrics', 'product')


admin.site.register(Score, ScoreAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(EnterpriseProduct, EnterpriseProductAdmin)
admin.site.register(Metrics, MetricsAdmin)
admin.site.register(MetricsProduct, MetricsProductAdmin)
