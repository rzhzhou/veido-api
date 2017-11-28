from random import randint
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from datetime import date, datetime, timedelta

from observer.utils.date.convert import datetime_to_timestamp
from observer.apps.origin.models import Inspection
from observer.apps.seer.models import (
    RiskNews, ScoreIndustry, AreaIndustry, Industry, ManageIndex, SocietyIndex, ConsumeIndex, UserArea, SummariesScore, InternetScore)
from observer.apps.seer.service.news import NewsQuerySet
from observer.apps.seer.service.abstract import Abstract
from observer.apps.seer.service.industry import IndustryTrack


class Area(Abstract):

    def __init__(self, params={}):
        super(Area, self).__init__(params)
        self.industry_track = IndustryTrack(params)

    def get_area_enterprise_count(self):
        industries = self.industry_track.get_industries()[:3]

        for i in industries:
            Inspection.objects.filter(industry__id=i.id)

    def get_all(self):
        data = {
            'name': Industry.objects.get(pk=self.industry).name,
            'risk_rank': self.industry_track.get_total_risk_rank(),
            'indicators': self.industry_track.get_dimension(),
            'trend': self.industry_track.trend_chart()
        }
        return data
