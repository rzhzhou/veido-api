import datetime

from django.db import models
from tinymce.models import HTMLField


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题')
    photo = models.ImageField(upload_to='photos', verbose_name='封面')
    content = HTMLField(verbose_name='内容')
    pubtime = models.DateField(default=datetime.date.today, verbose_name='发布时间')
    tag = models.CharField(default='', max_length=255, verbose_name='标签')
    views = models.IntegerField(default=0, verbose_name='浏览次数')
    abstract = models.CharField(default='', max_length=255, verbose_name='摘要')

    class Meta:
        app_label = 'apps'
        db_table = 'base_news'
        verbose_name_plural = u'公司动态'

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def __unicode__(self):
        return self.title
