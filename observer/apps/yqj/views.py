# -*- coding: utf-8 -*-
import time
import uuid
import random
import jwt
import pytz

from datetime import date, datetime, timedelta
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, Q
from django.views.generic import View
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from observer.utils.date import pretty
from observer.utils.date.convert import utc_to_local_time
from observer.utils.excel import xls_to_response
from observer.utils.excel.briefing import article
from observer.utils.decorators.cache import token
from observer.utils.connector.redisconnector import RedisQueryApi
from observer.apps.yqj.models import (WeixinPublisher, Weixin, WeiboPublisher, Weibo,
                                              ArticlePublisher, Article,
                                              Topic, Risk, RelatedData, Category, 
                                              Group, User, Custom, CustomKeyword, Collection,
                                              ArticleCollection, TopicCollection, Inspection,
                                              GroupAuthUser, LocaltionScore, RiskScore, Area)

from observer.apps.yqj.service.news import NewsQuerySet
from observer.apps.yqj.service.risknews import RiskNewsQuerySet
from observer.apps.yqj.service.event import EventQuerySet
from observer.apps.yqj.service.inspection import InspectionQuerySet
from observer.apps.yqj.service.article import ArticleQuerySet


class BaseView(APIView):

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.query_params = {
            'start': self.today - timedelta(days=30),
            'end': self.today,
        }

    def set_params(self, params):
        for k, v in params.iteritems():
            self.query_params[k] = v
        self.page=self.query_params.get('page')

        #start, end convert to local datetime
        self.query_params['start'], self.query_params['end'] = utc_to_local_time(
            [self.query_params['start'], self.query_params['end']]
        )

        #end add 1 day
        self.query_params['end'] = self.query_params['end'] + timedelta(days=1)

    def paging(self, queryset, page, num):
        paginator = Paginator(queryset, num)  # Show $num <QuerySet> per page

        try:
            results = paginator.page(page)   
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.   
            results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of  
            # results.
            results = paginator.page(paginator.num_pages)

        return results


class NewsView(BaseView):
    def __init__(self):
        super(NewsView, self).__init__()

    def set_params(self, request):
        super(NewsView, self).set_params(request.GET)
        self.category_id = self.query_params.get('category_id')
        self.area_id = self.query_params.get('area_id')

    def paging(self, queryset):
        return super(NewsView, self).paging(queryset, self.page, self.query_params['length'])

    def serialize(self, queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsTotal": NewsQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'], category_id=self.category_id, area_id=self.area_id).count(),
            "recordsFiltered": NewsQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'], category_id=self.category_id, area_id=self.area_id).count(),
            "data":map(lambda r:{
                'id':r['id'],
                'title':r['title'],
                'source': r['source'],
                'area': Area.objects.get(pk = r['area']).name,
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        } 

        return data

    def get(self, request):
        self.set_params(request)

        queryset = NewsQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'], category_id=self.category_id, area_id=self.area_id).order_by('-pubtime')

        return Response(self.serialize(queryset))



class RiskView(BaseView):
    def __init__(self):
        super(RiskView, self).__init__()

    def set_params(self, request):
        super(RiskView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(RiskView, self).paging(queryset, self.page, self.query_params['length'])

    def serialize(self,queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": RiskNewsQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'],).count(),
            "data":map(lambda r:{
                "riskScore": RiskScore.objects.get(risk__id=r['id']).score,
                'relevance': LocaltionScore.objects.get(pk=r['id']).score,
                'id':r['id'],
                'title':r['title'],
                'source': r['source'],
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }

        return data
        

    def get(self, request):
        self.set_params(request)
        queryset =RiskNewsQuerySet(params = self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'],).order_by('-pubtime')
        return Response(self.serialize(queryset))


class EventView(BaseView):
    def __init(self):
        super(EventView,self).__init__()


    def set_params(self,request):
        super(EventView,self).set_params(request.GET)

    def paging(self,queryset):
        return super(EventView,self).paging(queryset,self.page,self.query_params['length'])

    def serialize(self,queryset):
        results =self.paging(queryset)

        data={
            "recordsTotal": EventQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'],).count(),
            "data":map(lambda r:{
                'id':r['id'],
                'title':r['title'],
                'source': r['source'],
                'area':Area.objects.get(pk=r['area']).name,
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset =EventQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'],).order_by('-pubtime')
        return Response(self.serialize(queryset))


class InspectionTableView(BaseView):
    def __init__(self):
        super(InspectionTableView,self).__init__()

    def set_params(self, request):
        super(InspectionTableView,self).set_params(request.GET)

    def paging(self, queryset):
        return super(InspectionTableView, self).paging(queryset, self.page, self.query_params['length'])


    def serialize(self, queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": InspectionQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['start'], endtime=self.query_params['end'],).count(),
            "data":map(lambda r:{
                'id':r['id'],
                'name':r['name'],
                'source': r['source'],
                'product': r['product'],
                'qualitied':"%.2f%%" % (r['qualitied'] * 100),
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset =InspectionQuerySet(params=self.query_params).get_all_news_list(starttime=self.query_params['start'], endtime=self.query_params['end']).order_by('-pubtime')

        return Response(self.serialize(queryset))
        





        