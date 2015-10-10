# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.conf import settings

from observer.apps.base.views import BaseAPIView
from observer.apps.base.models import Weixin, Area
from observer.apps.base import authenticate, login_required, set_logo

class WeixinView(BaseAPIView):
    HOME_PAGE_LIMIT = 6
    def get(self, request):
        container = self.requestContainer(sort='hot', limit_list=settings.WEIXIN_TABLE_LIMIT,
            limit=self.HOME_PAGE_LIMIT)
        if container['sort'] == 'new':
            datas = self.paging(Weixin.objects.all(), container['limit'], container['page'])
        else: # hot
            datas = self.paging(Weixin.objects.all(), container['limit'], container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weixin/%s_tpl.html' % container['type'], {'weixin_list':  items})
        return Response({'html': html_string, 'total': datas['total_number']})


class LocationWeixinView(BaseAPIView):
    def get(self, request, id):
        container = self.requestContainer()
        try:
            id = int(id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'html': '', 'total': 0})
        items = Weixin.objects.filter(area=area)
        datas = self.paging(items, settings.LOCATION_WEIXIN_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        html_string = render_to_string('weixin/list_tpl.html', {'weixin_list': items})
        return Response({'html': html_string, 'total': datas['total_number']})