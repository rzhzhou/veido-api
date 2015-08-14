# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from base.views import BaseTemplateView
from base.models import Topic


class EventView(BaseTemplateView):
    def get(self,request):
        return self.render_to_response('event/event_list.html')


class EventDetailView(BaseTemplateView):
    def get(self, request, id):
        try:
            event_id = int(id)
            event = Topic.objects.get(id=event_id)
            eval_keywords_list = eval(event.keywords) if event.keywords else []
            keywords_list = [{"name": name, "number": number} for name, number in eval_keywords_list]
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
        #weixin_list = [SetLogo(item) for item in event.weixin.all()][:10]
        #weibo_list = [SetLogo(item) for item in event.weibo.all()][:10]
        #for item in weibo_list:
        #    SetLogo(item)
        #    if len(item.content) < 144:
        #        setattr(item, 'short', True)
        #return self.render_to_response('event/event.html', {'event': event, 'weixin_list': weixin_list, 'weibo_list': weibo_list})
        return self.render_to_response('event/event.html', {'event': event, 'keywords_list': keywords_list, 'isCollected': iscollected})
