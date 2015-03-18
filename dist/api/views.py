#coding=utf-8

import datetime
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from yqj.models import (Article, Area, Weixin, Weibo, Topic, RelatedData, ArticleCategory, save_user)
from serializers import ArticleSerializer
#from django.db.model import get_model


def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)
    
    user = authenticate(username, password)
    response = JsonResponse()
    if user.is_authenticated():
        response.set_cookie('pass_id', user.id)
        response.set_cookie('name', user.username)
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})


def regist_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)
    try:
        area = Area.objects.get(name=u'武汉')
        save_user(username, password, area)
    except excep:
        raise excep
        return JsonResponse({'status': False})

    return JsonResponse({'status': True})

    

class TableAPIView(APIView):
    COLLECTED_TEXT = u'<i class="fa fa-star" data-toggle="tooltip", data-placement="right" title="取消收藏">'
    NO_COLLECTED_TEXT = u'<i class="fa fa-star-o" data-toggle="tooltip", data-placement="right" title="添加收藏">'

    LIMIT_NUMBER = 300

    def collected_html(self, item):
        items = self.collected_items()
        return self.COLLECTED_TEXT if self.isIn(item, items) else self.NO_COLLECTED_TEXT

    def isIn(self, item, items):
        if isinstance(item, models.Model):
            item_id = item.id
        else:
            item_id = item['id']

        if item_id is None:
            raise TypeError('item should has id atrribute or id key')
        
        return any(filter(lambda x: x.id == item_id, items))

    def collected_items(self):
        return []
        #user = self.request.myuser
        #return user.collections.article_collections.articles

    def title_html(self, *args):
        title_format = u'<a href="{0}" title="{1}" target="_blank" data-id="{2}" data-type="{3}">{1}</a>'
        return title_format.format(*args)

    
def get_date_from_iso(datetime_str):
    #return datetime.datetime.strptime("2008-09-03T20:56:35.450686Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        
class ArticleTableView(TableAPIView):
    def get(self, request, id):
        try:
            category = ArticleCategory.objects.get(id=id)
        except ArticleCategory.DoesNotExist:
            return Response({'news': []})
        
        result = []
        articles = category.articles.all()[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(articles, many=True)

        for item in articles:
            collect_html = self.collected_html(item)
            #pubtime = get_date_from_iso(item.pubtime)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = 78
            one_record = [collect_html, title, item.source, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)

        return Response({'news': result})

class NewsTableView(TableAPIView):
    def get(self, request):
        result = []
        news = Article.objects.all()[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(news, many=True)

        for item in news:
            collected_html = self.collected_html(item)
            #pubtime = get_date_from_iso(item['item'])
            area = u'武汉'
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = 78
            one_record = [collect_html, title, item.source, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)
        
        return Response({"news": result})


class LocationTableView(TableAPIView):
    def get(self, request, location_id):
        try:
            id = int(location_id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'news': []})
        result = []
        news = Article.objects.filter(area=area)[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(news, many=True)

        for item in news:
            collected_html = self.collected_html(item)
            #pubtime = get_date_from_iso(item.item)
            area = u'武汉'
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = 78
            one_record = [collected_html, title, item.source, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)
        
        return Response({"news": result})


class CollectModifyView(View):
    pass

