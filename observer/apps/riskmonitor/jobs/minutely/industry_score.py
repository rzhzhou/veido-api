import os
import sys
import django
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.getcwd()+'/../../../../../'))
reload(sys)
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
django.setup()

from django.db.models import Sum

from observer.apps.riskmonitor.models import (
   RiskNews, Industry, ScoreIndustry)

# first = Industry.objects.all()
# print first[3].industrys.all()

def reprinted_per_industry(industry):
    sum_reprinted = industry.industrys.aggregate(
        reprinted=Sum('reprinted'))
    return sum_reprinted['reprinted']

def make_score():
    all_reprinted = RiskNews.objects.aggregate(
	reprinted=Sum('reprinted'))['reprinted']
    industrys = Industry.objects.all()
    for industry in industrys:
	per_reprint = reprinted_per_industry(industry)

	if per_reprint is None:
	    ScoreIndustry(score=0, industry=industry).save()
	else:			
	    score = (float(reprinted_per_industry(industry)) / all_reprinted) * 100
	    score = "%.2f"%score
	    ScoreIndustry(score=score, industry=industry).save()
make_score()
