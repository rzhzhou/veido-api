from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import Corpus
from observer.utils.crawler.api import CrawlerTask
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

        return 200


class CorpusEdit(Abstract):

    def __init__(self, user, params={}):
        super(CorpusEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        riskword = getattr(self, 'riskword', '')

        corpus = Corpus.objects.get(id=edit_id)
        corpus.riskword = riskword
        corpus.save()

        return 200


class CorpusDelete(Abstract):

    def __init__(self, user, params={}):
        super(CorpusDelete, self).__init__(params)
        self.user = user

    def delete(self, cid):
        del_ids = cid
        industrys = getattr(self, 'name', '')
        riskwords = getattr(self, 'riskword', '')

        for (ids, industry, riskword) in zip(del_ids.split(","), industrys.split(","), riskwords.split(",")):
            CrawlerTask(industry, riskword).remove()
            Corpus.objects.filter(id=ids).delete()

        return 200


class CrawlerData(Abstract):

    def __init__(self, user, params={}):
        super(CrawlerData, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_ids = cid
        status = getattr(self, 'status', '')
        industrys = getattr(self, 'name', '')
        riskwords = getattr(self, 'riskword', '')

        for (ids, industry, riskword) in zip(edit_ids.split(","), industrys.split(","), riskwords.split(",")):
            CrawlerTask(industry, riskword).build()
            corpus = Corpus.objects.get(id=ids)
            corpus.status = status
            corpus.save()

        return 200
