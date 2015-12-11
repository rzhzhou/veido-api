# -*- coding: utf-8 -*-
import os
import sys
import django

reload(sys)
root_mod = '/home/sli/workweb/api/'
sys.path.append(root_mod)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "observer.settings.development");
django.setup()

from datetime import datetime, timedelta, date

from django.db.models import Sum
from django.shortcuts import render
from django.db import connection

from observer.apps.base.models import Area
from observer.apps.riskmonitor.models import (RiskNews, 
    Industry)
from observer.apps.base.views import BaseAPIView

def get_reprinted(industry, starttime, endtime):
    part_reprinted = RiskNews.objects.filter(industry=
        industry, pubtime__range=(starttime, endtime)
        ).aggregate(Sum('reprinted'))['sum_reprinted']
    print part_reprinted
    return part_reprinted

def same_compare(industry, starttime, endtime):
    start_last_year = starttime + timedelta(year=1)
    end_last_year = endtime + timedelta(year=1)
    compare_now = get_reprinted(industry, starttime, endtime)
    compare_last = get_reprinted(industry, start_last_year, end_last_year) 
    compare = ((compare_now / compare_last) -1) * 100
    return compare

def loop_compare(industry, starttime, endtime):
    range_time = (endtime - starttime).days


class RiskTotal(BaseAPIView):
    def point(self, part_news, all_news):
        part = part_news.aggregate(Sum('reprinted'))['sum_reprinted']
        alls = all_news.aggregate(Sum('reprinted'))['sum_reprinted']
        point_num = float("%.2f"%(float(part) / alls))
        return point_num
 
    def get(self, request, id):
        user = request.myuser
        area_news = RiskNews.objects.filter(area=user.area)
        all_news = RiskNews.objects.all()
        point_num = self.point(area_news, all_news)
        return None


class RiskRankView(RiskTotal):
    def get(self, request, id):
        container = self.requesthead(
            limit_list=settings.INDUSTRY_PAGE_LIMIT)
        user = request.myuser
        area_id = user.area.id
        sql = """
        SELECT * FROM (SELECT industry.`name`,area.`id` ,SUM(`risk_news`.`reprinted`) AS `reprinted__sum` FROM industry 
        LEFT JOIN risk_news_industry ON industry.`id`=risk_news_industry.`industry_id`
        LEFT JOIN risk_news ON risk_news.`id`=risk_news_industry.`risknews_id`
        LEFT JOIN yqj2.area ON risk_news.`area_id`=area.`id` WHERE area.`id`=%s
        GROUP BY industry.`name` ) AS reprinted
        ORDER BY reprinted__sum DESC
        """
        if container['type']=='enterprise':
            sql = sql.replace('industry', 'enterprise')
        cursor = connection.cursor()
        try:
            cursor.execute(sql, [area_id, ])
            result = cursor.fetchall()
        finally:
            cursor.close()
        return result





    