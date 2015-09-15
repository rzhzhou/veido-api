# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta, date

from django.conf import settings
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db import connection
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.utils import timezone

from base import login_required, get_user_image, set_logo, sidebarUtil
from base.views import BaseTemplateView
from base.models import (Area, Article, ArticlePublisher, Category, Collection,
    Custom, CustomKeyword, Group, Inspection, LocaltionScore, Product, ProductKeyword,
    RelatedData, Risk, RiskScore, Topic, Weibo, Weixin)
from yqj.redisconnect import RedisQueryApi


@login_required
def index_view(request):
    user = request.myuser
    if user.is_authenticated():
        business = sidebarUtil(request)['business']
        categories = Category.objects.filter(name__in=business)
        locations = Area.objects.filter(level=user.area.level+1, parent=user.area)
        user.company = user.group.company

        news = Article.objects.count()
        weibo = Weibo.objects.count()
        weixin = Weixin.objects.count()
        total = news + weixin + weibo
        event = Topic.objects.all().count()
        event_news = Category.objects.get(name=u'事件').articles.count()
        event_weixin = Weixin.objects.filter(website_type='topic').count()
        event_weibo = Weibo.objects.filter(website_type='topic').count()
        event_data = event_news + event_weixin + event_weibo
        news_percent = news * 100 / total
        event_percent = event_data * 100 / total
        weixin_percent = weixin * 100 / total
        weibo_percent = weibo * 100 / total

        news_list = event_list = 10
        weixin_list = weibo_list = 5
        news_list = Category.objects.get(name='质监热点').articles.all()[:10]

        for item in news_list:
            try:
                setattr(item, 'hot_index', RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count())
            except IndexError:
                setattr(item, 'hot_index', 0)

        event_list = Topic.objects.all()[:event_list]
        for iteml in event_list:
            try:
                setattr(iteml, 'time', iteml.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d'))
            except:
                setattr(iteml, 'time', datetime.now().strftime('%Y-%m-%d'))
        for item in event_list:
            setattr(item, 'hot_index', item.articles.all().count()+item.weixin.all().count()+item.weibo.all().count())

        weibo_data = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:5]]
        for data in weibo_data:
            data['pubtime'] = datetime.fromtimestamp(data['pubtime'])
            if not data['photo']:
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
            if len(data['content']) < 200:
                data['short'] = True

        weixin_data = Weixin.objects.all()[0:weixin_list]
        for data in weixin_data:
            data = set_logo(data)


        group = Group.objects.get(company=user.company).id
        score_list = LocaltionScore.objects.filter(group=group)
        risk_id = []
        for item in score_list:
            risk_id.append(item.risk_id)
        risk_lists = Risk.objects.filter(id__in=risk_id)[:6]
        risk_list = []
        for item in risk_lists:
            data = {}
            try:
                relevance = LocaltionScore.objects.get(risk_id=item.id, group_id=group).score
            except:
                relevance = 0
            try:
                score = RiskScore.objects.get(risk=item.id).score
            except :
                score = 0
            data['relevance'] = relevance
            data['title'] = item.title
            data['source'] = item.source
            data['score'] = score
            data['time'] =  item.pubtime
            data['id'] = item.id
            risk_list.append(data)

        sidebar_name = sidebarUtil(request)
        return render_to_response("dashboard/dashboard.html",
            {   'user': user,
                'categories': categories,
                'locations': locations,
                'industries': [{'id': 0, 'name': u'综合'}],
                'news': {'number': news, 'percent': news_percent},
                'weibo': {'number': weibo, 'percent': weibo_percent},
                'weixin': {'number': weixin, 'percent': weixin_percent},
                'event': {'number': event, 'percent': event_percent},
                'news_list': news_list,
                'event_list': event_list,
                'risk_list': risk_list,
                'weixin_hottest_list': weixin_data,
                'weibo_hottest_list': weibo_data,
                'user_image': get_user_image(user),
                'name': sidebar_name,
            })
    else:
        return HttpResponse(status=401)


def person_view(request, person_id):
    return HttpResponse('person')


class CollectionView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('user/collection.html', {'name': sidebar_name})


class SettingsView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('user/settings.html', {'name': sidebar_name})


class UserView(BaseTemplateView):
    def get(self, request):
        return self.render_to_response('user/user.html')


class UserAdminView(BaseTemplateView):

    def get(self, request):
        sidebar_name = sidebarUtil(request)
        user = request.myuser
        if not user.isAdmin:
            return HttpResponse(status=401)

        user_list = user.group.user_set.all()
        user_list = filter(lambda x: x.id != request.myuser.id, user_list)
        for user in user_list:
            if user.id == request.myuser.id:
                continue
            user.name = user.username
            user.type = u'管理用户' if user.isAdmin else u'普通用户'
        return self.render_to_response('user/user.html', {'user_list': user_list, 'name': sidebar_name})


def register_view(request):
    return render_to_response('user/register.html')


def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = reqeust.POST['password']
        except KeyError:
            return HttpResponse(status=400)

        user = authenticate(username, password)
        if user.is_authenticated():
            response = HttpResponseRedirect('/')
            response.set_cookie('pass_id', user.id)
            response.set_cookie('name', user.name)
            return response

    return render_to_response('user/login.html', {'company': settings.COMPANY_NAME})


def logout_view(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('pass_id')
    response.delete_cookie('name')
    return response
