# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from backend.base import set_logo, sidebarUtil
from backend.base.views import BaseTemplateView
from backend.base.models import Weixin, RelatedData


class WeixinView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        hottest = [set_logo(data) for data in Weixin.objects.order_by('-pubtime')[0:20]]
        weixin = Weixin.objects.all()
        latest = self.paging(weixin, 20, 1)
        items = [set_logo(data) for data in latest['items']]
        html = self.set_css_to_weixin(items)
        return self.render_to_response('weixin/list.html', {'weixin_latest_list': latest,
                                                                   'weixin_hottest_list': hottest,
                                                                   'html': html,
                                                                   'total_page_number': latest['total_number'],
                                                                   'name': sidebar_name
                                                                   })


class WeixinDetailView(BaseTemplateView):
    def get(self, request, id):
        sidebar_name = sidebarUtil(request)
        try:
            weixin_id = int(id)
            weixin = Weixin.objects.get(id=weixin_id)
        except Weixin.DoesNotExist:
            return render_to_response('weixin/detail.html', {'article': '', 'relate': []})
        try:
            r = RelatedData.objects.filter(uuid=weixin.uuid)[0]
            relateddata = list(r.weixin.all()) + list(r.weibo.all()) + list(r.articles.all())
        except IndexError:
            relateddata = []
        return self.render_to_response('weixin/detail.html', {'article': set_logo(weixin),
                                                                'relate': relateddata,
                                                                'name': sidebar_name
                                                                })

