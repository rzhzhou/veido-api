# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.views import APIView

from base.views import BaseView
from yqj.models import Article, Area, Weixin, Weibo


class DispatchView(APIView, BaseView):

    def get(self, request, id):
        parameter = request.GET
        try:
            type = parameter['type'].replace('-', '_')
            start = parameter['start']
            end = parameter['end']
            page = parameter['page'] if parameter.has_key('page') else 0

            func = getattr(globals()['DispatchView'](), type)
            if page:
                return func(start, end, page)
            else:
                return func(start, end)
        except Exception, e:
            print e
            return Response({})


    def statistic(self, start, end):
        total = Article.objects.filter(pubtime__range=(start, end)).count()
        risk = total
        return Response({'total': total, 'risk': risk})

    def data_list(self, start, end, page):
        items = Article.objects.filter(pubtime__range=(start, end)).order_by('-pubtime')
        datas = self.paging(items, self.NEWS_PAGE_LIMIT, page)
        result = self.news_to_json(datas['items'])
        news = render_to_string('analytics/data_list_tmpl.html', {'data_list': result})
        return HttpResponse(news)


    def chart_type(self, start, end):
        article = Article.objects.filter(pubtime__range=(start,end)).count()
        weixin = Weixin.objects.filter(pubtime__range=(start,end)).count()
        weibo = Weibo.objects.filter(pubtime__range=(start,end)).count()
        return Response({'news': article, 'weixin': weixin, 'weibo': weibo})
       

    def chart_emotion(self, start, end):
        
        positive = Article.objects.filter(pubtime__range=(start,end),
                feeling_factor__gte=0.6).count()
        normal = Article.objects.filter(pubtime__range=(start,end),
            feeling_factor__gte=0.5, feeling_factor__lt=0.6).count()

        negative = Article.objects.filter(pubtime__range=(start,end), feeling_factor__lt=0.5).count()

        return Response({'positive':positive, 'normal': normal, 'negative': negative})
    
    def chart_weibo(self, start, end):
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
        sort_percent = []
        for result in sort_result:
            percent =  result['value']*100/sort_result[0]['value'] if result['value'] else 0
            sort_percent.append({'percent': percent})
        index = 0
        for items in sort_result:
            items.update(sort_percent[index])
            index+=1
        return Response({'provice_count':provice_count, 'sort_result': sort_result})

    def chart_trend(self, start, end):
        start = parse_date(start)
        end = parse_date(end)
        days = (end - start).days
        date = [(start + timedelta(days=x)) for x in xrange(days)]
        news_data = [Article.objects.filter(pubtime__range=(str(date[x]), str(date[x] + timedelta(days=1)))).count() for x in xrange(days)]
        weixin_data = [Weixin.objects.filter(pubtime__range=(str(date[x]), str(date[x] + timedelta(days=1)))).count() for x in xrange(days)]
        weibo_data = [Weibo.objects.filter(pubtime__range=(str(date[x]), str(date[x] + timedelta(days=1)))).count() for x in xrange(days)]
        total_data = [news_data[i] + weixin_data[i] + weibo_data[i] for i in xrange(days)]

        date = map(lambda x: x.strftime("%m-%d"), date)

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
