import os
import sys

import django
from django.db.models import Sum

from observer.apps.riskmonitor.models import (Enterprise, RiskNews,
                                              ScoreEnterprise)

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.getcwd()+'/../../../../../'))
reload(sys)
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
django.setup()




def reprinted_per_enterprise(enterprise):
    sum_reprinted = enterprise.enterprises.aggregate(
        reprinted=Sum('reprinted'))
    return sum_reprinted['reprinted']


def make_score():
    all_reprinted = RiskNews.objects.aggregate(
	reprinted=Sum('reprinted'))['reprinted']
    enterprises = Enterprise.objects.all()
    
    for enterprise in enterprises:
	per_reprint = reprinted_per_enterprise(enterprise)
	if per_reprint is None:
	    ScoreEnterprise(score=0, enterprise=enterprise).save()
	else:			
	    score = (float(reprinted_per_enterprise(enterprise)) / all_reprinted) * 100
	    score = "%.2f"%score
	    ScoreEnterprise(score=score, enterprise=enterprise).save()
make_score()
