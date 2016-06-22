import os
import sys
import django

reload(sys)
sys.path.append('/home/feng/Project/observer/api/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "observer.settings.development")
django.setup()

from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django_extensions.management.jobs import BaseJob

from observer.apps.base.models import Area
from observer.apps.riskmonitor.models import (Industry, RiskNews,
                                              ScoreIndustry, UserArea,
                                              UserIndustry)


class Job(BaseJob):

    def __init__(self):
        self.base_score = 100
        self.reduce_score = 1
        self.user = 'changzhou'
        self.cycle = 90
        self.time = datetime.today() - timedelta(days=1)

    def reducescore(self, industry, areas):
        tz = pytz.timezone('UTC')
        end = tz.localize(self.time).replace(hour=23, minute=59, second=59, microsecond=0)
        start = end.replace(hour=0, minute=0, second=0, microsecond=0)
        risknews = RiskNews.objects.filter(pubtime__range=(start, end), industry=industry,
                                            area__in=areas)
        reducescore = risknews.count() * self.reduce_score
        return reducescore

    def industry_make_score(self, user, areas):
        user_industrys = UserIndustry.objects.filter(user=user)
        industrys = [i.industry for i in user_industrys]

        for i in industrys:
            upresult = ScoreIndustry.objects.filter(industry=i, user=user).order_by('-pubtime')
            if upresult:
                increment = upresult[0].increment + 1
                upscore = upresult[0].score

            else:
                increment = 0
                upscore = self.base_score

            scoreindustry = ScoreIndustry.objects.filter(increment=(
                                    increment - self.cycle),
                                    industry=i)
            addscore = int(scoreindustry[0].reducescore) if scoreindustry else 0
            ScoreIndustry(score=(int(upscore) - self.reducescore(i, areas) +
                addscore), increment=increment, reducescore=self.reducescore(i, areas),
                industry=i,
                pubtime=self.time,
                user=user
                ).save()

    def get_areas(self, area):
        """
        获取某个地域下所有地区(包括该地域)，地域为全国不适用于此方法
        """
        lower_level = Area.objects.filter(parent_id=area.id)
        lower_id = map(lambda x: x.id, lower_level)
        areas = Area.objects.filter(
                Q(parent_id__in=lower_id) | Q(parent_id=area.id) | Q(id=area.id))
        return areas

    def execute(self):
        users = UserArea.objects.all()
        for u in users:
            areas = self.get_areas(u.area)
            self.industry_make_score(u.user, areas)


Job().execute()
