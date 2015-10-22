# -*- coding: utf-8 -*-
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import View
from rest_framework.response import Response

from observer.apps.base import authenticate, login_required, set_logo
from observer.apps.base.views import BaseAPIView
from observer.apps.base.models import CustomKeyword


class CustomNewsView(BaseAPIView):
    def get(self, request, custom_id):
        container = self.requesthead()
        try:
            keyword = CustomKeyword.objects.get(id=int(custom_id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return HttpResponseRedirect('/custom/')

        items = keyword.custom.articles.all()
        datas = self.paging(items, settings.CUSTOM_NEWS_LIMIT, container['page'])
        result = self.news_to_json(datas['items'])
        html_string = render_to_string('news/list_tpl.html', {'news_list': result})
        return Response({'html': html_string, 'total': datas['total_number']})


class CustomWeixinView(BaseAPIView):
    def get(self, request, custom_id):
        container = self.requesthead()
        try:
            keyword = CustomKeyword.objects.get(id=int(custom_id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return HttpResponseRedirect('/weixin/')
        items = keyword.custom.weixin.all()
        datas = self.paging(items, settings.CUSTOM_WEIXIN_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weixin/list_tpl.html', {'weixin_list': items})
        return Response({'html': html_string, 'total': datas['total_number']})


class CustomWeiboView(BaseAPIView):
    def get(self, request, custom_id):
        container = self.requesthead()
        try:
            keyword = CustomKeyword.objects.get(id=int(custom_id), group=user.group)
        except CustomKeyword.DoesNotExist:
            return HttpResponseRedirect('/weibo/')

        items = keyword.custom.weibo.all()
        datas = self.paging(items, settings.CUSTOM_WEIBO_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weibo/list_tpl.html', {'weibo_list': items})
        return Response({'html': html_string, 'total': datas['total_number']})


class CustomModifyView(View):
    def save(self, user):
        count = CustomKeyword.objects.filter(group=user.group).exclude(custom__isnull=False).count()
        if count >= 5:
            return {"status": False}
        try:
            custom = CustomKeyword(newkeyword=self.keyword, group=user.group)
            custom.save(using='master')
        except IntegrityError:
            return {"status": False}
        return {"status": True}

    def remove(self, user):
        pass

    def post(self, request, action):
        try:
            self.keyword = request.POST['keyword']
        except KeyError:
            return HttpResponse(status=404)
        user = self.request.myuser
        status = {"status": False}
        if action == 'add':
            status = self.save(user)
        if action == 'remove':
            status = self.delete(user)
        return JsonResponse({'status': status['status']})
