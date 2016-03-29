import os
import sys
import django
reload(sys)
sys.path.append('/home/code/gitlab/test/api/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "observer.settings.development")
django.setup()

import pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django_extensions.management.jobs import BaseJob
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from observer.apps.riskmonitor.models import (
    RiskNews, ScoreIndustry, UserIndustry, Industry)


class Job(BaseJob):

    def __init__(self):
        self.base_score = 100
        self.reduce_score = 1
        self.user = 'changzhou'
        self.cycle = 90
        self.time = datetime.today() - timedelta(days=1)

    def reducescore(self, industry):
        tz = pytz.timezone(settings.TIME_ZONE)
        end = tz.localize(self.time).replace(hour=0, minute=0, second=0, microsecond=0)
        start = (end - timedelta(days=1))
        risknews = RiskNews.objects.filter(pubtime__range=(start, end), industry=industry)
        reducescore = risknews.count() * self.reduce_score
        return reducescore

    def industry_make_score(self):
        user = User.objects.get(username=self.user)
        industrys = Industry.objects.all()

        upresult = ScoreIndustry.objects.last()
        for i in industrys:
            if upresult:
                increment = upresult.increment + 1
                upscore = ScoreIndustry.objects.filter(increment=upresult.increment,
                    industry=i)[0].score

                scoreindustry = ScoreIndustry.objects.filter(increment=(
                                        increment - self.cycle),
                                        industry=i)
                addscore = int(scoreindustry[0].reducescore) if scoreindustry else 0

                ScoreIndustry(score=(int(upscore) - self.reducescore(i) +
                    addscore), increment=increment, reducescore=self.reducescore(i),
                    industry=i,
                    pubtime=self.time
                    ).save()
            else:
                ScoreIndustry(score=100,
                                industry=i,
                                pubtime=self.time
                                ).save()

    def execute(self):
        pass

Job().industry_make_score()
