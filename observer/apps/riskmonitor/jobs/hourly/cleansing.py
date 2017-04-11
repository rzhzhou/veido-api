# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django_extensions.management.jobs import HourlyJob

from observer.apps.corpus.models import Corpus
from observer.apps.riskmonitor.models import RiskNews


class Job(HourlyJob):
    help = "Get Cleansing job."

    def execute(self):
        for corpus_obj in Corpus.objects.exclude(invalidword=u''):
            RiskNews.objects.filter(industry=corpus_obj.industry).filter(title__contains=corpus_obj.invalidword).delete()
