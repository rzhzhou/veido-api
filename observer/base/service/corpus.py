from datetime import datetime 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import (Corpus, )
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class CorpusData(Abstract):

    def __init__(self, params):
        super(CorpusData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'riskword', 'invalidword', 'industry__name', )

        cond = {
            'industry__id': getattr(self, 'industry_id', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Corpus.objects.fields.filter(**args).values(*fields)

        return queryset
