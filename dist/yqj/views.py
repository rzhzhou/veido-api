#coding=utf-8
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
    return render_to_response("dashboard/dashboard.html", {'user': user, 'categories': categories, 'locations': locations, 'news': news, 'weibo': weibo, 'weixin': weixin, 'event': event})

def category_view(request, ctg_id):
    return render_to_response('category/category.html')

def location_view(request, location_id):
    return render_to_response("location/location.html")
    
def person_view(request, person_id):
    return HttpResponse('person')

def login_view(request):
    return render_to_response('user/login.html')
