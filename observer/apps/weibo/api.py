# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base import authenticate, login_required, set_logo
from observer.apps.base.views import BaseAPIView
from observer.apps.base.models import Weibo, Area


class WeiboView(BaseAPIView):
    HOME_PAGE_LIMIT = 6

    def get(self, request):
        container = self.requesthead(
            sort='hot', limit_list=settings.WEIBO_TABLE_LIMIT, limit=self.HOME_PAGE_LIMIT)
        if container['sort'] == 'new':
            datas = self.paging(Weibo.objects.all(), container['limit'], container['page'])
        else:
            datas = self.pagingfromredis(Weibo, container['limit'], container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weibo/%s_tpl.html' % container['type'], {
            'weibo_list': items})
        return Response({'html': html_string, 'total': datas['total_number']})


class LocationWeiboView(BaseAPIView):
    def get(self, request, id):
        container = self.requesthead()
        try:
            id = int(id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'html': '', 'total': 0})
        items = Weibo.objects.filter(area=area)
        datas = self.paging(items, settings.LOCATION_WEIBO_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weibo/list_tpl.html', {'weibo_list': items})
        return Response({'html': html_string, 'total': datas['total_number']})
