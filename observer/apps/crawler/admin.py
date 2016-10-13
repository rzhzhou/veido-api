# -*- conding: utf-8 -*-
from django.contrib import admin
from models import Task, TaskConf


class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'crawler'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'crawler' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'crawler' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'crawler' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'crawler' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'crawler' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


class TaskAdmin(MultiDBModelAdmin):

    fields = ('app', 'sub_app', 'file', 'rank', 'url', 'data', 'priority',
              'interval', 'timeout', 'create_at', 'update_at', 'last_run',
              'next_run', 'status')
    list_display = ('app', 'sub_app', 'file', 'rank',
                    'url', 'priority', 'interval', 'timeout', 'next_run', 'status')
    list_filter = ('app', 'sub_app', 'file', 'rank',
                   'status', 'next_run', 'priority')
    search_fields = ('priority',)
    readonly_fields = ('create_at', 'update_at', 'last_run', 'next_run')


class TaskConfAdmin(MultiDBModelAdmin):

    fields = ('app', 'sub_app', 'file', 'rank', 'priority', 'interval',
              'timeout', 'create_at', 'update_at', 'status')
    list_display = ('app', 'sub_app', 'file', 'rank', 'interval', 'timeout', 'priority', 'status')
    list_filter = ('app', 'sub_app', 'file',
                   'rank', 'status', 'priority')
    search_fields = ('priority', 'status', 'type', )
    readonly_fields = ('create_at', 'update_at')

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskConf, TaskConfAdmin)
