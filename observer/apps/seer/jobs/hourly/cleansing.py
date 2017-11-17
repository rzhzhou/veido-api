
from datetime import date, timedelta
from django_extensions.management.jobs import HourlyJob

from observer.apps.corpus.models import Corpus
from observer.apps.seer.models import RiskNews


class Job(HourlyJob):
    help = "Get Cleansing job."

    def execute(self):
        for corpus_obj in Corpus.objects.exclude(invalidword=''):
            for invalidword in corpus_obj.invalidword.split(' '):
                RiskNews.objects.filter(industry=corpus_obj.industry).filter(title__contains=invalidword).update(status=-1, invalid_keyword=invalidword)
