from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.db import models
from yqj.models import (Article, Area, Weixin, Topic, RealtedData)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
#from api.serializers import ArticleSerializer,NotificationSerializer,InsightSerializer,EventSerializer,NewsSerializer,InspectionSerializer
from general.decorators import login_required
from django.db.models import Q
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models import get_model
from rest_framework.views import APIView
from django.db.models import Count
import datetime

# Create your views here.

@api_view(['GET'])
def article_view(request, id, **kwargs):
    try:
        article_id = int(id)
        article = Article.objects.get(id=article_id)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ArticleSerializer(article)
    return Response(serializer.data)

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
        
        return any(lambda x: x.id == item_id, items)

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
            return {'data': []}
        
        result = []
        articles = category.articles.all()[self.LIMIT_NUMBER]
        serializer = ArticleSerializer(articles, many=True)

        for item in articles:
            collect_html = self.collected_html(item)
            pubtime = get_date_from_iso(article['pubtime'])
            area = u'武汉'
            title = self.title_html(article['url'], article['title'], article['id'], 'article')
            hot_index = 78
            one_record = [collect_html, title, source, area, pubtime, hot_index]
            result.append(one_record)

        return Response({'data': result})
