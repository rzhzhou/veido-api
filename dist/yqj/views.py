# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db import connection
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.utils import timezone

from base import login_required, get_user_image
from base.views import BaseTemplateView
from base.models import (Area, Article, ArticlePublisher, Category, Collection,
    Custom, CustomKeyword, Group, Inspection, Product, ProductKeyword,
    RelatedData, Topic, Weibo, Weixin)
from yqj.redisconnect import RedisQueryApi


def SetLogo(obj):
    if not obj.publisher.photo:
        obj.publisher.photo = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
    return obj


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
        event_news_number = Article.objects.filter(website_type='topic').count()
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
            data = SetLogo(data)

        # inspection_list = Inspection.objects.filter(source=user.company).order_by('-pubtime')[:10]
        # for item in inspection_list:
        #     item.qualitied = str(int(item.qualitied*100)) + '%'
        # inspection = render_to_string('inspection/dashboard_inspection.html', {'inspection_list': 'inspection_list'})
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
            'weixin_hottest_list': weixin_data,
            'weibo_hottest_list': weibo_data,
            'user_image': get_user_image(user),
            # 'inspection_list': inspection,
            })
    else:
        return HttpResponse(status=401)

class CategoryView(BaseTemplateView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = ''
        return self.render_to_response('category/category.html', {'category': category})


class LocationView(BaseTemplateView):
    def get(self, request, location_id):
        """
        try:
            location = Area.objects.get(id=int(location_id))
        except Area.DoesNotExist:
            location = ''
        weixin = [SetLogo(data) for data in Weixin.objects.filter(area=location)][:10]
        weibo = [SetLogo(data) for data in Weibo.objects.filter(area=location)][:10]
        return self.render_to_response("location/location.html", {'location': location, 'weixin_list': weixin, 'weibo_list': weibo})
        """
        try:
            location = Area.objects.get(id=int(location_id))
        except Area.DoesNotExist:
            location = ''
        return self.render_to_response("location/location.html", {'location': location})


def person_view(request, person_id):
    return HttpResponse('person')


class EventView(BaseTemplateView):
    def get(self,request):
        return self.render_to_response('event/event_list.html')


class EventDetailView(BaseTemplateView):
    def get(self, request, id):
        try:
            event_id = int(id)
            event = Topic.objects.get(id=event_id)
            eval_keywords_list = eval(event.keywords) if event.keywords else []
            keywords_list = [{"name": name, "number": number} for name, number in eval_keywords_list]
        except Topic.DoesNotExist:
            return self.render_to_response('event/event.html', {'event': '', 'weixin_list': [], 'weibo_list': []})
        user = self.request.myuser
        try:
            collection = user.collection
        except Collection.DoesNotExist:
            collection = Collection(user=user)
            collection.save(using='master')
        items = user.collection.events.all()
        iscollected = any(filter(lambda x: x.id == event.id, items))
        #weixin_list = [SetLogo(item) for item in event.weixin.all()][:10]
        #weibo_list = [SetLogo(item) for item in event.weibo.all()][:10]
        #for item in weibo_list:
        #    SetLogo(item)
        #    if len(item.content) < 144:
        #        setattr(item, 'short', True)
        #return self.render_to_response('event/event.html', {'event': event, 'weixin_list': weixin_list, 'weibo_list': weibo_list})
        return self.render_to_response('event/event.html', {'event': event, 'keywords_list': keywords_list, 'isCollected': iscollected})


class WeixinView(BaseTemplateView):
    def get(self, request):
        hottest = [SetLogo(data) for data in Weixin.objects.order_by('-pubtime')[0:20]]
        weixin = Weixin.objects.all()
        latest = self.paging(weixin, 20, 1)
        items = [SetLogo(data) for data in latest['items']]
        html = self.set_css_to_weixin(items)
        return self.render_to_response('weixin/weixin_list.html', {'weixin_latest_list': latest,
                                                                   'weixin_hottest_list': hottest,
                                                                   'html': html,
                                                                   'total_page_number': latest['total_number']})


class WeixinDetailView(BaseTemplateView):
    def get(self, request, id):
        try:
            weixin_id = int(id)
            weixin = Weixin.objects.get(id=weixin_id)
        except Weixin.DoesNotExist:
            return render_to_response('weixin/weixin.html', {'article': '', 'relate': []})
        try:
            r = RelatedData.objects.filter(uuid=weixin.uuid)[0]
            relateddata = list(r.weixin.all()) + list(r.weibo.all()) + list(r.articles.all())
        except IndexError:
            relateddata = []
        return self.render_to_response('weixin/weixin.html', {'article': SetLogo(weixin), 'relate': relateddata})


class WeiboView(BaseTemplateView):
    def get(self, request):
        latest = [SetLogo(data) for data in Weibo.objects.order_by('-pubtime')[0:20]]
        for item in latest:
            if len(item.content) < 144:
                setattr(item, 'short', True)
        hottest  = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:20]]
        for data in hottest:
            data['pubtime'] = datetime.fromtimestamp(data['pubtime'])
            if data['photo'] == 'kong':
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
            if len(data['content']) < 144:
                data['short'] = True
        return self.render_to_response('weibo/weibo_list.html', {'weibo_latest_list': latest, 'weibo_hottest_list': hottest})


class CollectionView(BaseTemplateView):
    def get(self, request):
        return self.render_to_response('user/collection.html')


class SettingsView(BaseTemplateView):
    def get(self, request):

        return self.render_to_response('user/settings.html')


class CustomListView(BaseTemplateView):
    custom_list_num = 5
    def get(self, request):
        user = self.request.myuser
        newkeyword_list = CustomKeyword.objects.filter(group=user.group).exclude(custom__isnull=False)
        searchkeyword_list = CustomKeyword.objects.filter(group=user.group).exclude(custom__isnull=True)
        keyword_list = []
        for keyword in searchkeyword_list:
            setattr(keyword, 'name', keyword.newkeyword)
            setattr(keyword, 'news_list', keyword.custom.articles.all()[:self.custom_list_num])
            keyword_list.append(keyword)
        return self.render_to_response('custom/custom_list.html', {'custom_list': keyword_list, 'keyword_list': newkeyword_list})

    def get_news(self, keyword):
        return Article.objects.raw(u"SELECT * FROM article WHERE MATCH (content, title) AGAINST ('%s') LIMIT %s" % (keyword, self.custom_list_num))


class CustomView(BaseTemplateView):
    def get(self, request, id):
        user = request.myuser
        try:
            custom = CustomKeyword.objects.get(id=int(id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return self.render_to_response('custom/custom.html', {'name': u''})
        return self.render_to_response('custom/custom.html', {'name': custom.newkeyword})


class ProductView(BaseTemplateView):
    def get(self, reqeust, id):
        if id:
            try:
                prokeyword = ProductKeyword.objects.get(id=id)
                name = prokeyword.newkeyword
            except:
                name = u'全部'
                if id != '0':
                    return HttpResponseRedirect("/product/0/")
        else:
            return HttpResponseRedirect("/product/0/")
        try:

            group = Group.objects.filter(company=u'广东省质监局')
            prokeywords = group[0].productkeyword_set.all()
        except:
            return self.render_to_response('product/product.html', {'product_list': [{'id': '', 'name': ''}],'product': {'name': u'全部'}})
        prokey_len = len(prokeywords)
        prokeyword_list = [{'id': '0', 'name': u'全部'}] + [{'id': prokeywords[i].id, 'name': prokeywords[i].newkeyword} for i in xrange(0, prokey_len)]
        return self.render_to_response('product/product.html', {'product_list': prokeyword_list, 'product': {'name': name}})


class UserView(BaseTemplateView):
    def get(self, request):
        return self.render_to_response('user/user.html')


class UserAdminView(BaseTemplateView):

    def get(self, request):
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
        return self.render_to_response('user/user.html', {'user_list': user_list})

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


class SearchView(BaseTemplateView):
    def get(self, request, keyword):
        return self.render_to_response('search/result.html')


class InspectionView(BaseTemplateView):
    def get(self, request):
        return self.render_to_response('inspection/inspection_list.html', {})
