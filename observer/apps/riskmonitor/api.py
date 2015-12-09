# -*- coding: utf-8 -*-
import os
import sys
import django

reload(sys)
root_mod = '/home/sli/workweb/api/'
sys.path.append(root_mod)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
django.setup()

from django.db.models import Sum
from django.shortcuts import render

from observer.apps.riskmonitor.models import (RiskNews, 
    )


def same_compare():
    print RiskNews.objects.filter().aggregate(Sum('reprinted'))

same_compare()