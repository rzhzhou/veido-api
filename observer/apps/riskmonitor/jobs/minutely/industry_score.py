import os
import sys
from datetime import datetime, timedelta

import django
import pytz
from django.conf import settings
from django.db.models import Sum

from observer.apps.riskmonitor.models import Industry, RiskNews, ScoreIndustry

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.getcwd()+'/'))
print PROJECT_ROOT
reload(sys)
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
django.setup()




# first = Industry.objects.all()
# print first[3].industrys.all()

def reprinted_per_industry(industry):
    sum_reprinted = industry.industrys.aggregate(
        reprinted=Sum('reprinted'))
    return sum_reprinted['reprinted']

def make_score():
    tz = pytz.timezone(settings.TIME_ZONE)
    start = tz.localize(datetime.strptime('2015-11-22', '%Y-%m-%d'))
    end = tz.localize(datetime.strptime('2015-12-4', '%Y-%m-%d'))

    all_reprinted = RiskNews.objects.aggregate(
	reprinted=Sum('reprinted'))['reprinted']
    industrys = Industry.objects.all()
    for industry in industrys:
	per_reprint = reprinted_per_industry(industry)

	if per_reprint is None:
	    ScoreIndustry(score=0, industry=industry, pubtime=start).save()
	else:
	    score = (float(reprinted_per_industry(industry)) / all_reprinted) * 100
	    score = "%.2f"%score
	    ScoreIndustry(score=score, industry=industry, pubtime=start).save()
make_score()
