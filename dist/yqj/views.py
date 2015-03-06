#coding=utf-8
import datetime

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

def index_view(request):
    user = {'name': 'wuhan', 'company': u'武汉质监局'}
    categories = [{'name': u'微博', 'id': '98672345'}, {'name': u'文章', 'id': '52345609'}]
    locations = [{'name': u'武昌', 'id': '98672345'}, {'name': u'汉口', 'id': '52345609'}]
    
    news = {'number': 67}
    weibo = {'number': 167}
    weixin = {'number': 53}
    event = {'number': 29}
    
    news_list = [
                 {'url': 'www.baidu.com', 'title': u'新闻一', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)},
                 {'url': 'www.baidu.com', 'title': u'新闻二', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)},
                 {'url': 'www.baidu.com', 'title': u'新闻三', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)},
                ]
    event_list = [
                 {'url': 'www.baidu.com', 'title': u'新闻一', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)},
                 {'url': 'www.baidu.com', 'title': u'新闻二', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)},
                 {'url': 'www.baidu.com', 'title': u'新闻三', 'source': u'深度网', 'time': datetime.datetime(2014,6,8)},
                ]
    weixin_list = [
                    {'url': 'www.baidu.com', 'title': u'微信一', 'name': u'深度网', 'time': datetime.datetime(2014,6,8)},
                    {'url': 'www.baidu.com', 'title': u'微信二', 'name': u'深度网', 'time': datetime.datetime(2014,6,8)},
                    {'url': 'www.baidu.com', 'title': u'微信三', 'name': u'深度网', 'time': datetime.datetime(2014,6,8)},
                ]
    weibo_list = [
                    {'logo': 'http://placehold.it/64x64', 'url': 'www.baidu.com', 'title': u'微信一', 'name': u'深度网', 'time': datetime.datetime(2014,6,8), 'content': u'确定起重机的方案依据有：被吊运物体的重量；重心位置及绑扎；作业现场环境'},
                    {'logo': 'http://placehold.it/64x64','url': 'www.baidu.com', 'title': u'微信二', 'name': u'深度网', 'time': datetime.datetime(2014,6,8), 'content': u'确定起重机的方案依据有：被吊运物体的重量；重心位置及绑扎；作业现场环境'},
                    {'logo': 'http://placehold.it/64x64','url': 'www.baidu.com', 'title': u'微信三', 'name': u'深度网', 'time': datetime.datetime(2014,6,8), 'content': u'确定起重机的方案依据有：被吊运物体的重量；重心位置及绑扎；作业现场环境'},
                ]
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
    return render_to_response('category/category.html')

def location_view(request, location_id):
    return render_to_response("location/location.html")
    
def person_view(request, person_id):
    return HttpResponse('person')

def login_view(request):
    return render_to_response('user/login.html')
