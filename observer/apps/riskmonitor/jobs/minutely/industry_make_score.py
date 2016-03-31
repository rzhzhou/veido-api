import os
import sys
from datetime import datetime, timedelta

import django
reload(sys)
sys.path.append('/home/code/gitlab/test/api/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "observer.settings.development")
django.setup()

import pytz
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django_extensions.management.jobs import BaseJob

from observer.apps.riskmonitor.models import (Industry, RiskNews,
                                              ScoreIndustry, UserIndustry,
                                              UserArea)


class Job(BaseJob):

    def __init__(self):
        self.base_score = 100
        self.reduce_score = 1
        self.user = 'changzhou'
        self.cycle = 90
        self.time = datetime.today() - timedelta(days=4)

    def reducescore(self, industry, area):
        tz = pytz.timezone(settings.TIME_ZONE)
        end = tz.localize(self.time).replace(hour=23, minute=59, second=59, microsecond=0)
        start = end.replace(hour=0, minute=0, second=0, microsecond=0)
        risknews = RiskNews.objects.filter(pubtime__range=(start, end), industry=industry,
                                            area=area)
        reducescore = risknews.count() * self.reduce_score
        return reducescore

    def industry_make_score(self, user):
        try:
            area = UserArea.objects.get(user=user).area
            user_industrys = UserIndustry.objects.filter(user=user)
            industrys = [i.industry for i in user_industrys]
        except ObjectDoesNotExist:
            industrys = []

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
                    pubtime=self.time,
                    user=user
                    ).save()
            else:
                ScoreIndustry(score=100,
                                industry=i,
                                pubtime=self.time,
                                user=user
                                ).save()


    def execute(self):
        users = User.objects.all()
        for u in users:
            self.industry_make_score(u)


Job().execute()
