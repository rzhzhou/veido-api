# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from django.conf import settings

from base.views import BaseAPIView
from base.models import Topic
from base import authenticate, login_required, set_logo
from base.api_function import chart_line

class EventView(BaseAPIView):
    HOME_PAGE_LIMIT = 10
    def collected_items(self):
        user = self.request.myuser
        return user.collection.events.all()

    def get(self, request):
        container = self.requestContainer(limit=self.HOME_PAGE_LIMIT, 
            limit_list=settings.EVENT_PAGE_LIMIT)
        items = Topic.objects.all()
        datas = self.paging(items, container['limit'], container['page'])
        result = self.event_to_json(datas['items'])
        html_string = render_to_string('event/%s_tpl.html' % container['type'], {'event_list':  result})
        return Response({'total': datas['total_number'], 'html': html_string})


class EventTableView(BaseAPIView):
    def collected_items(self):
        user = self.request.myuser
        return user.collection.events.all()

    def get(self, request, page):
        items = Topic.objects.all()
        result = self.event_to_json(items)
        datas = self.paging(result, self.EVENT_PAGE_LIMIT, page)

        return Response({'total': datas['total_number'], 'data': list(datas["items"])})


class EventNewsView(BaseAPIView):

    def get(self, request, id):
        container = self.requestContainer()
        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/event/')
        items = event.articles.all()
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, container['page'])
        result = self.news_to_json(datas['items'])
        html_string = render_to_string('news/list_tpl.html', {'news_list':  result})
        return Response({'html': html_string, 'total': datas['total_number']})


class EventWeixinView(BaseAPIView):
    def get(self, request, id):
        container = self.requestContainer()
        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/weixin/')
        items = event.weixin.all()
        datas = self.paging(items, settings.EVENT_WEIXIN_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weixin/list_tpl.html', {'weixin_list':  items})
        return Response({'html': html_string, 'total': datas['total_number']})


class EventWeiboView(BaseAPIView):
    def get(self, request, id):
        container = self.requestContainer()
        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/weibo/')
        items = event.weibo.all()
        datas = self.paging(items, settings.EVENT_WEIBO_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weibo/list_tpl.html', {'weibo_list':  items})
        return Response({'html': html_string, 'total': datas['total_number']})


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
             {u'name': u'自媒体', u'value': topic.weibo.count()+topic.weixin.count()}]
    value = [item for item in value if item['value']]
    return JsonResponse({u'name': name, u'value': value})