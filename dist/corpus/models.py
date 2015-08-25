#coding=utf-8
from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name=u'标题')
    class Meta:
            app_label = 'corpus'
            db_table = 'event'
            verbose_name_plural = u'聚类事件'

    def __unicode__(self):
        return self.title