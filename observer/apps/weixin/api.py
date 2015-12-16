# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.response import Response

from observer.apps.base.initialize import authenticate, login_required, set_logo
from observer.apps.base.views import BaseAPIView, BaseView
from observer.apps.base.models import Weixin, Area, RelatedData


class WeixinView(BaseAPIView):
    HOME_PAGE_LIMIT = 6

    def get(self, request):
        container = self.requesthead(
            sort='hot',
            limit_list=settings.WEIXIN_TABLE_LIMIT,
            limit=self.HOME_PAGE_LIMIT)
        if container['sort'] == 'new':
            datas = self.paging(Weixin.objects.all(), container['limit'], container['page'])
        else:  # hot
            datas = self.paging(Weixin.objects.all(), container['limit'], container['page'])
        items = [set_logo(data) for data in datas['items']]
        result = self.weixin_to_json(items)
        return Response({'data': result, 'total': datas['total_number']})


class WeixinApi(BaseView):

    def get(self):
        datas = Weixin.objects.all()[:6]
        items = [set_logo(data) for data in datas]
        result = self.weixin_to_json(items)
        weixin_data = self.get_info(color='success', types='weixin', name=u'微信', link='/weixin', items=result)
        return weixin_data


class LocationWeixinView(BaseAPIView):
    def get(self, request, id):
        container = self.requesthead()
        try:
            id = int(id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'html': '', 'total': 0})
        items = Weixin.objects.filter(area=area)
        datas = self.paging(items, settings.LOCATION_WEIXIN_LIMIT, container['page'])
        items = [set_logo(data) for data in datas['items']]
        result = self.weixin_to_json(items)
        return Response({'data': result, 'total': datas['total_number']})


class WeixinDetailView(BaseAPIView):

    def get(self, request, id):
        try:
            weixin_id = int(id)
            weixin = Weixin.objects.filter(id=weixin_id)
            result = self.weixin_to_json(weixin)[0]
        except:
            return Response({'data': {}, 'relate': []})
        try:
            r = RelatedData.objects.filter(uuid=weixin[0].uuid)[0]
            weinxin_list = self.weixin_to_json(r.weixin.all())
            weibo_list = self.weibo_to_json(r.weibo.all())
            article_list = self.news_to_json(r.articles.all())
            relateddata = weinxin_list + weibo_list + article_list
        except IndexError:
            relateddata = []
        return Response( {'article': result, 'relate': relateddata})