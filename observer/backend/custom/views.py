# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base import sidebarUtil
from base.views import BaseTemplateView
from base.models import Article, CustomKeyword

class CustomView(BaseTemplateView):
    custom_list_num = 5

    def get(self, request):
        sidebar_name = sidebarUtil(request)
        user = self.request.myuser
        newkeyword_list = CustomKeyword.objects.filter(group=user.group).exclude(custom__isnull=False)
        searchkeyword_list = CustomKeyword.objects.filter(group=user.group).exclude(custom__isnull=True)
        keyword_list = []
        for keyword in searchkeyword_list:
            setattr(keyword, 'name', keyword.newkeyword)
            setattr(keyword, 'news_list', keyword.custom.articles.all()[:self.custom_list_num])
            keyword_list.append(keyword)
        return self.render_to_response('custom/list.html', {'custom_list': keyword_list, 'keyword_list': newkeyword_list, 'name': sidebar_name})

    def get_news(self, keyword):
        return Article.objects.raw(u"SELECT * FROM article WHERE MATCH (content, title) AGAINST ('%s') LIMIT %s" % (keyword, self.custom_list_num))


class CustomDetailView(BaseTemplateView):

    def get(self, request, id):
        sidebar_name = sidebarUtil(request)
        user = request.myuser
        try:
            custom = CustomKeyword.objects.get(id=int(id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return self.render_to_response('custom/detail.html', {'newkeyword': u'', 'name': sidebar_name})
        return self.render_to_response('custom/detail.html', {'customkeyword': custom.newkeyword, 'name': sidebar_name})
