# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework.response import Response
from django.db.models import Count,Q
from rest_framework.views import APIView
from yqj.models import Article, Weixin, Weibo, Area
from base.views import BaseView
from datetime import datetime, timedelta


class DispatchView(APIView):

    def get(self, request, id):
        parameter = request.GET
        type = parameter['type'].replace('-', '_')
        start = parameter['start']
        end = parameter['end']
        page = parameter['page'] if parameter.has_key('page') else 0

        func = getattr(globals()['DispatchView'](), type)
        if page:
            return func(start, end, page)
        else:
            return func(start, end)

    def statistic(self, start, end):
        total = Article.objects.filter(pubtime__range=(start, end)).count()
        risk = total
        return Response({'total': total, 'risk': risk})

    def chart_type(self, start, end):
        try:
            article = Article.objects.filter(pubtime__range=(start,end)).count()
            weixin = Weixin.objects.filter(pubtime__range=(start,end)).count()
            weibo = Weibo.objects.filter(pubtime__range=(start,end)).count()
            return Response({'news': article, 'weixin': weixin, 'weibo': weibo})
        except:
            return Response({}) 

    def chart_emotion(self, start, end): 
        try:
            positive = Article.objects.filter(pubtime__range=(start,end),
                feeling_factor__gte=0.6).count()

            normal = Article.objects.filter(pubtime__range=(start,end),
                feeling_factor__gte=0.5, feeling_factor__lt=0.6).count()

            negative = Article.objects.filter(pubtime__range=(start,end), feeling_factor__lt=0.5).count()

            return Response({'positive':positive, 'normal': normal, 'negative': negative})
        except:
            return Response({})

    def chart_weibo(self, start, end):
        try:
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
                count = Weibo.objects.filter(area__in=one_pro, pubtime__range=(start,end)).count()
                name =  Area.objects.get(id=i).name
                provice_count.append({'name': name, 'value': count})
            sort_result = sorted(provice_count, key=lambda x:x['value'], reverse=True)[:6]

            return Response({'provice_count':provice_count, 'sort_result': sort_result})
        except:
            return Response({})

    def chart_trend(self, start, end):
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        date_range = end - start
        date = [(start + timedelta(days=x)).date() for x in xrange(date_range.days)]
        news_data = [Article.objects.filter(pubtime__gte=date[x], pubtime__lt=date[x] + timedelta(days=1)).count() for x in xrange(date_range.days)]
        weixin_data = [Weixin.objects.filter(pubtime__gte=date[x], pubtime__lt=date[x] + timedelta(days=1)).count() for x in xrange(date_range.days)]
        weibo_data = [Weibo.objects.filter(pubtime__gte=date[x], pubtime__lt=date[x] + timedelta(days=1)).count() for x in xrange(date_range.days)]
        total_data = [news_data[i] + weixin_data[i] + weibo_data[i] for i in xrange(len(date))]

        date = [i.strftime("%m-%d") for i in date]

        return Response({
        "date": date,
        "news_data": news_data,
        "weixin_data": weixin_data,
        "weibo_data": weibo_data,
        "total_data": total_data
        })


class AnalyticsView(BaseView):
    def get(self, request):
        return self.render_to_response('analytics/analytics.html', {'industry': {'name': u'综合'}})

