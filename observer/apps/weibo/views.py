# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render_to_response

from observer.apps.base import set_logo, sidebarUtil
from observer.apps.base.views import BaseTemplateView
from observer.apps.base.models import Weibo
from observer.apps.yqj.redisconnect import RedisQueryApi


class WeiboView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        latest = [set_logo(data) for data in Weibo.objects.order_by('-pubtime')[0:20]]
        for item in latest:
            if len(item.content) < 144:
                setattr(item, 'short', True)
        hottest = [eval(item) for item in RedisQueryApi().lrange('sort_weibohot', 0, -1)[:20]]
        for data in hottest:
            data['pubtime'] = datetime.fromtimestamp(data['pubtime'])
            if data['photo'] == 'kong':
                data['photo'] = u'http://tp2.sinaimg.cn/3557640017/180/40054587155/1'
            if len(data['content']) < 144:
                data['short'] = True
        return self.render_to_response('weibo/list.html', {
            'weibo_latest_list': latest,
            'weibo_hottest_list': hottest,
            'name': sidebar_name})
