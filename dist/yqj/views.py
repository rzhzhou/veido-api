#coding=utf-8
import datetime

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

def index_view(request):
    user = {'name': 'wuhan', 'company': u'武汉质监局', 'isAdmin': True}
    categories = [{'name': u'微博', 'id': '98672345'}, {'name': u'文章', 'id': '52345609'}]
    locations = [{'name': u'武昌', 'id': '98672345'}, {'name': u'汉口', 'id': '52345609'}]
    
    news = {'number': 67}
    weibo = {'number': 167}
    weixin = {'number': 53}
    event = {'number': 29}
    
    logo_path = '/static/img/64.gif'
    #weixin_list_number = news_list_number = event_list_number = weibo_list_number = 5
    news_list_number = event_list_number = 5
    weixin_list_number = weibo_list_number = 5

    news_list = []
    weixin_list = []
    event_list = []
    weibo_list = []
    for i in range(news_list_number):
        news_list.append({'url': 'www.baidu.com', 'title': u'新闻', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)})

    for i in range(event_list_number):
        event_list.append({'url': 'www.baidu.com', 'title': u'新闻', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)})
                 
    for i in range(weixin_list_number):
        weibo_list.append({'logo': logo_path, 'url': 'www.baidu.com', 'title': u'微信', 'name': u'深度网', 'time': datetime.datetime(2014,6,8), 'content': u'确定起重机的方案依据有：被吊运物体的重量；重心位置及绑扎；作业现场环境'})

    for i in range(weibo_list_number):
        weixin_list.append({'logo': logo_path, 'url': 'www.baidu.com', 'title': u'微博', 'name': u'深度网', 'time': datetime.datetime(2014,6,8), 'content': u'确定起重机的方案依据有：被吊运物体的重量；重心位置及绑扎；作业现场环境'})
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

def category_view(request, ctg_id):
    category  = {'name': u'质量检测', 'url': 'http://www.baidu.com'}
    return render_to_response('category/category.html', {'category': category})

def location_view(request, location_id):
    location = {'name': u'武昌', 'url': 'http://www.baidu.com'}
    return render_to_response("location/location.html", {'location': location})
    
def person_view(request, person_id):
    return HttpResponse('person')

def login_view(request):
    return render_to_response('user/login.html')

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
    return render_to_response('news/news.html')

def event_view(request):
    return render_to_response('event/event_list.html')

def event_detail_view(request, id):
    return render_to_response('event/event.html')

def weixin_view(request):
    return render_to_response('weixin/weixin_list.html')

def weixin_detail_view(request, id):
    return render_to_response('weixin/weixin.html')

def weibo_view(request):
    return render_to_response('weibo/weibo_list.html')

def collection_view(request):
    return render_to_response('user/collection.html')

def setting_view(request):
    return render_to_response('user/setting.html')

def custom_view(request):
    return render_to_response('custom/custom.html')

def user_view(request):
    return render_to_response('user/user.html')

