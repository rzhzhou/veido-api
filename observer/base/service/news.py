from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.apps.officialsite.models import News
import os
from observer.base.service.abstract import Abstract


class ViewsData(Abstract):

    def __init__(self, params):
        super(ViewsData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'title', 'photo', 'content', 'pubtime', 'tag', 'views')

        cond = {
            'title__contains': getattr(self, 'title', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = News.objects.using('shendu').filter(**args).values(*fields)

        return queryset


class NewsAdd(Abstract):

    def __init__(self, user, params={}):
        super(NewsAdd, self).__init__(params)
        self.user = user

    def add(self):
        title = getattr(self, 'title', '')
        tag = getattr(self, 'tag', '')
        content = getattr(self, 'content', '')
        abstract = getattr(self, 'abstract', '')
        photo = getattr(self, 'photo', '')

        if not title or not tag or not content or not abstract:
            return 400

        if News.objects.using('shendu').filter(title=title, tag=tag, abstract=abstract).exists():
            return 202

        News(
            title=title,
            tag=tag,
            content=content,
            abstract=abstract,
            photo=photo,
        ).save(using='shendu')

        return 200
