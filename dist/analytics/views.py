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
        type = parameter['type']
        start = parameter['start']
        end = parameter['end']
        page = parameter['page'] if parameter.has_key('page') else 0
        func = getattr(globals()['DispatchView'](), type)
        return func(start, end, page)

    def statistic(self, start, end, page=0):
        return Response({})


class LineTableView():
    """
    {
        "date": ["07-30", "07-31", "08-01", "08-02", "08-03", "08-04", "08-05"],
        "news_data": [491, 363, 164, 116, 331, 381, 168],
    }
    """
    def get(self, request, id):
        start = datetime.strptime(request.GET['start'], "%Y-%m-%d")
        end = datetime.strptime(request.GET['end'], "%Y-%m-%d")
        date_range = end - start
        # print (start + timedelta(days=1)).strftime("%m-%d")
        date = [(start + timedelta(days=x)).date() for x in xrange(date_range.days)]
        print type(date[0])
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


class PieTypeTableView():
    def get(self, request):
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d')
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d')+timedelta(days=1)
        news = Article.objects.filter(pubtime__range=(start,end)).count()
        weixin = WeiXin.objects.filter(pubtime__range=(start,end)).count()
        weibo = Weibo.objects.filter(pubtime__range=(start,end)).count()

        return Response({'news': article, 'weixin': weixin, 'weibo': weibo})

class PieFeelingTableView():
    def get(self, request, id):
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d')
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d')+timedelta(days=1)
        positive = Article.objects.filter(pubtime__range=(start,end),
            feeling_factor__gte=0.6).count()

        normal = Article.objects.filter(pubtime__range=(start,end),
            feeling_factor__gte=0.5, feeling_factor__lt=0.6).count()

        negative = Article.objects.filter(pubtime__range=(start,end), feeling_factor__lt=0.5).count()

        return Response({'positive':positive, 'normal': normal, 'negative': negative})


class PieAreaTableView():
    def get(self, request, id):
    #SELECT id FROM yqj.`area` WHERE parent_id IN (SELECT id FROM yqj.`area` WHERE parent_id=2) OR parent_id=2 OR id =2
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d')
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d')+timedelta(days=1)
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
        sort_result = sorted(provice_count, key=lambda x:x['count'], reverse=True)[:6]

        return Response({'provice_count':provice_count, 'sort_result': sort_result})


class AnalyticsView(BaseView):
    def get(self, request):
        return self.render_to_response('analytics/analytics.html', {'industry': {'name': u'综合'}})

