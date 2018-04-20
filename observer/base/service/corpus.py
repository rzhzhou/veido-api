from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import (Corpus, AliasIndustry, )
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
        invalidword = getattr(self, 'invalidword', '')
        industry_id = getattr(self, 'industry_id', '')

        if not industry_id:
            return 400

        industry = AliasIndustry.objects.get(id=industry_id)
        if Corpus.objects.filter(industry=industry).exists():
            return 202

        Corpus(
            riskword=riskword,
            invalidword=invalidword,
            industry=industry,
        ).save()

        return 200


class CorpusEdit(Abstract): 

    def __init__(self, user, params={}):
        super(CorpusEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        riskword = getattr(self, 'riskword', '')
        invalidword = getattr(self, 'invalidword', '')

        corpus = Corpus.objects.get(id=edit_id)
        corpus.riskword = riskword
        corpus.invalidword = invalidword
        corpus.save()

        return 200


class CorpusDelete(Abstract): 

    def __init__(self, user):
        self.user = user

    def delete(self, cid):
        del_id = cid
        Corpus.objects.filter(guid=del_id).delete()
        
        return 200
