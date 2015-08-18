# -*- coding: utf-8 -*-
import time
import pytz
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView

from base import sidebarUtil
from base.views import BaseTemplateView
from django.conf import settings
from base.models import Article, Area, Category, Inspection, Weixin, Weibo
from yqj.mysqlUtil import query
from yqj.redisconnect import RedisQueryApi


class DispatchView(APIView, BaseTemplateView):

    def get(self, request, id):
        parameter = request.GET
        try:
            type = parameter['type'].replace('-', '_')
            tz = pytz.timezone(settings.TIME_ZONE)
            start = tz.localize(datetime.strptime(parameter['start'], '%Y-%m-%d'))
            end = tz.localize(datetime.strptime(parameter['end'], '%Y-%m-%d') + timedelta(days=1))
            cache = int(parameter['cache']) if parameter.has_key('cache') else 1
            func = getattr(globals()['DispatchView'](), type)

            # cache is flag,if cache=1 read redis, else read mysql
            if cache:
                now = datetime.now()
                today = tz.localize(datetime(now.year, now.month, now.day) + timedelta(days=1))
                first_day_of_month = tz.localize(datetime(now.year, now.month, 1))
                date_range = (end - start).days

                data = None

                '''
                read over the past 7 days of data in redis
                read over the past 30 days of data in redis
                read this month of data in redis
                read last month of data in redis
                '''
                if end == today and date_range == 7:
                    data = RedisQueryApi().hget('CacheSevenDays', type)
                elif end == today and date_range == 30:
                    data = RedisQueryApi().hget('CacheThrityDays', type)
                elif end == today and start == first_day_of_month:
                    data = RedisQueryApi().hget('CacheThisMonth', type)
                elif end == first_day_of_month and start == first_day_of_month - relativedelta(months=1):
                    data = RedisQueryApi().hget('CacheLastMonth', type)

                if data:
                    return Response(eval(data))

            return func(start, end)

        except Exception, e:
            return Response({})


    def statistic(self, start, end):
        total = Article.objects.filter(pubtime__gte=start, pubtime__lt=end).count()
        event_count = Category.objects.get(name=u'事件').articles.filter(
            pubtime__gte=start, pubtime__lt=end).count()
        hot_count = Category.objects.get(name=u'质监热点').articles.filter(
            pubtime__gte=start, pubtime__lt=end).count()
        inspection_count = Inspection.objects.filter(
            pubtime__gte=start, pubtime__lt=end).count()

        risk = event_count + hot_count + inspection_count
        return Response({'total': total, 'risk': risk})

    def chart_type(self, start, end):
        article = Article.objects.filter(pubtime__gte=start, pubtime__lt=end).count()
        weixin = Weixin.objects.filter(pubtime__gte=start, pubtime__lt=end).count()
        weibo = Weibo.objects.filter(pubtime__gte=start, pubtime__lt=end).count()

        return Response({'news': article, 'weixin': weixin, 'weibo': weibo})

    def chart_emotion(self, start, end):
        positive = Article.objects.filter(pubtime__gte=start, pubtime__lt=end,
                feeling_factor__gte=0.9).count()
        normal = Article.objects.filter(pubtime__gte=start, pubtime__lt=end,
            feeling_factor__gte=0.1, feeling_factor__lt=0.9).count()
        negative = Article.objects.filter(
            pubtime__gte=start, pubtime__lt=end, feeling_factor__lt=0.1).count()

        return Response({'positive':positive, 'normal': normal, 'negative': negative})

    def chart_weibo(self, start, end):
        provice_count = []
        provinces = Area.objects.filter(level=2)
        for province in provinces:
            citys = Area.objects.filter(parent_id=province.id)
            city_id = map(lambda c: c.id, citys)
            areas_id = Area.objects.filter(Q(parent_id__in=city_id)|Q(parent_id=province.id)|Q(id=province.id))
            count = Weibo.objects.filter(area__in=areas_id, pubtime__gte=start, pubtime__lt=end).count()
            provice_count.append({'name': province.name, 'value': count})
        sort_result = sorted(provice_count, key=lambda x:x['value'])[-10:]
        name = map(lambda n: n['name'], sort_result)
        value = map(lambda v: v['value'], sort_result)
        return Response({'province': provice_count, 'name': name, 'value': value})

    def chart_trend(self, start, end):
        days = (end - start).days
        start = start.astimezone(pytz.utc)
        start = time.strftime( '%Y-%m-%d %X', start.timetuple())
        start = datetime.strptime(start, '%Y-%m-%d %X')
        date = [(start + timedelta(days=x)) for x in xrange(days)]

        date_range = [(i, i + timedelta(days = 1)) for i in date]
        query_str = map(
            lambda x: "sum(case when pubtime < '%s' and pubtime >= '%s' then 1 else 0 end)"
            % (x[1], x[0]),
            date_range
        )

        sum_result =lambda x: query('select %s from %s' % (','.join(query_str), x))
        news_data = [i for i in sum_result('article')[0]]
        weixin_data = [i for i in sum_result('weixin')[0]]
        weibo_data = [i for i in sum_result('weibo')[0]]

        total_data = map(lambda x: news_data[x] + weixin_data[x] + weibo_data[x] , xrange(days))

        date = map(lambda x: x.strftime("%m-%d"), date)

        return Response({
            "date": date,
            "news": news_data,
            "weixin": weixin_data,
            "weibo": weibo_data,
            "total": total_data
        })


# class AnalyticsParentsView(BaseTemplateView):
#     def get(self, request):
#         return self.render_to_response('analytics/analytics_all.html')


class AnalyticsChildView(BaseTemplateView):
    def get(self, request, id):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('analytics/analytics.html', {'industry': {'name': u'综合'}, 'name': sidebar_name})
