# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
import ConfigParser

from django.conf import settings
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db import connection
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.utils import timezone

from base import login_required, get_user_image, set_logo
from base.views import BaseTemplateView
from base.models import (Area, Article, ArticlePublisher, Category, Collection,
    Custom, CustomKeyword, Group, Inspection, LocaltionScore, Product, ProductKeyword,
    RelatedData, Risk, RiskScore, Topic, Weibo, Weixin)
from yqj.redisconnect import RedisQueryApi


def sidebarUtil(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    user = request.myuser
    conf = ConfigParser.ConfigParser()
    conf.read(os.path.join(BASE_DIR, "../sidebar.cfg"))
    username = user.username

    sidebar_name = {
        "news": conf.get(username, "news"),
        "event": conf.get(username, "event"),
        "location": conf.get(username, "location"),
        "custom": conf.get(username, "custom"),
        "site": conf.get(username, "site")
    }
    return sidebar_name


@login_required
def index_view(request):
    user = request.myuser
    if user.is_authenticated():
        categories = Category.objects.filter(~(Q(name='其他' )|Q(name='政府' )|Q(name='事件' )|Q(name='质监热点' )
            |Q(name='指定监测' )))
        locations = Area.objects.filter(level=user.area.level+1, parent=user.area)
        user.company = user.group.company

        news_number = Article.objects.count()
        weibo_number = Weibo.objects.count()
        weixin_number = Weixin.objects.count()
        total = news_number + weixin_number + weibo_number
        event = Topic.objects.all().count()
        event_news_number = Category.objects.get(name=u'事件').articles.count()
        event_weixin_number = Weixin.objects.filter(website_type='topic').count()
        event_weibo_number = Weibo.objects.filter(website_type='topic').count()
        event_data_number = event_news_number + event_weixin_number + event_weibo_number
        news_percent = news_number*100/total if news_number else 0
        event_percent = event_data_number*100/total if event_data_number else 0
        weixin_percent = weixin_number*100/total if weixin_number else 0
        weibo_percent = weibo_number*100/total if weibo_number else 0

        news_list_number = event_list_number = 10
        weixin_list_number = weibo_list_number = 5

        start_date = datetime.now() + timedelta(days=-7)
        # news_lists = Article.objects.filter(website_type='hot', pubtime__gt=start_date).order_by('-pubtime')[:news_list_number]
        # news_lists = Category.objects.get(name='质监热点').articles.filter(pubtime__gt=start_date).order_by('-pubtime')[:news_list_number]
        custom_id_list=[]
        keywords = CustomKeyword.objects.filter(group_id=4)
        #group_id = 4
        for keyword in keywords:
            custom_id = keyword.custom_id
            if custom_id:
                custom_id_list.append(custom_id)

        # custom_set = Custom.objects.filter(id__in=custom_id_list)
        # article_set = [i.articles.all() for i in custom_set]
        # article_set_list = reduce(lambda x, y: list(set(x).union(set(y))), article_set)
        # article_id = [article_set_list[i].id for i in range(len(article_set_list))]
        try:
            cursor = connection.cursor()
            sql = 'select article_id from custom_articles where %s'\
                %(
                    reduce(
                        lambda x, y: x + " or " + y,
                        ["custom_id=%s" for x in custom_id_list]
                        )
                    )
            cursor.execute(sql,custom_id_list)
            row = cursor.fetchall()
            article_id = []
            for r in row:
                article_id.append(r[0])
        except:
            article_id = []

        hot_list = Category.objects.get(name='质监热点').articles.all()
        for n in hot_list:
            article_id.append(n.id)

        news_list = Article.objects.filter(id__in=article_id)[:10]

        for item in news_list:
            try:
                setattr(item, 'hot_index', RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count())
            except IndexError:
                setattr(item, 'hot_index', 0)

        event_list = Topic.objects.all()
        for iteml in event_list:
            try:
                setattr(iteml, 'time', iteml.articles.order_by('pubtime')[0].pubtime.replace(tzinfo=None).strftime('%Y-%m-%d'))
            except IndexError:
                setattr(iteml, 'time', datetime.now().strftime('%Y-%m-%d'))
        event_list=sorted(event_list, key=lambda x: x.time, reverse=True)[:event_list_number]
        for item in event_list:
            setattr(item, 'hot_index', item.articles.all().count()+item.weixin.all().count()+item.weibo.all().count())

        weibo_data = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:5]]
        for data in weibo_data:
            data['pubtime'] = datetime.fromtimestamp(data['pubtime'])
            if not data['photo']:
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
            if len(data['content']) < 200:
                data['short'] = True

        weixin_data = Weixin.objects.all()[0:weixin_list_number]
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
                relevance = LocaltionScore.objects.get(risk_id=item.id).score
            except LocaltionScore.DoesNotExist:
                relevance = 0
            try:
                score = RiskScore.objects.get(risk=item.id).score
            except RiskScore.DoesNotExist:
                score = 0
            data['relevance'] = relevance
            data['title'] = item.title
            data['source'] = item.source
            data['score'] = score
            data['time'] =  datetime.now()
            data['id'] = item.id
            risk_list.append(data)

        sidebar_name = sidebarUtil(request)
        return render_to_response("dashboard/dashboard.html",
            {'user': user,
            'categories': categories,
            'locations': locations,
            'industries': [{'id': 0, 'name': u'综合'}],
            'news': {'number': news_number, 'percent': news_percent},
            'weibo': {'number': weibo_number, 'percent': weibo_percent},
            'weixin': {'number': weixin_number, 'percent': weixin_percent},
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


class RisksView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('risk/risk_list.html', {"name": sidebar_name})

class RisksDetailView(BaseTemplateView):
    def get(self, request, risk_id):
        sidebar_name = sidebarUtil(request)
        try:
            risk_id = int(risk_id)
            risk = Risk.objects.get(id=risk_id)
            eval_keywords_list = eval(risk.keywords) if risk.keywords else []
            keywords_list = [{"name": name, "number": number} for name, number in eval_keywords_list]
        except Risk.DoesNotExist:
            return self.render_to_response('risk/risk.html', {'risk': '', 'weixin_list': [], 'weibo_list': [], 'name': sidebar_name})
        # user = self.request.myuser
        # try:
        #     collection = user.collection
        # except Collection.DoesNotExist:
        #     collection = Collection(user=user)
        #     collection.save(using='master')
        # items = user.collection.Risks.all()
        # iscollected = any(filter(lambda x: x.id == risk_article.id, items))
        return self.render_to_response('risk/risk.html',{'risk': risk, 'keywords_list': keywords_list, 'name': sidebar_name})


class CollectionView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('user/collection.html',{'name': sidebar_name})


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
