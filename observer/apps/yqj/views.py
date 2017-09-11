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
from observer.apps.yqj.models import (
        Group, User, Custom, CustomKeyword,
        ArticleCollection, GroupAuthUser, 
        LocaltionScore)
from observer.apps.base.models import Area, Article
from observer.apps.yqj.service.news import NewsQuerySet
from observer.apps.yqj.service.risknews import RiskNewsQuerySet
from observer.apps.yqj.service.event import EventQuerySet
from observer.apps.yqj.service.inspection import InspectionQuerySet
from observer.apps.yqj.service.reference import ReferenceQuerySet
from observer.apps.yqj.service.insight import InsightQuerySet
from observer.apps.yqj.service.website import WebsiteQuerySet
from observer.apps.yqj.service.custom import CustomQuerySet


class BaseView(APIView):

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.query_params = {
            'starttime': self.today - timedelta(days=30),
            'endtime': self.today,
        }

    def set_params(self, params):
        for k, v in params.iteritems():
            self.query_params[k] = v
        # self.start=self.query_params.get('start')


        #start, end convert to local datetime
        # print self.query_params['start'] , self.query_params['end']
        self.query_params['starttime'], self.query_params['endtime'] = utc_to_local_time(
            [self.query_params['starttime'], self.query_params['endtime']]
        )

        

        #end add 1 day
        self.query_params['endtime'] = self.query_params['endtime'] + timedelta(days=1)

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
        # print request.GET
        super(NewsView, self).set_params(request.GET)
        self.category_id = self.query_params.get('category_id')
        self.area_id = self.query_params.get('area_id')

    def paging(self, queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(NewsView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self, queryset):
        results = self.paging(queryset)

        data={
            "draw": self.query_params['draw'],
            "recordsTotal": NewsQuerySet(params=self.query_params).get_all_news_list().count(),
            "recordsFiltered": NewsQuerySet(params=self.query_params).get_all_news_list().count(),
            "data":map(lambda r:{
                'id':r['id'],
                'TitleAndUrl':(r['title'],r['url']),
                'source': ArticlePublisher.objects.get(pk =r['publisher_id']).publisher,
                'area': Area.objects.get(pk = r['area']).name,
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }   
        # print results
        return data

    def get(self, request):
        self.set_params(request)
        # print request.GET

        queryset = NewsQuerySet(params=self.query_params).get_all_news_list().order_by('-pubtime')

        return Response(self.serialize(queryset))



class RiskView(BaseView):
    def __init__(self):
        super(RiskView, self).__init__()

    def set_params(self, request):
        super(RiskView, self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(RiskView, self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self,queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": RiskNewsQuerySet(params=self.query_params).get_all_news_list(starttime =self.query_params['starttime'], endtime=self.query_params['endtime'],).count(),
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
        queryset =RiskNewsQuerySet(params = self.query_params).get_all_news_list(starttime =self.query_params['starttime'], endtime=self.query_params['endtime'],).order_by('-pubtime')
        return Response(self.serialize(queryset))


class EventView(BaseView):
    def __init(self):
        super(EventView,self).__init__()


    def set_params(self,request):
        super(EventView,self).set_params(request.GET)

    def paging(self,queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(EventView,self).paging(queryset, page, self.query_params.get('length'))

    def serialize(self,queryset):
        results =self.paging(queryset)

        data={
            "recordsTotal": EventQuerySet(params=self.query_params).get_all_news_list().count(),
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

        queryset =EventQuerySet(params=self.query_params).get_all_news_list().order_by('-pubtime')
        return Response(self.serialize(queryset))


class InspectionTableView(BaseView):
    def __init__(self):
        super(InspectionTableView,self).__init__()

    def set_params(self, request):
        super(InspectionTableView,self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(InspectionTableView, self).paging(queryset, page, self.query_params.get('length'))


    def serialize(self, queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": InspectionQuerySet(params=self.query_params).get_all_news_list().count(),
            "data":map(lambda r:{
                'id':r['id'],
                # 'name':r['title'],
                'TitleAndUrl':(r['title'],r['url']),
                'publisher':InspectionPublisher.objects.get(pk=r['publisher']).name,
                'product': r['product'],
                'qualitied':"%.2f%%" % (r['qualitied'] * 100),
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset =InspectionQuerySet(params=self.query_params).get_all_news_list().order_by('-pubtime')

        return Response(self.serialize(queryset))


class ReferenceView(BaseView):
    def __init__(self):
        super(ReferenceView,self).__init__()

    def set_params(self, request):
        super(ReferenceView,self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(ReferenceView, self).paging(queryset, page, self.query_params.get('length'))


    def serialize(self, queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": ReferenceQuerySet(params=self.query_params).get_all_news_list().count(),
            "data":map(lambda r:{
                'id':r['id'],
                # 'name':r['title'],
                'TitleAndUrl':(r['title'],r['url']),
                'publisher':ArticlePublisher.objects.get(pk=r['publisher']).publisher,
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset =ReferenceQuerySet(params=self.query_params).get_all_news_list().order_by('-pubtime')

        return Response(self.serialize(queryset))


class InsightView(BaseView):
    def __init__(self):
        super(InsightView,self).__init__()

    def set_params(self, request):
        super(InsightView,self).set_params(request.GET)

    def paging(self, queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(InsightView, self).paging(queryset, page, self.query_params.get('length'))


    def serialize(self, queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": InsightQuerySet(params=self.query_params).get_all_news_list().count(),
            "data":map(lambda r:{
                'id':r['id'],
                # 'name':r['title'],
                'TitleAndUrl':(r['title'],r['url']),
                'publisher':ArticlePublisher.objects.get(pk=r['publisher']).publisher,
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset =InsightQuerySet(params=self.query_params).get_all_news_list().order_by('-pubtime')

        return Response(self.serialize(queryset))


class WebsiteView(BaseView):
    def __init__(self):
        super(WebsiteView,self).__init__()

    def set_params(self, request):
        super(WebsiteView,self).set_params(request.GET)
        # self.keyword =

    def paging(self, queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(WebsiteView, self).paging(queryset, page, self.query_params.get('length'))


    def serialize(self, queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": WebsiteQuerySet(params=self.query_params).get_all_news_list().count(),
            "data":map(lambda r:{
                'id':r['id'],
                # 'name':r['title'],
                'TitleAndUrl':(r['title'],r['url']),
                'source':r['source'],
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset =WebsiteQuerySet(params=self.query_params).get_all_news_list().order_by('-pubtime')

        return Response(self.serialize(queryset))

class CustomNewsView(BaseView):
    def __init__(self):
        super(CustomNewsView,self).__init__()

    def set_params(self, request):
        super(CustomNewsView,self).set_params(request.GET)
        self.custom_id = int(self.query_params['custom_id'])

    def paging(self, queryset):
        page = (int(self.query_params['start']) /
                int(self.query_params['length'])) + 1
        return super(CustomNewsView, self).paging(queryset, page, self.query_params.get('length'))


    def serialize(self, queryset):
        results = self.paging(queryset)
        data={
            "draw": self.query_params['draw'],
            "recordsFiltered": len(results),
            "recordsTotal": CustomQuerySet(params=self.query_params).get_all_news_list(custom_id=self.custom_id ,starttime=self.query_params['starttime'], endtime=self.query_params['endtime'],).count(),
            "data":map(lambda r:{
                'id':r['id'],
                # 'name':r['title'],
                'TitleAndUrl':(r['title'],r['url']),
                'publisher':ArticlePublisher.objects.get(pk= r['publisher']).publisher,
                'pubtime':utc_to_local_time(r['pubtime']).strftime('%Y-%m-%d %H:%M'),
            },results)
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset =CustomQuerySet(params=self.query_params).get_all_news_list(custom_id=self.custom_id ,starttime=self.query_params['starttime'], endtime=self.query_params['endtime']).order_by('-pubtime')

        return Response(self.serialize(queryset))

        