#coding=utf-8
import datetime

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from yqj.models import Article, Weixin, Weibo, RelatedData, ArticleCategory, Area, Topic
from django.views.generic import View
from yqj import login_required

def SetLogo(obj):
    if obj.publisher.photo == 'kong':
        obj.publisher.photo = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
    return obj

@login_required
def index_view(request):
    #user = {'name': 'wuhan', 'company': u'武汉质监局', 'isAdmin': True}
    user = request.myuser
    if user.is_authenticated():
        categories = ArticleCategory.objects.all()
        locations = Area.objects.filter(level=user.area.level+1, parent=user.area)

	news = Article.objects.all().count()
	weibo = Weibo.objects.all().count()
	weixin = Weixin.objects.all().count()
	event = Topic.objects.all().count()

	news_list_number = event_list_number = 5
	weixin_list_number = weibo_list_number = 5

	news_list = []
	weixin_list = []
	event_list = []
	weibo_list = []
	news_list = Article.objects.all()[:news_list_number]
	for item in news_list:
            item = SetLogo(item)
	    setattr(item, 'hot_index', RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count())
	for i in range(event_list_number):
            event_list.append({'url': 'www.baidu.com', 'title': u'新闻', 'source': u'深度网', 'time': 53})
	weibo_data = Weibo.objects.all()[0:weibo_list_number]
	for data in weibo_data:
            data = SetLogo(data)
	    weibo_list.append({'logo': data.publisher.photo, 'id': data.id, 'title': data.title, 'name': data.author, 'time': data.pubtime, 'content': data.content})
	weixin_data = Weixin.objects.all()[0:weixin_list_number]
	for data in weixin_data:
            data = SetLogo(data)
	    weixin_list.append({'logo': data.publisher.photo, 'id': data.id, 'title': data.title, 'name': data.author, 'time': data.pubtime, 'content': data.content})
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
			'weixin_list': weixin_list,
			'weibo_list': weibo_list,
			})
    else:
        return HttpResponse(status=401)


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
            context['user'] = user
	    context['locations'] = self.get_locations(user.area)
        return render_to_response(template_path, context)
    
    def get_article_categories(self):
        return ArticleCategory.objects.all()
    
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
	weixin = [SetLogo(data) for data in Weixin.objects.filter(area=location)]
	weibo = [SetLogo(data) for data in Weibo.objects.filter(area=location)]
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
        r = RelatedData.objects.filter(uuid=news.uuid)[0]
        relateddata = list(r.weixin.all()) + list(r.weibo.all()) + list(r.articles.all())
        return self.render_to_response('news/news.html', {'article': SetLogo(news), 'relate': relateddata})


class EventView(BaseView):
    def get(self,request):
        return self.render_to_response('event/event_list.html')


class EventDetailView(BaseView):
    def get(self, request, id):
        return self.render_to_response('event/event.html')


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
        hottest = latest = [SetLogo(data) for data in Weibo.objects.order_by('-pubtime')[0:20]]
        #hottest  = latest
        return self.render_to_response('weibo/weibo_list.html', {'weibo_latest_list': latest, 'weibo_hottest_list': hottest})


class CollectionView(BaseView):
    def get(self, request):
        return self.render_to_response('user/collection.html')


class SettingsView(BaseView):
    def get(self, request):
        return self.render_to_response('user/settings.html')

def custom_view(request):
    return render_to_response('custom/custom.html')


class UserView(BaseView):
    def get(self, request):
        return slef.render_to_response('user/user.html')

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

    return render_to_response('user/login.html')

def logout_view(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('pass_id')
    response.delete_cookie('name')
    return response

def search_view(request, keyword):
    return render_to_response('search/result.html')
