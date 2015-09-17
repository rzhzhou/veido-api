# -*- coding: utf-8 -*-
import os
import requests
import json
import cPickle
import pytz
import time
from datetime import datetime, timedelta
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from serializers import ArticleSerializer

from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db import models, connection, IntegrityError
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from base import authenticate, login_required, set_logo
from base.views import BaseAPIView
from base.models import (Area, Article, Category, Collection, Custom,
    CustomKeyword, Group, Inspection, LocaltionScore, Product, ProductKeyword,
    RelatedData, Risk, RiskScore, Topic, User, Weibo, Weixin, save_user, hash_password)
from yqj.redisconnect import RedisQueryApi
from api.api_function import (GetFirstDaySeason, get_season, year_range,
    season_range, months_range, days_range, week_range, unstable)
from yuqing.settings import BASE_DIR


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
    except :
        return JsonResponse({'status': False})

    return JsonResponse ({'status': True})


def get_date_from_iso(datetime_str):
    #return datetime.strptime("2008-09-03T20:56:35.450686Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")


class ArticleTableView(BaseAPIView):
    def get(self, request, id, page):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'total': 0, 'data': []})
        """
            return Response({'news': []})
        result = []
        articles = category.articles.all()[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(articles, many=True)

        for item in articles:
            collected_html = self.collected_html(item)
            #pubtime = get_date_from_iso(item.pubtime)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            try:
                hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            except IndexError:
                hot_index = 0
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)

        return Response({'news': result})
        """
        items = category.articles.all()
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, page)
        result = self.news_to_json(datas['items'])
        return Response({'total': datas['total_number'], 'data': result})


class RisksView(BaseAPIView):
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
        parameter = request.GET

        api_type = parameter['type']
        page = parameter['page'] if parameter.has_key('page') else 1
        limit = self.RISK_PAGE_LIMIT if api_type == 'list' else 6
        items = self.get_score_article(request)
        datas = self.paging(items, limit, page)
        html_string = render_to_string('risk/%s_tpl.html' % api_type, {'risk_list':  datas['items']})
        return Response({'total': datas['total_number'], 'html': html_string})


class RisksNewsView(BaseAPIView):

    def get(self, request, id):
        parameter = request.GET
        page = parameter['page'] if parameter.has_key('page') else 1

        try:
            risk = Risk.objects.get(id=int(id))
        except Risk.DoesNotExist:
            return HttpResponseRedirect('/risk/')

        items = risk.articles.all()
        datas = self.paging(items, self.NEWS_PAGE_LIMIT, page)
        result = self.news_to_json(datas['items'])
        html_string = render_to_string('news/list_tpl.html', {'news_list':  result})
        return Response({'total': datas['total_number'], 'html': html_string})


class RisksWeixinView(BaseAPIView):
    EVENT_WEIXIN_LIMIT = 10

    def get(self, request, id):
        parameter = request.GET
        page = parameter['page'] if parameter.has_key('page') else 1

        try:
            risk = Risk.objects.get(id=int(id))
        except Risk.DoesNotExist:
            return HttpResponseRedirect('/risk/')

        items = risk.weixin.all()
        datas = self.paging(items, self.EVENT_WEIXIN_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weixin/list_tpl.html', {'weixin_list':  datas['items']})
        return Response({'total': datas['total_number'], 'html': html_string})


class RisksWeiboView(BaseAPIView):
    EVENT_WEIBO_LIMIT = 10

    def get(self, request, id):
        parameter = request.GET
        page = parameter['page'] if parameter.has_key('page') else 1

        try:
            risk = Risk.objects.get(id=int(id))
        except Risk.DoesNotExist:
            return HttpResponseRedirect('/risk/')

        items = risk.weibo.all()
        datas = self.paging(items, self.EVENT_WEIBO_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weibo/list_tpl.html', {'weibo_list':  datas['items']})
        return Response({'total': datas['total_number'], 'html': html_string})


class NewsView(BaseAPIView):
    def get_custom_artice(self):
        articles = Category.objects.get(name='质监热点').articles.all()
        return articles

    def get(self, request):
        parameter = request.GET

        api_type = parameter['type']
        page = parameter['page'] if parameter.has_key('page') else 1
        limit = settings.NEWS_PAGE_LIMIT if api_type == 'list' else 10
        items = self.get_custom_artice()
        datas = self.paging(items, limit, page)
        result = self.news_to_json(datas['items'])
        html_string = render_to_string('news/%s_tpl.html' % api_type, {'news_list':  result})
        return Response({'total': datas['total_number'], 'html': html_string})


class LocationTableView(BaseAPIView):
    def get(self, request, location_id, page):
        try:
            id = int(location_id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'total': 0, 'data': []})
        """
            return Response({'news': []})
        result = []
        news = Article.objects.filter(area=area)[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(news, many=True)

        for item in news:
            collected_html = self.collected_html(item)
            #pubtime = get_date_from_iso(item.item)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)

        return Response({"news": result})
        """
        items = Article.objects.filter(area=area)
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, page)
        result = self.news_to_json(datas['items'])
        return Response({'total': datas['total_number'], 'data': result})


class LocationWeixinView(BaseAPIView):
    LOCATION_WEIXIN_LIMIT = 10
    def get(self, request, location_id, page):
        try:
            id = int(location_id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'html': '', 'total': 0})
        items = Weixin.objects.filter(area=area)
        datas = self.paging(items, self.LOCATION_WEIXIN_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html = self.set_css_to_weixin(items)
        return Response({'html': html, 'total': datas['total_number']})


class LocationWeiboView(BaseAPIView):
    LOCATION_WEIBO_LIMIT = 10
    def get(self, request, location_id, page):
        try:
            id = int(location_id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'html': '', 'total': 0})
        items = Weibo.objects.filter(area=area)
        datas = self.paging(items, self.LOCATION_WEIBO_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html = self.set_css_to_weibo(items)
        return Response({'html': html, 'total': datas['total_number']})


class EventView(BaseAPIView):
    def collected_items(self):
        user = self.request.myuser
        return user.collection.events.all()

    def get(self, request):
        parameter = request.GET

        api_type = parameter['type']
        page = parameter['page'] if parameter.has_key('page') else 1
        limit = self.EVENT_PAGE_LIMIT if api_type == 'list' else 10
        items = Topic.objects.all()
        datas = self.paging(items, limit, page)
        result = self.event_to_json(datas['items'])
        html_string = render_to_string('event/%s_tpl.html' % api_type, {'event_list':  result})
        return Response({'total': datas['total_number'], 'html': html_string})


class EventNewsView(BaseAPIView):

    def get(self, request, id):
        parameter = request.GET
        page = parameter['page'] if parameter.has_key('page') else 1

        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/event/')
        items = event.articles.all()
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, page)
        result = self.news_to_json(datas['items'])
        html_string = render_to_string('news/list_tpl.html', {'news_list':  result})
        return Response({'html': html_string, 'total': datas['total_number']})


class EventWeixinView(BaseAPIView):
    EVENT_WEIXIN_LIMIT = 10

    def get(self, request, id):
        parameter = request.GET
        page = parameter['page'] if parameter.has_key('page') else 1

        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/weixin/')
        items = event.weixin.all()
        datas = self.paging(items, self.EVENT_WEIXIN_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weixin/list_tpl.html', {'weixin_list':  items})
        return Response({'html': html_string, 'total': datas['total_number']})


class EventWeiboView(BaseAPIView):
    EVENT_WEIBO_LIMIT = 10

    def get(self, request, id):
        parameter = request.GET
        page = parameter['page'] if parameter.has_key('page') else 1

        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/weibo/')
        items = event.weibo.all()
        datas = self.paging(items, self.EVENT_WEIBO_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weibo/list_tpl.html', {'weibo_list':  items})
        return Response({'html': html_string, 'total': datas['total_number']})


class CollectView(APIView):
    def article_html(self, item):
        url = u'/news/%s' % item.id
        view = ArticleTableView(self.request)
        title = view.title_html(url, item.title, item.id, 'article')
        try:
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
        except:
            hot_index =0
        line = [title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
        #line = [view.collected_html(item), title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
        return line

    def topic_html(self, item):
        url = u'/event/%s' % item.id
        view = EventTableView(self.request)
        title = view.title_html(url, item.title, item.id, 'topic')
        hot_index = item.articles.all().count() + item.weixin.all().count() + item.weibo.all().count()
        time = item.articles.all().order_by('-pubtime')
        if time:
            pubtime = time[0].pubtime
        else:
            pubtime = timezone.now()
        one_record = [title, item.source, item.area.name, pubtime.date(), hot_index]
        #one_record = [view.collected_html(item), title, item.source, item.area.name, pubtime.date(), hot_index]
        return one_record

    def get(self, request, table_type, page):
        try:
            self.collection = request.myuser.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save(using='master')
        """
        news = [self.article_html(item) for item in self.collection.articles.all()]
        topic = [self.topic_html(item) for item in self.collection.events.all()]

        return Response({'news': news, 'event': topic})
        """
        if table_type == 'news':
            view = ArticleTableView(self.request)
            items = self.collection.articles.all()
            datas = view.paging(items, settings.NEWS_PAGE_LIMIT, page)
            result = view.news_to_json(datas['items'])
        elif table_type == 'event':
            view = EventTableView(self.request)
            items = self.collection.events.all()
            datas = view.paging(items, view.EVENT_PAGE_LIMIT, page)
            result = view.event_to_json(datas['items'])
        else:
            result = []
            datas = {'taotal_number': 0}
        return Response({'total': datas['total_number'], 'data': result})



class CollecModifyView(View):
    def save(self, item):
        data = {self.related_field: item, 'collection': self.collection}
        if isinstance(item, Article):
            try:
                category = item.categorys.all()[0]
            except IndexError:
                category = Category.objects.get(name='其他')
            data['category'] =  category.name
        try:
            collection_item = self.get_related_model().objects.create(**data)
            collection_item.save(using='master')
        except IntegrityError:
             pass


    def delete(self, item):
        try:
            collectitem = self.get_collection_model().objects.get(**{self.related_field: item, 'collection': self.collection})
            collectitem.delete(using='master')
        except self.get_collection_model.DoesNotExist:
            pass

    @property
    def related_field(self):
        return self.data_type.lower()

    def get_related_model(self):
        return models.get_model('base', self.data_type.capitalize() + 'Collection')

    def _create_collection(self):
        #add a collection to the user
        try:
            _collection = self.request.myuser.collection
        except ObjectDoesNotExist:
            _collection = Collection(user=user)
            _collection.save(using='master')
        return _collection

    @property
    def collection(self):
        return self._create_collection()

    def get_model(self):
        return models.get_model('base', self.data_type.capitalize())

    def get_collection_model(self):
        return models.get_model('base', self.data_type.capitalize() + 'Collection')

    def post(self, request, action, *args, **kwargs):
        try:
            self.data_type = request.POST['type']
            pk = request.POST['id']
        except KeyError:
            return HttpResponse(status=404)

        related_fields = ['article', 'topic']
        if self.data_type not in related_fields:
            return HttpResponse(status=400)

        #find the model and get instance
        try:
            model = self.get_model()
            item = model.objects.get(id=pk)
        except model.DoesNotExist:
            return HttpResponse(status=404)

        if action == 'remove':
            self.delete(item)
        elif action == 'add':
            self.save(item)
        return JsonResponse({'status': True})

class SearchView(CollectView):
    LIMIT = 200
    def get(self, request, keyword, *args, **kwargs):
        try:
            self.collection = request.myuser.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save(using='master')
        news = []
        for data in self.search_article(keyword):
            news.append(self.article_html(data))
        event = []
        for data in self.search_event(keyword):
            event.append(self.topic_html(data))
        return JsonResponse({"news": news, "event": event})

    def search_article(self, key):
        return Article.objects.raw(u"SELECT * FROM article WHERE MATCH (content, title) AGAINST ('%s') LIMIT %s" % (key, self.LIMIT))

    def search_event(self, key):
        #return Topic.objects.raw(u"SELECT * FROM topic WHERE MATCH (abstract, title) AGAINST ('%s') LIMIT %s" % (key, self.LIMIT))
        return Topic.objects.raw(u"SELECT * FROM topic WHERE title like '%%{0}%%' LIMIT {1}".format(key, self.LIMIT))


class CustomTableView(BaseAPIView):
    def get_bak(self, request, custom_id):
        customname = [u'电梯',u'锅炉', u'两会']
        try:
            #custom = Custom.objects.get(id=int(custom_id))
            custom = customname[int(custom_id)]
        except Custom.DoesNotExist:
            return Response({'news': ''})
        result = []
        #news = custom.articles.all()[:self.LIMIT_NUMBER]
        news = self.get_news(custom)
        serializer = ArticleSerializer(news, many=True)

        for item in news:
            collected_html = self.collected_html(item)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            try:
                hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            except IndexError:
                hot_index = 0
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)

        return Response({"news": result})

    def get_news(self, keyword):
        return Article.objects.raw(u"SELECT * FROM article WHERE MATCH (content, title) AGAINST ('%s')" % (keyword))

    def get(self, request, custom_id, page):
        user = request.myuser
        try:
            keyword = CustomKeyword.objects.get(id=int(custom_id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return Response({'total': 0, 'data': []})
        items = keyword.custom.articles.all()
        datas = self.paging(items, settings.NEWS_PAGE_LIMIT, page)
        result = self.news_to_json(datas['items'])
        return Response({'total': datas['total_number'], 'data': result})


class ProductTableView(BaseAPIView):
    def get(self, request, id, page):
        if id:
            try:
                prokey = [ProductKeyword.objects.get(id=id)]
            except ProductKeyword.DoesNotExist:
                group = Group.objects.filter(company=u'广东省质监局')
                prokey = group[0].productkeyword_set.all()
        else:
            group = Group.objects.filter(company=u'广东省质监局')
            prokey = group[0].productkeyword_set.all()

        prokey_len = len(prokey)
        product = [prokey[i].product for i in xrange(prokey_len)]

        data = [p.articles.all() for p in product]
        if data != []:
            item = reduce(lambda x, y: list(set(x).union(set(y))), data)
        else:
            item =[]
        article_ids = [item[i].id for i in range(len(item))]
        item = Article.objects.filter(id__in=article_ids)

        datas = self.paging(item, settings.NEWS_PAGE_LIMIT, page)
        result = self.news_to_json(datas['items'])
        return Response({'total': datas['total_number'], 'data': result})


class CustomWeixinView(BaseAPIView):
    CUSTOM_WEIXIN_LIMIT = 10
    def get(self, request, custom_id, page):
        user = request.myuser
        try:
            keyword = CustomKeyword.objects.get(id=int(custom_id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return Response({'html': '', 'total': 0})
        items = keyword.custom.weixin.all()
        datas = self.paging(items, self.CUSTOM_WEIXIN_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html = self.set_css_to_weixin(items)
        return Response({'html': html, 'total': datas['total_number']})


class CustomWeiboView(BaseAPIView):
    CUSTOM_WEIBO_LIMIT = 10
    def get(self, request, custom_id, page):
        user = request.myuser
        try:
            keyword = CustomKeyword.objects.get(id=int(custom_id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return Response({'html': '', 'total': 0})
        items = keyword.custom.weibo.all()
        datas = self.paging(items, self.CUSTOM_WEIBO_LIMIT, page)
        items = [set_logo(data) for data in datas['items']]
        html = self.set_css_to_weibo(items)
        return Response({'html': html, 'total': datas['total_number']})


class CustomModifyView(View):
    def save(self, user):
        count = CustomKeyword.objects.filter(group=user.group).exclude(custom__isnull=False).count()
        if count >= 5:
            return {"status": False}
        try:
            custom = CustomKeyword(newkeyword=self.keyword, group=user.group)
            custom.save(using='master')
        except IntegrityError:
            return {"status": False}
        return {"status": True}

    def remove(self, user):
        pass

    def post(self, request, action):
        try:
            self.keyword = request.POST['keyword']
        except KeyError:
            return HttpResponse(status=404)
        user = self.request.myuser
        status = {"status": False}
        if action == 'add':
            status = self.save(user)
        if action == 'remove':
            status = self.delete(user)
        return JsonResponse({'status': status['status']})

class InspectionLocalView(BaseAPIView):
    def get(self, request):
        user = request.myuser
        company = user.group.company
        inspection_list = Inspection.objects.exclude(qualitied__lt=0).filter(source=company).order_by('-pubtime')[:10]

        tz  = pytz.timezone(settings.TIME_ZONE)
        for item in inspection_list:
            timel = item.pubtime.astimezone(tz)
            item.pubtime = timel
            item.qualitied = str(int(item.qualitied*100)) + '%'

        inspection = render_to_string('inspection/dashboard_inspection.html', {'inspection_list': inspection_list})
        return HttpResponse(inspection)


class InspectionNationalView(BaseAPIView):
    def get(self, request):
        user = request.myuser
        user.company = user.group.company
        inspection_list = Inspection.objects.exclude(qualitied__lt=0).all().order_by('-pubtime')[:10]

        tz  = pytz.timezone(settings.TIME_ZONE)
        for item in inspection_list:
            timel = item.pubtime.astimezone(tz)
            item.pubtime = timel
            item.qualitied = str(int(item.qualitied*100)) + '%'

        inspection = render_to_string('inspection/dashboard_inspection.html', {'inspection_list': inspection_list})
        return HttpResponse(inspection)


class InspectionTableView(BaseAPIView):
    def get(self, request):
        result = []
        news = Inspection.objects.exclude(qualitied__lt=0).order_by('-pubtime').all()

        for item in news:
            #collected_html = u'<i class="fa fa-star-o" data-toggle="tooltip", data-placement="right" title="添加收藏">'
            title = self.title_html(item.url, item.name, item.id, 'inspection')
            quality = str(int(item.qualitied*100)) + '%'
            #one_record = [collected_html, item.product, title, quality, item.source, item.pubtime.strftime('%Y-%m-%d')]
            tz  = pytz.timezone(settings.TIME_ZONE)
            timel = item.pubtime.astimezone(tz)

            one_record = [item.product, title, quality, item.source, timel.strftime('%Y-%m-%d')]
            result.append(one_record)

        return Response({"inspection": result})

        #items = Inspection.objects.order_by('-pubtime').all()
        #datas = self.paging(items, settings.NEWS_PAGE_LIMIT, page)
        #result = self.inspection_to_json(datas['items'])
        #return Response({"total": datas['total_number'], "data": result})

    def inspection_to_json(self, items):
        result = []
        for data in items:
            item = {}
            item['title'] = data.name
            item['source'] = data.source
            item['category'] = data.product
            item['quality'] = str(data.qualitied * 100)[:4] + "%"
            item['time'] = data.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d')
            item['source'] = data.source
            result.append(item)
        return result


class WeixinView(BaseAPIView):
    Weixin_table_limit = 20
    def get(self, request):
        parameter = request.GET

        api_type = parameter['type']
        sort = parameter['sort'] if parameter.has_key('sort') else 'hot'
        page = parameter['page'] if parameter.has_key('page') else 1
        limit = self.Weixin_table_limit if api_type == 'list' else 6

        if sort == 'new':
            datas = self.paging(Weixin.objects.all(), limit, page)
        else: # hot
            datas = self.paging(Weixin.objects.all(), limit, page)
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weixin/%s_tpl.html' % api_type, {'weixin_list':  items})
        return Response({'html': html_string, 'total': datas['total_number']})


class WeiboView(BaseAPIView):
    Weibo_table_limit = 20

    def get(self, request):
        parameter = request.GET

        api_type = parameter['type']
        sort = parameter['sort'] if parameter.has_key('sort') else 'hot'
        page = parameter['page'] if parameter.has_key('page') else 1
        limit = self.Weibo_table_limit if api_type == 'list' else 6

        if sort == 'new':
            datas = self.paging(Weibo.objects.all(), limit, page)
        else:
            datas = self.pagingfromredis(Weibo, limit, page)
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weibo/%s_tpl.html' % api_type, {'weibo_list':  items})
        return Response({'html': html_string, 'total': datas['total_number']})



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
    name_list =  map(lambda x: x.split('.')[0], file_list)

    count = 0
    for i in name_list :
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
    #authencate success
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

        d =  dict(rows)
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
        #values.append({'name': item.name, 'value': 80})
    values = [item for item in values if item['value']]
    return JsonResponse({'name': name, "value": values})

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

def chart_line(date_range, min_date, max_date, articles):
    #data range by year   less one axis has data
    if date_range.days > 6 * 55:
        return year_range(min_date, max_date, date_range, articles)
    #data range by season   less two axis has data
    elif date_range.days > 6 * 30:
        return season_range(min_date, max_date, date_range, articles)
    #data range by month    less two axis has data
    elif  date_range.days >= 3 * 10:
        return months_range(min_date, max_date, date_range, articles)
    #data range by weeks    less one axis has data
    elif date_range.days > 7:
        return week_range(min_date, max_date, date_range, articles)
    #data range by days     less one axis has data
    elif date_range.days >= 0:
        return days_range(min_date, max_date, date_range, articles)
    else:
        return unstable()

@api_view(['GET'])
@login_required
def chart_pie_event_view(request, topic_id):
    try:
        topic = Topic.objects.get(id=int(topic_id))
    except (KeyError, ValueError, Topic.DoesNotExist):
        return HttpResponse(status=400)

    #data = topic.articles.values('publisher__publisher').annotate(value=Count('publisher__publisher'))
    #name = []
    #value= []
    #for item in data:
    #    item['name'] = item.pop('publisher__publisher')
    #    name.append(item['name'])
    #    value.append(item)
    name = [u'新闻媒体', u'政府网站', u'自媒体']
    value = [{u'name': u'新闻媒体', u'value': topic.articles.filter(publisher__searchmode=1).count()},
             {u'name': u'政府网站', u'value': topic.articles.filter(publisher__searchmode=0).count()},
             {u'name': u'自媒体', u'value': topic.weibo.count()+topic.weixin.count()}]
    value = [item for item in value if item['value']]
    return JsonResponse({u'name': name, u'value': value})


def chart_pie_risk_view(request, risk_id):
    try:
        risk = Risk.objects.get(id=int(risk_id))
    except (KeyError, ValueError, Risk.DoesNotExist):
        return HttpResponse(status=400)
    name = [u'新闻媒体', u'政府网站', u'自媒体']
    value = [{u'name': u'新闻媒体', u'value': risk.articles.filter(publisher__searchmode=1).count()},
             {u'name': u'政府网站', u'value': risk.articles.filter(publisher__searchmode=0).count()},
             {u'name': u'自媒体', u'value': risk.weibo.count()+risk.weixin.count()}]
    value = [item for item in value if item['value']]
    return JsonResponse({u'name': name, u'value': value})

def map_view(request):
    data = cPickle.load(file(os.path.join(BASE_DIR, "yqj/jobs/minutely/map.json"), "r"))
    risk_data = data["regionData"]
    return JsonResponse({"regionData": risk_data })

