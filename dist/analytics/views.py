# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.views import APIView

from base.views import BaseTemplateView
from django.conf import settings
from yqj.models import Article, Area, Weixin, Weibo
from yqj.redisconnect import RedisQueryApi


class DispatchView(APIView, BaseTemplateView):

    def get(self, request, id):
        parameter = request.GET
        try:
            type = parameter['type'].replace('-', '_')
            start = parameter['start']
            end = parameter['end']
            page = parameter['page'] if parameter.has_key('page') else 0
            func = getattr(globals()['DispatchView'](), type)

            date_range = RedisQueryApi().hget('cache', 'date_range')
            if date_range:
                date_start = datetime.strptime(eval(date_range)['start'], '%Y-%m-%d')
                date_end = datetime.strptime(eval(date_range)['end'], '%Y-%m-%d')
                start_time = datetime.strptime(start, '%Y-%m-%d')
                end_time = datetime.strptime(end, '%Y-%m-%d')
                if date_start==start_time and date_end==end_time:
                    data = RedisQueryApi().hget('cache', type)
                    result = eval(data) if data else []
                    if result:
                        return Response(result)
            return func(start, end)
        except Exception, e:
            return Response({})


    def statistic(self, start, end):
        start = parse_date(start)
        end = parse_date(end)
        total = Article.objects.filter(pubtime__range=(start, end)).count()
        risk = total
        return Response({'total': total, 'risk': risk})

    def chart_type(self, start, end):
        start = parse_date(start)
        end = parse_date(end)
        article = Article.objects.filter(pubtime__range=(start,end)).count()
        weixin = Weixin.objects.filter(pubtime__range=(start,end)).count()
        weibo = Weibo.objects.filter(pubtime__range=(start,end)).count()
        return Response({'news': article, 'weixin': weixin, 'weibo': weibo})

    def chart_emotion(self, start, end):
        start = parse_date(start)
        end = parse_date(end)
        positive = Article.objects.filter(pubtime__range=(start,end),
                feeling_factor__gte=0.6).count()
        normal = Article.objects.filter(pubtime__range=(start,end),
            feeling_factor__gte=0.5, feeling_factor__lt=0.6).count()

        negative = Article.objects.filter(pubtime__range=(start,end), feeling_factor__lt=0.5).count()

        return Response({'positive':positive, 'normal': normal, 'negative': negative})

    def chart_weibo(self, start, end):
        start = parse_date(start)
        end = parse_date(end)
        provice_count = []
        provinces = Area.objects.filter(level=2)
        for province in provinces:
            citys = Area.objects.filter(parent_id=province.id)
            city_id = map(lambda c: c.id, citys)
            areas_id = Area.objects.filter(Q(parent_id__in=city_id)|Q(parent_id=province.id)|Q(id=province.id))
            count = Weibo.objects.filter(area__in=areas_id, pubtime__range=(start,end)).count()
            provice_count.append({'name': province.name, 'value': count})
        sort_result = sorted(provice_count, key=lambda x:x['value'])[-10:]
        name = map(lambda n: n['name'], sort_result)
        value = map(lambda v: v['value'], sort_result)
        return Response({'provice_count':provice_count, 'name': name, 'value': value})

    def chart_trend(self, start, end):
        start = parse_date(start)
        end = parse_date(end)
        days = (end - start).days
        date = [(start + timedelta(days=x)) for x in xrange(days)]
        news_data = map(lambda x: Article.objects.filter(pubtime__range=(
            date[x], date[x] + timedelta(days=1))).count(), xrange(days))
        weixin_data = map( lambda x: Weixin.objects.filter(pubtime__range=(
            date[x], date[x] + timedelta(days=1))).count(), xrange(days))
        weibo_data = map(lambda x: Weibo.objects.filter(pubtime__range=(
            date[x], date[x] + timedelta(days=1))).count(), xrange(days))
        total_data = map(lambda x: news_data[x] + weixin_data[x] + weibo_data[x] , xrange(days))

        date = map(lambda x: x.strftime("%m-%d"), date)

        return Response({
            "date": date,
            "news_data": news_data,
            "weixin_data": weixin_data,
            "weibo_data": weibo_data,
            "total_data": total_data
        })


# class AnalyticsParentsView(BaseTemplateView):
#     def get(self, request):
#         return self.render_to_response('analytics/analytics_all.html')


class AnalyticsChildView(BaseTemplateView):
    def get(self, request, id):
        return self.render_to_response('analytics/analytics.html', {'industry': {'name': u'综合'}})
