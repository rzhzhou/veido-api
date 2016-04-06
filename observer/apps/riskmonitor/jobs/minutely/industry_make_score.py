import os
import sys
from datetime import datetime, timedelta

import django
import pytz
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django_extensions.management.jobs import BaseJob

from observer.apps.riskmonitor.models import (Industry, RiskNews,
                                              ScoreIndustry, UserArea,
                                              UserIndustry)

reload(sys)
sys.path.append('/home/code/gitlab/test/api/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "observer.settings.development")
django.setup()




class Job(BaseJob):

    def __init__(self):
        self.base_score = 100
        self.reduce_score = 1
        self.user = 'changzhou'
        self.cycle = 90
        self.time = datetime.today() - timedelta(days=1)

    def reducescore(self, industry, area):
        # tz = pytz.timezone(settings.TIME_ZONE)
        tz = pytz.timezone('UTC')
        end = tz.localize(self.time).replace(hour=23, minute=59, second=59, microsecond=0)
        start = end.replace(hour=0, minute=0, second=0, microsecond=0)
        risknews = RiskNews.objects.filter(pubtime__range=(start, end), industry=industry,
                                            area=area)
        reducescore = risknews.count() * self.reduce_score
        return reducescore

    def industry_make_score(self, user, area):
        try:
            user_industrys = UserIndustry.objects.filter(user=user)
            industrys = [i.industry for i in user_industrys]
        except ObjectDoesNotExist:
            industrys = []

        for i in industrys:
            upresult = ScoreIndustry.objects.filter(industry=i, user=user).order_by('-pubtime')
            if upresult:
                increment = upresult[0].increment + 1
                upscore = upresult[0].score

                scoreindustry = ScoreIndustry.objects.filter(increment=(
                                        increment - self.cycle),
                                        industry=i)
                addscore = int(scoreindustry[0].reducescore) if scoreindustry else 0
                ScoreIndustry(score=(int(upscore) - self.reducescore(i, area) +
                    addscore), increment=increment, reducescore=self.reducescore(i, area),
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
        users = UserArea.objects.all()
        for u in users:
            self.industry_make_score(u.user, u.area)


Job().execute()
