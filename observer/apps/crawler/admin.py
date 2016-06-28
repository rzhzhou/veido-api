# -*- conding: utf-8 -*-
from django.contrib import admin
from models import Task, TaskConf


class TaskAdmin(admin.ModelAdmin):

    fields = ('app', 'module', 'crawlerimpl', 'rank', 'url', 'data', 'priority',
              'interval', 'timeout', 'create_at', 'update_at', 'last_run',
              'next_run', 'status')
    list_display = ('app', 'module', 'crawlerimpl', 'rank',
                    'url', 'priority', 'interval', 'timeout', 'next_run', 'status')
    list_filter = ('app', 'module', 'crawlerimpl', 'rank',
                   'status', 'next_run', 'priority')
    search_fields = ('priority',)
    readonly_fields = ('create_at', 'update_at', 'last_run', 'next_run')


class TaskConfAdmin(admin.ModelAdmin):
    fields = ('app', 'module', 'crawlerimpl', 'rank', 'priority', 'interval',
              'timeout', 'create_at', 'update_at', 'status')
    list_display = ('app', 'module', 'crawlerimpl', 'rank',
                    'priority', 'interval', 'timeout', 'priority', 'status')
    list_filter = ('app', 'module', 'crawlerimpl',
                   'rank', 'status', 'priority')
    search_fields = ('priority', 'status', 'type', )
    readonly_fields = ('create_at', 'update_at')

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskConf, TaskConfAdmin)
