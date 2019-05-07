from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import *
from observer.base.resource import *
from observer.utils.str_format import str_to_md5str


class CPCIndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )


class CCCIndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    # resource_class = IndustryResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )


class LicenceIndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    # resource_class = IndustryResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )


class ConsumerIndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    # resource_class = IndustryResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )


class MajorIndustriesAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = IndustryResources

    autocomplete_fields = ('parent',)
    search_fields = ('id',)
    list_display = ('id', 'level', 'parent')
    list_filter = ('level',)


class HistoryIndustriesAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = HistoryIndustriesResources

    autocomplete_fields = ('industry',)
    search_fields = ('name', )
    list_display = ('industry', 'name', 'year', 'status',)
    list_filter = ('year', 'status')


class MajorIndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    # resource_class = IndustryResources
    autocomplete_fields = ('parent', 'licence', 'ccc', 'consumer')
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent',
                    'licence', 'ccc', 'consumer')


class AliasIndustryAdmin(ImportExportActionModelAdmin):
    # resource_class = IndustryResources
    search_fields = ('name', )
    list_display = ('name', 'industry_id', 'ccc_id', 'licence_id', )


class AreaAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = AreaResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )


class UserInfoAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    autocomplete_fields = ('user', 'area', )
    list_display = ('user', 'area', )


class InspectionAdmin(ImportExportActionModelAdmin):
    resource_class = InspectionResources
    search_fields = ('title', )
    list_display = ('title', 'pubtime', 'source',
                    'qualitied', 'category', 'level', )


class EnterpriseAdmin(ImportExportActionModelAdmin):
    pass


# class InspectionEnterpriseAdmin(ImportExportActionModelAdmin):
#     pass


class ArticleAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = ArticleResources
    search_fields = ('title', 'source', )
    list_display = ('title', 'url', 'pubtime', 'source', 'score', )


class CategoryAdmin(ImportExportActionModelAdmin):
    resource_class = CategoryResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )


class ArticleCategoryAdmin(ImportExportActionModelAdmin):
    pass


class DMLinkAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    autocomplete_fields = ('create_by', )
    list_display = ('name', 'link', 'kwords', 'fwords',
                    'create_at', 'create_by', 'status', )


class IndustryProductsAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = IndustryProductsResources
    search_fields = ('name', 'industry_id')
    list_display = ('name', 'industry_id')


class VersionRecordAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    # resource_class = VersionRecordResources
    search_fields = ('id', 'content')
    list_display = ('version', 'content', 'pubtime')


admin.site.register(CPCIndustry, CPCIndustryAdmin)
admin.site.register(CCCIndustry, CCCIndustryAdmin)
admin.site.register(LicenceIndustry, LicenceIndustryAdmin)
admin.site.register(ConsumerIndustry, ConsumerIndustryAdmin)
admin.site.register(MajorIndustries, MajorIndustriesAdmin)
admin.site.register(HistoryIndustries, HistoryIndustriesAdmin)
admin.site.register(MajorIndustry, MajorIndustryAdmin)
admin.site.register(AliasIndustry, AliasIndustryAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Enterprise, EnterpriseAdmin)
# admin.site.register(InspectionEnterprise, InspectionEnterpriseAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CorpusCategories)
# admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(DMLink, DMLinkAdmin)
admin.site.register(IndustryProducts, IndustryProductsAdmin)
admin.site.register(VersionRecord, VersionRecordAdmin)
