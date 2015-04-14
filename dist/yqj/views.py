#coding=utf-8
import datetime
import os

from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from yqj.models import Article, Weixin, Weibo, RelatedData, ArticleCategory, Area, Topic, Inspection, Custom
from yqj import login_required
from yqj.redisconnect import RedisQueryApi
from django.db.models import Q

def SetLogo(obj):
    if not obj.publisher.photo:
        obj.publisher.photo = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
    return obj

@login_required
def index_view(request):
    #user = {'name': 'wuhan', 'company': u'武汉质监局', 'isAdmin': True}
    user = request.myuser
    if user.is_authenticated():
        categories = ArticleCategory.objects.all()
        locations = Area.objects.filter(level=user.area.level+1, parent=user.area)
        user.company = user.group.company

        news = Article.objects.all().count()
        weibo = Weibo.objects.all().count()
        weixin = Weixin.objects.all().count()
        event = Topic.objects.all().count()

        news_list_number = event_list_number = 10
        weixin_list_number = weibo_list_number = 5


        end_date = datetime.datetime.now()
        start_date = end_date + datetime.timedelta(days=-7)
        news_list = Article.objects.filter(pubtime__range=(start_date, end_date))
        for item in news_list:
            item = SetLogo(item)
            try:
                setattr(item, 'hot_index', RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count())
            except IndexError:
                setattr(item, 'hot_index', 0)
        news_list = sorted(news_list, key = lambda x: x.hot_index, reverse=True)[:news_list_number]

        event_list = Topic.objects.all()
        for item in event_list:
            setattr(item, 'hot_index', item.articles.all().count()+item.weixin.all().count()+item.weibo.all().count())
        event_list = sorted(event_list, key = lambda x: x.hot_index, reverse=True)[:event_list_number]

        weibo_data = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:5]]
        for data in weibo_data:
            if data['photo'] == 'kong':
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'

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
            'news': news,
            'weibo': weibo,
            'weixin': weixin,
            'event': event,
            'news_list': news_list,
            'event_list': event_list,
            'weixin_list': weixin_data,
            'weibo_list': weibo_data,
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




class CategoryView(BaseView):
    def get(self, request, category_id):
        try:
            category = ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            category = ''
        return self.render_to_response('category/category.html', {'category': category})


class LocationView(BaseView):
    def get(self, request, location_id):
        try:
            location = Area.objects.get(id=int(location_id))
        except Area.DoesNotExist:
            location = ''
        weixin = [SetLogo(data) for data in Weixin.objects.filter(area=location)][:10]
        weibo = [SetLogo(data) for data in Weibo.objects.filter(area=location)][:10]
        return self.render_to_response("location/location.html", {'location': location, 'weixin_list': weixin, 'weibo_list': weibo})


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
            relateddata = list(r.weixin.all()) + list(r.weibo.all()) + list(r.articles.all())
        except IndexError:
            relateddata = []
        try:
            event = Topic.objects.filter(articles__id=news_id)[0]
        except IndexError:
            event = ''
        return self.render_to_response('news/news.html', {'article': SetLogo(news), 'relate': relateddata, 'event': event})


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
        weixin_list = [SetLogo(item) for item in event.weixin.all()][:10]
        weibo_list = [SetLogo(item) for item in event.weibo.all()][:10]
        return self.render_to_response('event/event.html', {'event': event, 'weixin_list': weixin_list, 'weibo_list': weibo_list})


class WeixinView(BaseView):
    def get(self, request):
        latest = [SetLogo(data) for data in Weixin.objects.order_by('-pubtime')[0:20]]
        hottest = latest
        return self.render_to_response('weixin/weixin_list.html', {'weixin_latest_list': latest, 'weixin_hottest_list': hottest})


class WeixinDetailView(BaseView):
    def get(self, request, id):
        try:
            weixin_id = int(id)
            weixin = Weixin.objects.get(id=weixin_id)
        except Weixin.DoesNotExist:
            return render_to_response('weixin/weixin.html', {'article': '', 'relate': []})
        r = RelatedData.objects.filter(uuid=weixin.uuid)[0]
        relateddata = list(r.weixin.all()) + list(r.weibo.all()) + list(r.articles.all())
        return self.render_to_response('weixin/weixin.html', {'article': SetLogo(weixin), 'relate': relateddata})


class WeiboView(BaseView):
    def get(self, request):
        latest = [SetLogo(data) for data in Weibo.objects.order_by('-pubtime')[0:20]]
        hottest  = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:20]]
        for data in hottest:
            if data['photo'] == 'kong':
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
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
        custom_list = user.group.custom.all()
        keyword_list = []
        for keyword in custom_list:
            item = {}
            item['name'] = keyword.keyword
            item['news_list'] = keyword.articles.all()[:custom_list_num]
            keyword_list.append(item)

        customname = [u'电梯',u'锅炉', u'315晚会', u'两会', u'两会', u'两会', u'两会', u'两会']
        custom_list = []
        for name in customname:
            custom_list.append({'name': name, 'news_list': self.get_news(name), 'id': customname.index(name)})
        return self.render_to_response('custom/custom_list.html', {'custom_list': custom_list})

    def get_news(self, keyword):
        return Article.objects.raw(u"SELECT * FROM article WHERE MATCH (content, title) AGAINST ('%s') LIMIT %s" % (keyword, self.custom_list_num))


class CustomView(BaseView):
    def get(self, request, id):
        try:
            custom = Custom.objects.get(id=int(id))
        except Custom.DoesNotExist:
            return self.render_to_response('custom/custom.html')
        weixin_list = custom.weixin.all()
        weibo_list = custom.weibo.all()
        customname = [u'电梯',u'锅炉', u'315晚会', u'两会', u'两会', u'两会', u'两会', u'两会']
        custom = {}
        try:
            custom['name'] = customname[int(id)]
        except KeyError:
            return self.render_to_response('custom/custom.html')
        return self.render_to_response('custom/custom.html', {'name': custom.keyword, 'weixin_list': weixin_list, 'weibo_list': weibo_list})


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
