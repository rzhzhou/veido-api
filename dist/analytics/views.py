# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.response import Response
from django.db.models import Count,Q
from rest_framework.views import APIView
from yqj.models import Article, Weixin, Weibo, Area
from base.views import BaseView


class TableAPIView(APIView):
    def __init__(self, request=None):
        self.request = request


class LineTableView(TableAPIView):
    def get(self, request ):
        pass


class PieTypeTableView(TableAPIView):
    def get(self, request, start, end):
        article = Article.objects.filter(pubtime__range=(start,end)).count()
        weixin = WeiXin.objects.filter(pubtime__range=(start,end)).count() 
        weibo = Weibo.objects.filter(pubtime__range=(start,end)).count()

        return Response({'article': article, 'weixin': weixin, 'weibo': weibo})

class PieFeelingTableView(TableAPIView):
    def get(self, request, start, end):
        positive = Article.objects.filter(pubtime__range=(start,end), 
            feeling_factor__gte=0.6).count()

        normal = Article.objects.filter(pubtime__range=(start,end), 
            feeling_factor__gte=0.5, feeling_factor__lt=0.6).count()

        negative = Article.objects.filter(pubtime__range=(start,end), feeling_factor__lt=0.5).count()
    
        return Response({'positive':positive, 'normal': normal, 'negative': negative})


class PieAreaTableView(TableAPIView):
    def get(self, request, start, end):
    #SELECT id FROM yqj.`area` WHERE parent_id IN (SELECT id FROM yqj.`area` WHERE parent_id=2) OR parent_id=2 OR id =2

        pro_area = Area.objects.filter(level=2)
        pro_id = []
        for item in pro_area:
            pro_id.append(item.id)

        provice_count = []    
        for i in pro_id:
            city_area = Area.objects.filter(parent_id=i)
            city_id = []
            for c in city_area:
                city_id.append(c.id)
            one_pro = Area.objects.filter(Q(parent_id__in=city_id)|Q(parent_id=i)|Q(id=i))
            one_pro_id = [] 
            for items in one_pro:
                one_pro_id.append(items.id)
            count = Weibo.objects.filter(area__in=one_pro, pubtime__range=(start,end)).count()
            name =  Area.objects.get(id=i).name  
            provice_count.append({'name': name, 'count': count})
        sort_result = sorted(provice_count, key=lambda x:x['count'], reversed=True)[:6]
    
        return Response({'provice_count':provice_count, 'sort_result': sort_result})


class AnalyticsView(BaseView):
    def get(self, request):
        return self.render_to_response('analytics/analytics.html', {'industry': {'name': u'综合'}})

