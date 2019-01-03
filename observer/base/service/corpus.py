from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Corpus_categories, Category
from observer.utils.crawler.api import CrawlerTask, CrawlerTask_category
import os
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class CorpusData(Abstract):

    def __init__(self, params):
        super(CorpusData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'riskword', 'invalidword', 'industry__id', 'industry__name', )

        cond = {
            'industry__id': getattr(self, 'industry_id', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Corpus.objects.filter(**args).values(*fields)

        return queryset


class CorpusAdd(Abstract):

    def __init__(self, user, params={}):
        super(CorpusAdd, self).__init__(params)
        self.user = user

    def add(self):
        
        keyword = getattr(self, 'keyword', '')
        category_id = getattr(self, 'category_id', '')
        industry_id = getattr(self, 'industry_id') if getattr(self, 'industry_id') else 0

        if not category_id:
            return 400

        if Corpus_categories.objects.filter(category_id=category_id, keyword=keyword, industry_id=industry_id).exists():
            return 202

        Corpus_categories(
            keyword=keyword,
            category_id=category_id,
            industry_id=industry_id,
        ).save()

        return 200


class CorpusEdit(Abstract):

    def __init__(self, user, params={}):
        super(CorpusEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        keyword = getattr(self, 'keyword', None)

        corpus_categories = Corpus_categories.objects.get(id=edit_id)
        corpus_categories.keyword = keyword
        corpus_categories.save()

        return 200


class CorpusDelete(Abstract):

    def __init__(self, user, params={}):
        super(CorpusDelete, self).__init__(params)
        self.user = user

    def delete(self, cid):
        del_ids = cid
        status = getattr(self, 'status')
        keywords = getattr(self, 'keyword', '')
        category_ids = getattr(self, 'category_id', '')
        industry_ids = getattr(self, 'industry_id', '')
        if status == 1:
            for (ids, keyword, category_id, industry_id) in zip(del_ids.split(","), keywords.split(","), category_ids.split(","), industry_ids.split(",")):
                CrawlerTask_category(keyword, category_id, industry_id).remove()
                Corpus_categories.objects.filter(id=ids).delete()
        else:
            for (ids, keyword, category_id, industry_id) in zip(del_ids.split(","), keywords.split(","), category_ids.split(","), industry_ids.split(",")):
                Corpus_categories.objects.filter(id=ids).delete()

        return 200



class CrawlerData(Abstract):

    def __init__(self, user, params={}):
        super(CrawlerData, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_ids = cid
        status = getattr(self, 'status', '')
        keywords = getattr(self, 'keyword', '')
        category_ids = getattr(self, 'category_id')
        industry_ids = getattr(self, 'industry_id')

        for (ids, keyword, category_id, industry_id) in zip(edit_ids.split(","), keywords.split(","), category_ids.split(","), industry_ids.split(",")):
            CrawlerTask_category(keyword, category_id, industry_id).build()
            corpus_categories = Corpus_categories.objects.get(id=ids)
            corpus_categories.status = status
            corpus_categories.save()

        return 200

class CategoryListData(Abstract):
    
    def __init__(self, params):
        super(CategoryListData, self).__init__(params)

    def get_all(self):
        filter = ('id', 'name')

        cond = {
            'level': getattr(self, 'level', None),
            'parent': getattr(self, 'parent', None),
            'name__icontains': getattr(self, 'text', None),
        }

        args = dict([k,v] for k, v in cond.items() if v)

        queryset = Category.objects.filter(**args).values(*filter)

        return queryset
        
