from __future__ import unicode_literals

from django.db import models


class Task(models.Model):
    app = models.CharField(max_length=255, verbose_name='应用')
    sub_app = models.CharField(blank=True, max_length=255, verbose_name='子应用')
    file = models.CharField(max_length=255, verbose_name='文件名')
    rank = models.IntegerField(verbose_name='等级')
    url = models.URLField(verbose_name='链接')
    data = models.TextField(blank=True, verbose_name='数据')
    priority = models.IntegerField(verbose_name='优先级')
    interval = models.IntegerField(verbose_name='周期')
    timeout = models.IntegerField(verbose_name='超时时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_run = models.DateTimeField(verbose_name='上次执行结束时间')
    next_run = models.DateTimeField(verbose_name='下次运行开始时间')
    status = models.IntegerField(verbose_name='状态')

    class Meta:
        app_label = 'crawler'
        ordering = ['-rank', 'next_run', '-priority']
        verbose_name_plural = u'爬虫任务'

    def __unicode__(self):
        return self.url


class TaskConf(models.Model):
    app = models.CharField(max_length=255, verbose_name='应用')
    sub_app = models.CharField(blank=True, max_length=255, verbose_name='子应用')
    file = models.CharField(max_length=255, verbose_name='文件名')
    rank = models.IntegerField(verbose_name='等级')
    priority = models.IntegerField(verbose_name='优先级')
    interval = models.IntegerField(verbose_name='周期')
    timeout = models.IntegerField(verbose_name='超时时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.IntegerField(verbose_name='状态')

    class Meta:
        app_label = 'crawler'
        verbose_name_plural = u'爬虫任务配置'

    def __unicode__(self):
        if not self.sub_app:
            crawler_key = [self.app, self.file, str(self.rank)]
        else:
            crawler_key = [self.app, self.sub_app, self.file, str(self.rank)]
        return '.'.join(crawler_key)
