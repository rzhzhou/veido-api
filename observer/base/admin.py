from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportActionModelAdmin
from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import (
								Industry, CCCIndustry, LicenseIndustry, 
								AliasIndustry, 
								)
from observer.base.resource import IndustryResources
from observer.utils.str_format import str_to_md5str


class IndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    resource_class = IndustryResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )
    

class CCCIndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    # resource_class = IndustryResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )
    

class LicenseIndustryAdmin(ImportExportActionModelAdmin, ForeignKeyAutocompleteAdmin):
    # resource_class = IndustryResources
    autocomplete_fields = ('parent', )
    search_fields = ('id', 'name', )
    list_display = ('id', 'name', 'level', 'parent', )
    

class AliasIndustryAdmin(ImportExportActionModelAdmin):
    # resource_class = IndustryResources
    search_fields = ('name', )
    list_display = ('name', 'industry_id', 'ccc_id', 'license_id', )


admin.site.register(Industry, IndustryAdmin)
admin.site.register(CCCIndustry, CCCIndustryAdmin)
admin.site.register(LicenseIndustry, LicenseIndustryAdmin)
admin.site.register(AliasIndustry, AliasIndustryAdmin)
