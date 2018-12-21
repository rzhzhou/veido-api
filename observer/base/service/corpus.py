from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Corpus, Corpus_categories
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
        if getattr(self, 'industry_id', None):
            riskword = getattr(self, 'riskword', '')
            industry_id = getattr(self, 'industry_id', '')

            if not industry_id:
                return 400

            if Corpus.objects.filter(industry_id=industry_id, riskword=riskword).exists():
                return 202

            Corpus(
                riskword=riskword,
                industry_id=industry_id,
            ).save()
        else:
            keyword = getattr(self, 'keyword', '')
            category_id = getattr(self, 'category_id', '')

            if not category_id:
                return 400

            if Corpus_categories.objects.filter(category_id=category_id, keyword=keyword).exists():
                return 202

            Corpus_categories(
                keyword=keyword,
                category_id=category_id,
            ).save()

        return 200


class CorpusEdit(Abstract):

    def __init__(self, user, params={}):
        super(CorpusEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        if getattr(self, 'riskword', None):
            riskword = getattr(self, 'riskword', '')

            corpus = Corpus.objects.get(id=edit_id)
            corpus.riskword = riskword
            corpus.save()
        else:
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
        if getattr(self, 'industry_id', None):
            industrys = getattr(self, 'name', '')
            riskwords = getattr(self, 'riskword', '')
            industry_ids = getattr(self, 'industry_id')

            for (ids, industry, riskword, industry_id) in zip(del_ids.split(","), industrys.split(","), riskwords.split(","), industry_ids.split(",")):
                CrawlerTask(industry, riskword, industry_id).remove()
                Corpus.objects.filter(id=ids).delete()

        else:
            keywords = getattr(self, 'keyword', '')
            category_ids = getattr(self, 'category_id', '')

            for (ids, keyword, category_id) in zip(del_ids.split(","), keywords.split(","), category_ids.split(",")):
                CrawlerTask_category(keyword, category_id).remove()
                Corpus_categories.objects.filter(id=ids).delete()

        return 200



class CrawlerData(Abstract):

    def __init__(self, user, params={}):
        super(CrawlerData, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_ids = cid
        if getattr(self, 'industry_id', None):
            status = getattr(self, 'status', '')
            industrys = getattr(self, 'name', '')
            riskwords = getattr(self, 'riskword', '')
            industry_ids = getattr(self, 'industry_id')
            corpus_ids = getattr(self, 'corpus_id')

            for (ids, industry, riskword, industry_id, corpus_id) in zip(edit_ids.split(","), industrys.split(","), riskwords.split(","), industry_ids.split(","), corpus_ids.split(",")):
                CrawlerTask(industry, riskword, industry_id, corpus_id).build()
                corpus = Corpus.objects.get(id=ids)
                corpus.status = status
                corpus.save()
        else:
            status = getattr(self, 'status', '')
            keywords = getattr(self, 'keyword', '')
            category_ids = getattr(self, 'category_id')

            for (ids, keyword, category_id) in zip(edit_ids.split(","), keywords.split(","), category_ids.split(",")):
                CrawlerTask_category(keyword, category_id).build()
                corpus_categories = Corpus_categories.objects.get(id=ids)
                corpus_categories.status = status
                corpus_categories.save()

        return 200
