#coding=utf-8

import os
import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db import models, connection, IntegrityError
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from yqj.models import (Article, Area, Weixin, Weibo, Topic, RelatedData, ArticleCategory,
                            save_user, Collection, Topic, hash_password, User, Custom, Inspection)
from yqj.views import SetLogo
from serializers import ArticleSerializer
from yqj import authenticate, login_required
from django.db.models import Count
from api_function import GetFirstDaySeason, get_season
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from yqj.redisconnect import RedisQueryApi

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
    print request.method

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

    return JsonResponse({'status': True})


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class TableAPIView(APIView):
    COLLECTED_TEXT = u'<i class="fa fa-star" data-toggle="tooltip", data-placement="right" title="取消收藏">'
    NO_COLLECTED_TEXT = u'<i class="fa fa-star-o" data-toggle="tooltip", data-placement="right" title="添加收藏">'

    LIMIT_NUMBER = 300
    def __init__(self, request=None):
        self.request = request

    def collected_html(self, item):
        items = self.collected
        return self.COLLECTED_TEXT if self.isIn(item, items) else self.NO_COLLECTED_TEXT

    def isIn(self, item, items):
        if isinstance(item, models.Model):
            item_id = item.id
        else:
            item_id = item['id']

        if item_id is None:
            raise TypeError('item should has id atrribute or id key')

        return any(filter(lambda x: x.id == item_id, items))

    @property
    def collected(self):
        if getattr(self, '_collected', None) is None:
            self._collected = self.collected_items()
        return self._collected

    def collected_items(self):
        #return []
        #try:
        user = self.request.myuser
        try:
            self.collection = user.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save()
        return user.collection.articles.all()
        #except:
        #    return []

    def title_html(self, *args):
        title_format = u'<a href="{0}" title="{1}" target="_blank" data-id="{2}" data-type="{3}">{1}</a>'
        return title_format.format(*args)

    def set_css_to_weixin(self, items):
        html = ""
        count = u'0'
        for item in items:
            html += """<li class="media">"""
            html += """<div class="media-left">"""
            html +=  u'<img class="media-object" src="%s" alt="%s">' % (item.publisher.photo, item.publisher.publisher)
            html += """</div>
                       <div class="media-body"> """
            html +=  u'<h4 class="media-heading">%s</h4>' % (item.publisher.publisher)
            html +=  u'<p><a href="/weixin/%s/" target="_blank">%s</a></p>' % (item.id, item.title)
            html += """<div class="media-meta">
                       <div class="info pull-right">"""
            html +=  u'<span>阅读 %s</span>' % count
            html +=  u'<span><i class="fa fa-thumbs-o-up"></i> %s</span>' % count
            html += """</div>"""
            html +=  u'<div class="time pull-left">%s</div>' % item.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M')
            html += """</div></div></li>"""
        return html

    def set_css_to_weibo(self, items):
        html = ""
        count = u'0'
        for item in items:
            html += """<li class="media">"""
            html += """<div class="media-left">"""
            html +=  u'<img class="media-object" src="%s" alt="%s">' % (item.publisher.photo, item.publisher.publisher)
            html += """</div>
                       <div class="media-body"> """
            html +=  u'<h4 class="media-heading">%s</h4>' % (item.publisher.publisher)
            if len(item.content) < 200:
                 html +=  u'<p>%s</p>' % (item.content)
            else: 
                 html +=  u'<p><a href="%s" target="_blank">%s</a></p>' % (item.url, item.title)
            html += """<div class="media-meta">
                       <div class="info pull-right">"""
            html +=  u'<span>转载 %s</span>' % count
            html +=  u'<span>评论 %s</span>' % count
            html +=  u'<span><i class="fa fa-thumbs-o-up"></i> %s</span>' % count
            html += """</div>"""
            html +=  u'<div class="time pull-left">%s</div>' % item.pubtime.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M')
            html += """</div></div></li>"""
        return html

    def paging(self, model, limit, page):
        #limit  每页显示的记录数 page 页码
        items = model.objects.all()
        # 实例化一个分页对象
        paginator = Paginator(items, limit)
	try:
            # 获取某页对应的记录
            items = paginator.page(page)
        except PageNotAnInteger: 
            # 如果页码不是个整数 取第一页的记录
            items = paginator.page(1)
        except EmptyPage:  
            # 如果页码太大，没有相应的记录 取最后一页的记录
            items = paginator.page(paginator.num_pages)

        return {'items': items, 'total_number': paginator.num_pages}
    
    def pagingfromredis(self, model, limit, page):
        items = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)]
        # 实例化一个分页对象
        paginator = Paginator(items, limit)
	try:
            # 获取某页对应的记录
            items = paginator.page(page)
        except PageNotAnInteger: 
            # 如果页码不是个整数 取第一页的记录
            items = paginator.page(1)
        except EmptyPage:  
            # 如果页码太大，没有相应的记录 取最后一页的记录
            items = paginator.page(paginator.num_pages)

        return {'items': items, 'total_number': paginator.num_pages}
        

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

class NewsTableView(TableAPIView):
    def get(self, request):
        result = []
        news = Article.objects.all()[:1738]
        serializer = ArticleSerializer(news, many=True)

        for item in news:
            collected_html = u'<i class="fa fa-star-o" data-toggle="tooltip", data-placement="right" title="添加收藏">'
            #collected_html = self.collected_html(item)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            try:
                hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            except IndexError:
                hot_index = 0
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
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
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)

        return Response({"news": result})


class EventTableView(TableAPIView):
    def collected_items(self):
        user = self.request.myuser
        return user.collection.events.all()

    def get(self, request):
        result = []
        event = Topic.objects.all()[:self.LIMIT_NUMBER]
        for item in event:
            collected_html = self.collected_html(item)
            url = u'/event/%s' % item.id
            title = self.title_html(url, item.title, item.id, 'topic')
            hot_index = item.articles.all().count() + item.weixin.all().count() + item.weibo.all().count()
            time = item.articles.all().order_by('-pubtime')
            if time:
                pubtime = time[0].pubtime
            else:
                pubtime = datetime.datetime.now()
            one_record = [collected_html, title, item.source, item.area.name, pubtime.date(), hot_index]
            result.append(one_record)
        return Response({"event": result})


class EventDetailTableView(TableAPIView):
    def get(self, request, id):
        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return Response({'news': ''})
        news = event.articles.all()
        result = []
        for item in news:
            collected_html = self.collected_html(item)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title, item.id, 'article')
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)
        return Response({'news': result})


    def get_collected_html(self, item):
        pass

class CollectView(APIView):
    def article_html(self, item):
        url = u'/news/%s' % item.id
        view = ArticleTableView(self.request)
        title = view.title_html(url, item.title, item.id, 'article')
        hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
        line = [view.collected_html(item), title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
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
            pubtime = datetime.datetime.now()
        one_record = [view.collected_html(item), title, item.source, item.area.name, pubtime.date(), hot_index]
        return one_record

    def get(self, request):
        try:
            self.collection = request.myuser.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save()
        news = [self.article_html(item) for item in self.collection.articles.all()]
        topic = [self.topic_html(item) for item in self.collection.events.all()]

        return Response({'news': news, 'event': topic})


class CollecModifyView(View):
    def save(self, item):
        data = {self.related_field: item, 'collection': self.collection}
        if isinstance(item, Article):
            category = item.categorys.all()[0]
            data['category'] =  category.name
        try:
            collection_item = self.get_related_model().objects.create(**data)
            collection_item.save()
        except IntegrityError:
             pass


    def delete(self, item):
        try:
            collectitem = self.get_collection_model().objects.get(**{self.related_field: item, 'collection': self.collection})
            collectitem.delete()
        except self.get_collection_model.DoesNotExist:
            pass

    @property
    def related_field(self):
        return self.data_type.lower()

    def get_related_model(self):
        return models.get_model('yqj', self.data_type.capitalize() + 'Collection')

    def _create_collection(self):
        #add a collection to the user
        try:
            _collection = self.request.myuser.collection
        except ObjectDoesNotExist:
            _collection = Collection(user=user)
            _collection.save()
        return _collection

    @property
    def collection(self):
        return self._create_collection()

    def get_model(self):
        return models.get_model('yqj', self.data_type.capitalize())

    def get_collection_model(self):
        return models.get_model('yqj', self.data_type.capitalize() + 'Collection')

    def post(self, request, action, *args, **kwargs):
        try:
            print request.POST['type'], request.POST['id']
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
            self.collection.save()
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


class CustomTableView(TableAPIView):
    def get(self, request, custom_id):
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


class InspectionTableView(TableAPIView):
    def get(self, request):
        result = []
        news = Inspection.objects.order_by('-pubtime').all()

        for item in news:
            collected_html = u'<i class="fa fa-star-o" data-toggle="tooltip", data-placement="right" title="添加收藏">'
            title = self.title_html(item.url, item.name, item.id, 'inspection')
            quality = str(item.qualitied * 100)[:4] + "%"
            one_record = [collected_html, item.product, title, quality, item.source, item.pubtime.strftime('%Y-%m-%d')]
            result.append(one_record)

        return Response({"inspection": result})


class WeixinTableView(TableAPIView):
    weixin_table_limit = 20
    def get(self, request, weixin_type, page):
        if weixin_type == 'new':
            datas = self.paging(Weixin, self.weixin_table_limit, page)
        elif weixin_type == 'hot':
            datas = self.paging(Weixin, self.weixin_table_limit, page)
        items = [SetLogo(data) for data in datas['items']]
        html = self.set_css_to_weixin(items)
        return Response({'html': html, 'total': datas['total_number']})


class WeiboTableView(TableAPIView):
    weibo_table_limit = 20
    def set_css_to_hotweibo(self, items):
        html = ""
        count = u'0'
        for item in items:
            html += """<li class="media">"""
            html += """<div class="media-left">"""
            html +=  u'<img class="media-object" src="%s" alt="%s">' % (item['photo'], item['publisher'])
            html += """</div>
                       <div class="media-body"> """
            html +=  u'<h4 class="media-heading">%s</h4>' % (item['publisher'])
            if len(item['content']) < 200:
                 html +=  u'<p>%s</p>' % (item['content'])
            else: 
                 html +=  u'<p><a href="%s" target="_blank">%s</a></p>' % (item['url'], item['title'])
            html += """<div class="media-meta">
                       <div class="info pull-right">"""
            html +=  u'<span>转载 %s</span>' % item['reposts_count']
            html +=  u'<span>评论 %s</span>' % item['comments_count']
            html +=  u'<span><i class="fa fa-thumbs-o-up"></i> %s</span>' % item['attitudes_count']
            html += """</div>"""
            html +=  u'<div class="time pull-left">%s</div>' % datetime.datetime.fromtimestamp(item['pubtime']).strftime('%Y-%m-%d %H:%M')
            html += """</div></div></li>"""
        
        return html

    def get(self, request, weibo_type, page):
        if weibo_type == 'new':
            datas = self.paging(Weibo, self.weibo_table_limit, page)
        elif weibo_type == 'hot':
            hot_datas = self.pagingfromredis(Weibo, self.weibo_table_limit, page)
            for data in hot_datas['items']:
                if not data['photo']:
                    data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1' 
            html = self.set_css_to_hotweibo(hot_datas['items'])
            return Response({'html': html, 'total': hot_datas['total_number']})
        items = [SetLogo(data) for data in datas['items']]
        html = self.set_css_to_weibo(items)
        return Response({'html': html, 'total': datas['total_number']})
        


@login_required
def upload_image(request):
    user = request.myuser
    try:
        f = request.FILES['image']
    except KeyError:
        return HttpResponse(status=400)

    media_path = settings.MEDIA_ROOT
    filename = str(user.id) + os.path.splitext(f.name)[1]

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
        user.save()
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
            user.save()
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
            delete_user.delete()
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

    save_user(username, password, myuser.area, myuser.group)
    return JsonResponse({'status': True})

def get_count_feeling(start_d, end_d, feeling_type):
    feeling_limit = ''
    if feeling_type == 'positive':
        feeling_limit = 'feeling_factor >= 0.6'
    elif feeling_type == 'negative':
        feeling_limit = 'feeling_factor <= 0.4'
    else:
        feeling_limit = 'feeling_factor > 0.4  and feeling_factor < 0.6'

    with connection.cursor() as c:
        sql_str = "SELECT Date(pubtime), COUNT(*) FROM article where Date(pubtime) >= '{0}' and Date(pubtime) < '{1}' and {2} group by Date(pubtime)".format(start_d, end_d, feeling_limit)
        c.execute(sql_str)
        rows = c.fetchall()

        d =  dict(rows)
        result = []
        day = start_d
        while day < end_d:
            num = d[day] if day in d else 0
            result.append(num)
            day = day + datetime.timedelta(days=1)
        return result

@login_required
def chart_line_index_view(request):
    today = datetime.datetime.today().date()
    start_d = today - datetime.timedelta(days=6)
    end_d = today + datetime.timedelta(days=1)

    data = {}
    data['date'] = [(today - datetime.timedelta(days=x)).strftime("%m-%d") for x in reversed(range(7))]
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
    #data range by season
    if date_range.days > 6 * 30:
        #get first day of the current season
        current_date = GetFirstDaySeason(datetime.datetime.now())
        #only get recent 4 season data
        begin_date =  current_date - relativedelta(year=1)
        negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
        for art in articles:
            date = GetFirstDaySeason(art.pubtime)
            if date < begin_date:
                continue
            factor = art.feeling_factor
            if factor > 0.6:
                positive[date] += 1
            elif factor < 0.4 and factor > 0:
                negative[date] += 1
            else:
                neutral[date] += 1

        range_date = [ current_date - relativedelta(months=i) for i in range(12, 0, -3) ]

        data = {}
        data['negative'] = [ negative[date] for date in range_date]
        data['positive'] = [ positive[date] for date in range_date]
        data['neutral'] = [ neutral[date] for date in range_date]
        data['date'] = [ str(date.year) + get_season(date) for date in range_date]
        return JsonResponse(data)


    #data range by month
    elif  date_range.days > 6 * 7:
        #get first day of the current month
        current_date = datetime.datetime.now().date().replace(day=1)
        #only get recent 6 months data
        begin_date =  current_date - relativedelta(months=6)

        negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
        for art in articles:
            date = art.pubtime.date().replace(day=1)
            if date < begin_date:
                continue
            factor = art.feeling_factor
            if factor > 0.6:
                positive[date] += 1
            elif factor < 0.4 and factor > 0:
                negative[date] += 1
            else:
                neutral[date] += 1

        range_date = [ current_date - relativedelta(months=i) for i in range(6, -1, -1) ]

        data = {}
        data['negative'] = [ negative[date] for date in range_date]
        data['positive'] = [ positive[date] for date in range_date]
        data['neutral'] = [ neutral[date] for date in range_date]
        data['date'] = [ date.strftime("%Y-%m") for date in range_date]
        return JsonResponse(data)
    #data range by weeks
    else:
        #find the first day of current week
        today = datetime.datetime.now().date()
        first_day = today - datetime.timedelta(days=today.weekday())
        begin_date =  first_day - relativedelta(weeks=6)

        get_week = lambda x : (first_day - x).days / 7 + 1
        negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
        for art in articles:
            week = get_week(art.pubtime.date())
            if week > 6:
                continue
            factor = art.feeling_factor
            if factor > 0.6:
                positive[week] += 1
            elif factor < 0.4 and factor > 0:
                negative[week] += 1
            else:
                neutral[week] += 1
        range_week = range(6, -1, -1)

        data = {}
        data['positive'] = [ positive[week] for week in range_week ]
        data['negative'] = [ negative[week] for week in range_week ]
        data['neutral'] = [ neutral[week] for week in range_week ]
        data['date'] = [ (first_day - datetime.timedelta(days=i*7)).strftime("%m-%d") for i in range_week ]
        return JsonResponse(data)


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

