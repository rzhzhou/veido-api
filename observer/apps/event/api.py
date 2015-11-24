# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from observer.apps.base import authenticate, login_required, set_logo
from observer.apps.base.views import BaseAPIView, BaseView
from observer.apps.base.models import Topic
from observer.apps.base.api_function import chart_line


class EventDetailsView(BaseAPIView):
    HOME_PAGE_LIMIT = 10

    def collected_items(self, id):
        # user = self.request.myuser
        # collection = user.collection.events.filter(id=id)
        # flag = True if collection else False
        collected = True
        return collected

    def abstract(self, event):
        abstract = {}
        abstract['title'] = event.title
        abstract['content'] = event.abstract
        return abstract

    def keywords(self, event):
        eval_keywords_list = eval(event.keywords) if event.keywords else []
        keywords_list = [{"name": name, "number": "%.2f"%number}
         for name, number in eval_keywords_list]
        return keywords_list

    def event_news(self, event, container):
        items = event.articles.all()
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, container['page'])
        result = self.news_to_json(datas['items'])
        return {'items': result, 'pages': datas['total_number']}

    def event_weixin(self, event, container):
        items = event.weixin.all()
        datas = self.paging(items, settings.EVENT_WEIXIN_LIMIT, container['page'])
        result = self.weixin_to_json(datas['items'])
        return {
            'items': result, 
            'name': u'微信',
            'type': 'weixin', 
            'color': 'success',
            'link': '/weixin'
            }
    def event_weibo(self, event, container):
        items = event.weibo.all()
        datas = self.paging(items, settings.EVENT_WEIBO_LIMIT, container['page'])
        result = self.weibo_to_json(datas['items'])
        return {
            'items': result,
            'type': 'weibo',
            'name': u'微博',
            'color': 'warning',
            'link': '/weibo',
            }

    def get(self, request, id):
        collected = self.collected_items(id)
        container = self.requesthead(
            limit=self.HOME_PAGE_LIMIT, limit_list=settings.EVENT_PAGE_LIMIT)
        try:
            event = Topic.objects.get(id=id)
            abstract = self.abstract(event)
            keywords = self.keywords(event)
            news = self.event_news(event, container)
            weixins = self.event_weixin(event, container)
            weibos = self.event_weibo(event, container)
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/event/')
        return Response({
            'abstract': abstract, 
            'collected':collected,
            'keywords': keywords,
            'news': news,
            'weixin': weixins,
            'weibo': weibos,
            })


class EventApi(BaseView):

    def get(self):
        items = Topic.objects.all()[:10]
        result = self.event_to_json(items)
        event_data = self.get_info(title=u'质监事件', color='danger', types='event', name='eventDetail', items=result)
        return event_data


class EventTableView(BaseAPIView):
    def get(self, request):
        container = self.requesthead(
            limit_list=settings.EVENT_PAGE_LIMIT)
        items = Topic.objects.all()
        result = self.event_to_json(items)
        datas = self.paging(result, settings.EVENT_PAGE_LIMIT, container['page'])
        return Response({'list':{'pages': datas['total_number'], 
            'items': list(datas["items"])}})


@login_required
def chart_line_event_view(request, topic_id):
    try:
        articles = Topic.objects.get(id=topic_id).articles.all()
    except Topic.DoesNotExist:
        return HttpResponse(status=404)
    if not articles:
        return HttpResponse(status=404)
    min_date = min(x.pubtime.date() for x in articles)
    max_date = max(x.pubtime.date() for x in articles)
    date_range = max_date - min_date
    return chart_line(date_range, min_date, max_date, articles)


@api_view(['GET'])
@login_required
def chart_pie_event_view(request, topic_id):
    try:
        topic = Topic.objects.get(id=int(topic_id))
    except (KeyError, ValueError, Topic.DoesNotExist):
        return HttpResponse(status=400)

    name = [u'新闻媒体', u'政府网站', u'自媒体']
    value = [{u'name': u'新闻媒体', u'value': topic.articles.filter(publisher__searchmode=1).count()},
             {u'name': u'政府网站', u'value': topic.articles.filter(publisher__searchmode=0).count()},
             {u'name': u'自媒体', u'value': topic.weibo.count() + topic.weixin.count()}]
    value = [item for item in value if item['value']]
    return JsonResponse({u'name': name, u'value': value})
