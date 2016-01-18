# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base.initialize import authenticate, login_required, set_logo
from observer.apps.base.views import BaseAPIView, BaseView
from observer.apps.base.models import Weibo, Area
from observer.utils.connector.redisconnector import RedisQueryApi

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
        result = self.weibo_to_json(items)
        return Response({'data': result, 'total': datas['total_number']})


class WeiboApi(BaseView):

    def get(self):
        uuids = RedisQueryApi().lrange('hotuuid', 0, -1)
        items = Weibo.objects.filter(uuid__in=uuids)
        result = self.weibo_to_json(items)[:6]
        weibo_data = self.get_info(color='warning', types='weibo', name=u'微博', link='/weibo', items=result)
        return weibo_data


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
        result = self.weibo_to_json(items)
        return Response({'data': result, 'total': datas['total_number']})
