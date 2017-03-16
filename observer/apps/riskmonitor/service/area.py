# -*- coding: utf-8 -*-
from random import randint
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta

from observer.utils.date.convert import datetime_to_timestamp
from observer.apps.origin.models import Inspection
from observer.apps.riskmonitor.models import (
    RiskNews, ScoreIndustry, AreaIndustry, Industry, ManageIndex, SocietyIndex, ConsumeIndex, UserArea, SummariesScore, InternetScore)
from observer.apps.riskmonitor.service.news import NewsQuerySet


class Area(Industry):

    def __init__(self, params={}):
        super(IndustryTrack, self).__init__(params)

    def get_area_enterprise_count(self):
        industries = self.get_industries()[:3]

        for i in industries:
            Inspection.objects.filter(industry__id=i.id)

    def get_all(self):
        data = {
            'name': Industry.objects.get(pk=self.industry).name,
            'risk_rank': self.get_total_risk_rank(),
            'indicators': self.get_dimension(),
            'trend': self.trend_chart()
        }
        return data
