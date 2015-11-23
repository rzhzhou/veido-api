# -*- coding: utf-8 -*-
import cPickle
import os
import pytz
from datetime import datetime, timedelta

from django.db import models, connection, IntegrityError
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from observer.apps.base import authenticate, login_required, set_logo
from observer.apps.base.models import save_user, hash_password, User, Area, Category
from django.conf import settings
from observer.apps.base import sidebarUtil
from observer.apps.base.views import BaseAPIView
from observer.apps.news.api import NewsApi
from observer.apps.event.api import EventApi
from observer.apps.weixin.api import WeixinApi
from observer.apps.weibo.api import WeiboApi
from observer.apps.base.models import (
    Area, Article, ArticlePublisher, Category, Collection, Custom, CustomKeyword,
    Group, Inspection, LocaltionScore, Product, ProductKeyword, RelatedData,
    Risk, RiskScore, Topic, Weibo, Weixin)
from observer.utils.connector.redisconnector import RedisQueryApi

def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)

    user = authenticate(username, password)
    if user.is_authenticated():
        response = JsonResponse({'status': True})
        response.set_cookie('pass_id', user.id)
        response.set_cookie('name', user.username)
        return response
    else:
        return JsonResponse({'status': False})


@api_view(['POST'])
def registe_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)
    users = User.objects.filter(username=username)
    if users:
        return JsonResponse({'status': False})
    try:
        area = Area.objects.get(name=u'武汉')
        save_user(username, password, area)
    except:
        return JsonResponse({'status': False})

    return JsonResponse({'status': True})


@login_required
def upload_image(request):
    user = request.myuser
    try:
        f = request.FILES['image']
    except KeyError:
        return HttpResponseRedirect('/settings/')

    media_path = settings.MEDIA_ROOT
    filename = str(user.id) + os.path.splitext(f.name)[1]
    file_list = os.listdir(media_path)
    name_list = map(lambda x: x.split('.')[0], file_list)

    count = 0
    for i in name_list:
        if i == str(user.id):
            os.remove(media_path + '/' + file_list[count])
        count += 1

    try:
        new_file = open(os.path.join(media_path, filename), 'w')
        for chunk in f.chunks():
            new_file.write(chunk)
    except OSError:
        return HttpResponseRedirect('/settings/')
    finally:
        new_file.close()

    return HttpResponseRedirect('/settings/')


@login_required
def change_passwd(request):
    user = request.myuser
    try:
        old_passwd = request.POST['oldPassword']
        new_passwd = request.POST['newPassword']
        username = request.POST['username']
    except KeyError:
        return HttpResponse(status=400)
    if username != user.username:
        return JsonResponse({'status': False})

    coded = hash_password(old_passwd, user.salt)
    # authencate success
    if user.password == coded:
        user.password = hash_password(new_passwd, user.salt)
        user.save(using='master')
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})


@login_required
def reset_passwd(request):
    try:
        reseted_user_ids = request.POST['id'].split(',')
        reseted_id_list = map(lambda x: int(x), reseted_user_ids)
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    admin_user = request.myuser
    group_users = admin_user.group.user_set.all()
    group_user_ids = list(map(lambda x: x.id, group_users))

    for user_id in reseted_id_list:
        if user_id in group_user_ids:
            user = User.objects.get(id=user_id)
            user.password = hash_password('123456', user.salt)
            user.save(using='master')
    return JsonResponse({'status': True})


@login_required
def delete_user_view(request):
    try:
        reseted_user_ids = request.POST['id'].split(',')
        reseted_id_list = map(lambda x: int(x), reseted_user_ids)
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    admin_user = request.myuser
    group_users = admin_user.group.user_set.all()
    group_user_ids = list(map(lambda x: x.id, group_users))

    for user_id in reseted_id_list:
        if user_id in group_user_ids and user_id != admin_user.id:
            delete_user = User.objects.get(id=user_id)
            delete_user.delete(using='master')
    return JsonResponse({'status': True})


@login_required
def add_user_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)

    myuser = request.myuser
    if not myuser.isAdmin:
        return HttpResponse(status=401)

    if User.objects.filter(username=username):
        return JsonResponse({'status': False})
    else:
        save_user(username, password, myuser.area, myuser.group)
        return JsonResponse({'status': True})


def get_count_feeling(start_d, end_d, feeling_type):
    feeling_limit = ''
    if feeling_type == 'positive':
        feeling_limit = 'feeling_factor >= 0.9'
    elif feeling_type == 'negative':
        feeling_limit = 'feeling_factor <= 0.1 and feeling_factor >= 0'
    else:
        feeling_limit = 'feeling_factor > 0.1  and feeling_factor < 0.9 or feeling_factor = -1'
    with connection.cursor() as c:
        sql_str = "SELECT Date(pubtime), COUNT(*) FROM article where Date(pubtime) >= '{0}' and Date(pubtime) < '{1}' and {2} group by Date(pubtime)".format(start_d, end_d, feeling_limit)
        c.execute(sql_str)
        rows = c.fetchall()

        d = dict(rows)
        a = [i[0] for i in rows]
        result = []
        day = start_d
        while day < end_d:
            num = d[day] if day in d else 0
            result.append(num)
            day = day + timedelta(days=1)
        return result


@login_required
def chart_line_index_view(request):
    today = timezone.now()
    today = today.astimezone(pytz.utc).date()
    start_d = today - timedelta(days=6)
    end_d = today + timedelta(days=1)

    data = {}
    data['date'] = [(today - timedelta(days=x)).strftime("%m-%d") for x in reversed(range(7))]
    data['positive'] = get_count_feeling(start_d, end_d, 'positive')
    data['neutral'] = get_count_feeling(start_d, end_d, 'netrual')
    data['negative'] = get_count_feeling(start_d, end_d, 'negative')

    return JsonResponse(data)


@login_required
def chart_pie_index_view(request):
    area = request.myuser.area
    locations = Area.objects.filter(parent=area)
    name = [item.name for item in locations]
    values = []
    for item in locations:
        values.append({'name': item.name, 'value': item.article_set.all().count()})
        # values.append({'name': item.name, 'value': 80})
    values = [item for item in values if item['value']]
    return JsonResponse({'name': name, "value": values})


def map_view(request):
    data = cPickle.load(file(os.path.join(settings.BASE_DIR, "yqj/jobs/minutely/map.json"), "r"))
    risk_data = data["regionData"]
    return JsonResponse({"regionData": risk_data})


class Dashboard(BaseAPIView):

    def get(self, request):
        news = Category.objects.get(name=u'质监热点').articles.all().count()
        event = Topic.objects.count()
        inspection = Inspection.objects.count()
        event_list = EventApi().get()
        news_list = NewsApi().get()
        weixin_list = WeixinApi().get()
        weibo_list = WeiboApi().get()
        return Response({
            "boxes": [{
              "id": 0,
              "name": u"质监热点",
              "number": news,
              "link": "news",
              "color": "aqua",
              "icon": "newspaper-o"
            },
            {
              "id": 1,
              "name": u"事件",
              "number": event,
              "link": "event",
              "color": "red",
              "icon": "exclamation"
            },
            {
              "id": 2,
              "name": u"行业监测",
              "number": "2890",
              "link": "industry",
              "color": "green",
              "icon": "industry"
            },
            {
              "id": 3,
              "name": u"抽检信息",
              "number": inspection,
              "link": "inspection",
              "color": "yellow",
              "icon": "cubes"
            }],
            "weixin": weixin_list,
            "weibo": weibo_list,
            "news": news_list, 
            'event': event_list
          })


class Sidebar(APIView):

  def get(self, request):
      sidebar = sidebarUtil(request)
      return Response({
          "user": {
          "name": sidebar["user"].username,
          "company": sidebar["site"].decode('utf-8'),
          "icon": "/dist/img/avatar.jpg"
          },
          "map": [
            {
              "id": "dashboard",
              "name": u"整体概览",
              "icon": "dashboard"
            },
            {
              "id": "website",
              "name": u"网站",
              "icon": "globe"
            },
            {
              "id": "keyword",
              "name": u"关键词",
              "icon": "comment-o"
            },
            {
              "id": "event",
              "name": sidebar["event"].decode('utf-8'),
              "icon": "warning"
            },
            {
              "id": "eventDetail",
              "name": u"事件详情",
              "icon": "warning"
            },
            {
              "id": "person",
              "name": u"人物",
              "icon": "user"
            },
            {
              "id": "news",
              "name": sidebar["news"].decode('utf-8'),
              "icon": "newspaper-o"
            },
            {
              "id": "newsDetail",
              "name": u"热点详情",
              "icon": "newspaper-o"
            },
            {
              "id": "industry",
              "name": u"行业监测",
              "icon": "industry"
            },
            {
              "id": "inspection",
              "name": u"抽检信息",
              "icon": "cubes"
            },
            {
              "id": "department",
              "name":u"业务信息",
              "icon": "tasks"
            },
            {
              "id": "collection",
              "name": u"我的收藏",
              "icon": "star"
            },
            {
              "id": "settings",
              "name": u"我的设置",
              "icon": "gear"
            },
            {
              "id": "user",
              "name": u"账户管理",
              "icon": "user"
            },
            {
              "id": "weixinDetail",
              "name": u"微信",
              "icon": ""
            }
          ]
        })


def logout_view(request):
  return JsonResponse({})
