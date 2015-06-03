#coding=utf-8
import datetime
import os

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from yqj.models import Article, Weixin, Weibo, RelatedData, ArticleCategory,\
                       Area, Topic, Inspection, Custom, Keyword, Collection,ArticlePublisher
from yqj import login_required
from yqj.redisconnect import RedisQueryApi
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from simArticle import sim_article

def SetLogo(obj):
    if not obj.publisher.photo:
        obj.publisher.photo = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
    return obj

@login_required
def index_view(request):
    user = request.myuser
    if user.is_authenticated():
        categories = ArticleCategory.objects.filter(~Q(name='其他'))
        locations = Area.objects.filter(level=user.area.level+1, parent=user.area)
        user.company = user.group.company

        #news = Article.objects.filter(website_type='topic').count()
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


        end_date = timezone.now()
        start_date = end_date + datetime.timedelta(days=-7)
        news_list = Article.objects.filter(website_type='hot' , pubtime__range=(start_date, end_date)).order_by('-pubtime')[:news_list_number]
        for item in news_list:
            try:
                setattr(item, 'hot_index', RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count())
            except IndexError:
                setattr(item, 'hot_index', 0)
        #news_list = sorted(news_list, key = lambda x: x.hot_index, reverse=True)[:news_list_number]

        event_list = Topic.objects.all()
        for iteml in event_list:
            try:
                setattr(iteml, 'time', iteml.articles.order_by('pubtime')[0].pubtime.replace(tzinfo=None).strftime('%Y-%m-%d'))
            except IndexError:
                setattr(iteml, 'time', datetime.datetime.now().strftime('%Y-%m-%d'))
        event_list=sorted(event_list, key=lambda x: x.time, reverse=True)[:event_list_number]
        #item['time'] = data.articles.order_by('pubtime')[0].pubtime.replace(tzinfo=None).strftime('%Y-%m-%d')
        for item in event_list:
             setattr(item, 'hot_index', item.articles.all().count()+item.weixin.all().count()+item.weibo.all().count())
        # event_list=sorted(event_list[:event_list_number],key=lambda x: x.hot_index, reverse=True)
        #event_list = sorted(event_list, key = lambda x: x.hot_index, reverse=True)[:event_list_number]

        weibo_data = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:5]]
        for data in weibo_data:
            data['pubtime'] = datetime.datetime.fromtimestamp(data['pubtime'])
            if not data['photo']:
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
            if len(data['content']) < 200:
                data['short'] = True

        weixin_data = Weixin.objects.all()[0:weixin_list_number]
        for data in weixin_data:
            data = SetLogo(data)

        inspection_list = Inspection.objects.order_by('-pubtime')[:10]
        for item in inspection_list:
            item.qualitied = str(int(item.qualitied*100)) + '%'

        return render_to_response("dashboard/dashboard.html",
            {'user': user,
            'categories': categories,
            'locations': locations,
            'news': {'number': news_number, 'percent': news_percent},
            'weibo': {'number': weibo_number, 'percent': weibo_percent},
            'weixin': {'number': weixin_number, 'percent': weixin_percent},
            'event': {'number': event, 'percent': event_percent},
            'news_list': news_list,
            'event_list': event_list,
            'weixin_hottest_list': weixin_data,
            'weibo_hottest_list': weibo_data,
            'user_image': get_user_image(user),
            'inspection_list': inspection_list,
            })
    else:
        return HttpResponse(status=401)

def get_user_image(user):
    image_url = None
    for filename in os.listdir(settings.MEDIA_ROOT):
        if os.path.splitext(filename)[0] == str(user.id):
            image_url = os.path.join('/media', filename)
    if image_url is None:
        image_url = '/static/img/avatar.jpg'
    return image_url

class LoginRequiredMixin(object):
    ALLOWED_METHOD = ['GET']

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class BaseView(LoginRequiredMixin, View):
    INCLUDE_SIDEBAR = True
    INCLUDE_USER = True

    def render_to_response(self, template_path, context={}):
        if self.INCLUDE_SIDEBAR:
            categories = self.get_article_categories()
            #for ctg in categories:
            #    ctg.id = encrypt(ctg.id)
            context['categories'] = categories

        if self.INCLUDE_USER:
            user = self.request.myuser
            user.company = user.group.company
            context['user'] = user

        context['user_image'] = get_user_image(user)
        context['locations'] = self.get_locations(user.area)
        return render_to_response(template_path, context)

    def get_article_categories(self):
        return ArticleCategory.objects.filter(~Q(name = '其他'))

    def get_locations(self, area):
        #area = Area.objects.get(id=int(location_id))
        if area.id == 4:
            return []
        return Area.objects.filter(parent=area, level=area.level+1)

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
            html +=  u'<div class="time pull-left">%s</div>' % item.pubtime.strftime('%Y-%m-%d %h:%m')
            html += """</div></div></li>"""
        return html

    def set_css_to_weibo(self, items):
        pass

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

class CategoryView(BaseView):
    def get(self, request, category_id):
        try:
            category = ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            category = ''
        return self.render_to_response('category/category.html', {'category': category})


class LocationView(BaseView):
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


class NewsView(BaseView):
    def get(self, request):
        return self.render_to_response('news/news_list.html', {})


class NewsDetailView(BaseView):
    def get(self, request, news_id):
        try:
            news_id = int(news_id)
            news = Article.objects.get(id=news_id)
        except Article.DoesNotExist:
            return self.render_to_response('news/news.html', {'article': '', 'relate': []})

        try:
            r = RelatedData.objects.filter(uuid=news.uuid)[0]
            relateddata = list(r.articles.all())
        except IndexError:
            relateddata = []
        try:
            event = Topic.objects.filter(articles__id=news_id)[0]
        except IndexError:
            event = ''
        user = self.request.myuser
        try:
            collection = user.collection
        except Collection.DoesNotExist:
            collection = Collection(user=user)
            collection.save(using='master')
        items = user.collection.articles.all()
        iscollected = any(filter(lambda x: x.id == news.id, items))
        return self.render_to_response('news/news.html', {'article': news, 'relate': relateddata, 'event': event, 'isCollected': iscollected})
 #sim_article(news.title,news.pubtime


class EventView(BaseView):
    def get(self,request):
        return self.render_to_response('event/event_list.html')


class EventDetailView(BaseView):
    def get(self, request, id):
        try:
            event_id = int(id)
            event = Topic.objects.get(id=event_id)
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
        return self.render_to_response('event/event.html', {'event': event, 'isCollected': iscollected})


class WeixinView(BaseView):
    def get(self, request):
        hottest = [SetLogo(data) for data in Weixin.objects.order_by('-pubtime')[0:20]]
        latest = self.paging(Weixin, 20, 1)
        items = [SetLogo(data) for data in latest['items']]
        html = self.set_css_to_weixin(items)
        return self.render_to_response('weixin/weixin_list.html', {'weixin_latest_list': latest, 
                                                                   'weixin_hottest_list': hottest, 
                                                                   'html': html,
                                                                   'total_page_number': latest['total_number']})


class WeixinDetailView(BaseView):
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


class WeiboView(BaseView):
    def get(self, request):
        latest = [SetLogo(data) for data in Weibo.objects.order_by('-pubtime')[0:20]]
        for item in latest:
            if len(item.content) < 144:
                setattr(item, 'short', True)
        hottest  = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:20]]
        for data in hottest:
            data['pubtime'] = datetime.datetime.fromtimestamp(data['pubtime'])
            if data['photo'] == 'kong':
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
            if len(data['content']) < 144:
                data['short'] = True
        return self.render_to_response('weibo/weibo_list.html', {'weibo_latest_list': latest, 'weibo_hottest_list': hottest})


class CollectionView(BaseView):
    def get(self, request):
        return self.render_to_response('user/collection.html')


class SettingsView(BaseView):
    def get(self, request):

        return self.render_to_response('user/settings.html')

class CustomListView(BaseView):
    custom_list_num = 5
    def get(self, request):
        user = self.request.myuser
        newkeyword_list = Keyword.objects.filter(group=user.group).exclude(custom__isnull=False)
        searchkeyword_list = Keyword.objects.filter(group=user.group).exclude(custom__isnull=True)
        keyword_list = []
        for keyword in searchkeyword_list:
            setattr(keyword, 'name', keyword.newkeyword)
            setattr(keyword, 'news_list', keyword.custom.articles.all()[:self.custom_list_num])
            keyword_list.append(keyword)
        return self.render_to_response('custom/custom_list.html', {'custom_list': keyword_list, 'keyword_list': newkeyword_list})

    def get_news(self, keyword):
        return Article.objects.raw(u"SELECT * FROM article WHERE MATCH (content, title) AGAINST ('%s') LIMIT %s" % (keyword, self.custom_list_num))


class CustomView(BaseView):
    def get(self, request, id):
        user = request.myuser
        try:
            custom = Keyword.objects.get(id=int(id), group=user.group)
        except Keyword.DoesNotExist:
            return self.render_to_response('custom/custom.html', {'name': u''})
        return self.render_to_response('custom/custom.html', {'name': custom.newkeyword})


class UserView(BaseView):
    def get(self, request):
        return self.render_to_response('user/user.html')


class UserAdminView(BaseView):

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


class SearchView(BaseView):
    def get(self, request, keyword):
        return self.render_to_response('search/result.html')


class InspectionView(BaseView):
    def get(self, request):
        return self.render_to_response('inspection/inspection_list.html', {})

