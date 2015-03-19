#coding=utf-8
import datetime

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from yqj.models import Article, Weixin, Weibo, RelatedData, ArticleCategory, Area, Topic

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

def category_view(request, ctg_id):
    category  = {'name': u'质量检测', 'url': 'http://www.baidu.com'}
    return render_to_response('category/category.html', {'category': category})

def location_view(request, location_id):
    location = Area.objects.get(id=int(location_id))
    weixin = [SetLogo(data) for data in Weixin.objects.filter(area=location)]
    weibo = [SetLogo(data) for data in Weibo.objects.filter(area=location)]
    return render_to_response("location/location.html", {'location': location, 'weixin_list': weixin, 'weibo_list': weibo})

def person_view(request, person_id):
    return HttpResponse('person')


def news_view(request):
    news_list_data = []
    for i in range(10):
        news_list_data.append({'url': u'www.baidu.com',
                          'title': u'质监免费检测珠宝饰品',
                          'source': u'深度网',
                          'pubtime': datetime.datetime(2014,6,8),
                          'area': u'武昌'})
    return render_to_response('news/news_list.html', {'news_list_data': news_list_data})

def news_detail_view(request, news_id):
    try:
        news_id = int(news_id)
        news = Article.objects.get(id=news_id)
    except ValueError:
        return HttpResponse(status=400)
    except Article.DoesNotExist:
        return HttpResponse(status=404)
    r = RelatedData.objects.filter(uuid=news.uuid)[0]
    relateddata = list(r.weixin.all()) + list(r.weibo.all()) + list(r.articles.all())
    return render_to_response('news/news.html', {'article': SetLogo(news), 'relate': relateddata})

def event_view(request):
    return render_to_response('event/event_list.html')

def event_detail_view(request, id):
    return render_to_response('event/event.html')

def weixin_view(request):
    latest = [SetLogo(data) for data in Weixin.objects.order_by('-pubtime')[0:20]]
    hottest = latest
    return render_to_response('weixin/weixin_list.html', {'weixin_latest_list': latest, 'weixin_hottest_list': hottest})

def weixin_detail_view(request, id):
    try:
        weixin_id = int(id)
        weixin = Weixin.objects.get(id=weixin_id)
    except ValueError:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    except Weixin.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    r = RelatedData.objects.filter(uuid=weixin.uuid)[0]
    relateddata = list(r.weixin.all()) + list(r.weibo.all()) + list(r.articles.all())
    return render_to_response('weixin/weixin.html', {'article': SetLogo(weixin), 'relate': relateddata})

def weibo_view(request):
    hottest = latest = [SetLogo(data) for data in Weibo.objects.order_by('-pubtime')[0:20]]
    #hottest  = latest
    return render_to_response('weibo/weibo_list.html', {'weibo_latest_list': latest, 'weibo_hottest_list': hottest})

def collection_view(request):
    return render_to_response('user/collection.html')

def settings_view(request):
    return render_to_response('user/settings.html')

def custom_view(request):
    return render_to_response('custom/custom.html')

def user_view(request):
    return render_to_response('user/user.html')

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
