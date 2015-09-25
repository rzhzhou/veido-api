# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base import sidebarUtil
from base.views import BaseTemplateView
from base.models import Topic


class EventView(BaseTemplateView):
    def get(self,request):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('event/event_list.html',{'name': sidebar_name})


class EventDetailView(BaseTemplateView):
    def get(self, request, id):
        sidebar_name = sidebarUtil(request)
        try:
            event_id = int(id)
            event = Topic.objects.get(id=event_id)
            eval_keywords_list = eval(event.keywords) if event.keywords else []
            keywords_list = [{"name": name, "number": round(number, 2)} for name, number in eval_keywords_list]
        except Topic.DoesNotExist:
            return self.render_to_response('event/event.html', {'event': '', 'weixin_list': [], 'weibo_list': []})
        user = self.request.myuser
        try:
            collection = user.collection
        except Collection.DoesNotExist:
            collection = Collection(user=user)
            collection.save(using='master')
        items = user.collection.events.all()
        iscollected = any(filter(lambda x: x.id == event.id, items))
        return self.render_to_response('event/event.html', 
            {
                'event': event,
                'keywords_list': keywords_list,
                'isCollected': iscollected,
                'name': sidebar_name
                })
