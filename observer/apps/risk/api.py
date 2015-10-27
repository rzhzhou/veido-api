# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base import authenticate, login_required, set_logo
from observer.apps.base.api_function import chart_line
from observer.apps.base.models import Group, LocaltionScore, Risk, RiskScore
from observer.apps.base.views import BaseAPIView
from observer.apps.yqj.redisconnect import RedisQueryApi

class RisksView(BaseAPIView):
    HOME_PAGE_LIMIT = 10

    def get_score_article(self, request):
        user = request.myuser
        company = user.group.company
        group = Group.objects.get(company=company).id
        score_list = LocaltionScore.objects.filter(group=group)
        risk_id = []
        for item in score_list:
            risk_id.append(item.risk_id)

        risk_lists = Risk.objects.filter(id__in=risk_id)
        risk_list = []
        for item in risk_lists:
            data = {}
            try:
                relevance = LocaltionScore.objects.get(risk_id=item.id, group_id=group).score
            except:
                relevance = 0
            try:
                score = RiskScore.objects.get(risk=item.id).score
            except:
                score = 0
            data['relevance'] = relevance
            data['title'] = item.title
            data['source'] = item.source
            data['score'] = score
            data['pubtime'] = item.pubtime
            data['id'] = item.id
            risk_list.append(data)
        return risk_list

    def get(self, request):
        container = self.requesthead(
            page=1, limit=self.HOME_PAGE_LIMIT, limit_list=settings.RISK_PAGE_LIMIT)
        items = self.get_score_article(request)
        datas = self.paging(items, container['limit'], container['page'])
        return Response({'total': datas['total_number'], 'data': list(datas['items'])})


class RisksNewsView(BaseAPIView):

    def get(self, request, id):
        container = self.requesthead()
        try:
            risk = Risk.objects.get(id=int(id))
        except Risk.DoesNotExist:
            return HttpResponseRedirect('/risk/')

        items = risk.articles.all()
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, container['page'])
        result = self.news_to_json(datas['items'])
        return Response({'total': datas['total_number'], 'data': result})


class RisksWeixinView(BaseAPIView):
    def get(self, request, id):
        container = self.requesthead()
        try:
            risk = Risk.objects.get(id=int(id))
        except Risk.DoesNotExist:
            return HttpResponseRedirect('/risk/')

        items = risk.weixin.all()
        datas = self.paging(items, settings.RISK_WEIXIN_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        result = self.weixin_to_json(items)
        return Response({'total': datas['total_number'], 'data': result})


class RisksWeiboView(BaseAPIView):
    def get(self, request, id):
        container = self.requesthead()
        try:
            risk = Risk.objects.get(id=int(id))
        except Risk.DoesNotExist:
            return HttpResponseRedirect('/risk/')

        items = risk.weibo.all()
        datas = self.paging(items, settings.RISK_WEIBO_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        result = self.weibo_to_json(items)
        return Response({'total': datas['total_number'], 'data': result})


def chart_line_risk_view(request, risk_id):
    try:
        articles = Risk.objects.get(id=risk_id).articles.all()
    except Risk.DoesNotExist:
        return HttpResponse(status=400)
    if not articles:
        return HttpResponse(status=400)
    min_date = min(x.pubtime.date() for x in articles)
    max_date = max(x.pubtime.date() for x in articles)
    date_range = max_date - min_date
    return chart_line(date_range, min_date, max_date, articles)


def chart_pie_risk_view(request, risk_id):
    try:
        risk = Risk.objects.get(id=int(risk_id))
    except (KeyError, ValueError, Risk.DoesNotExist):
        return HttpResponse(status=400)
    name = [u'新闻媒体', u'政府网站', u'自媒体']
    value = [{u'name': u'新闻媒体', u'value': risk.articles.filter(publisher__searchmode=1).count()},
             {u'name': u'政府网站', u'value': risk.articles.filter(publisher__searchmode=0).count()},
             {u'name': u'自媒体', u'value': risk.weibo.count() + risk.weixin.count()}]
    value = [item for item in value if item['value']]
    return JsonResponse({u'name': name, u'value': value})
