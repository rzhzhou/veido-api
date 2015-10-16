# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from observer.apps.base import sidebarUtil
from observer.apps.base.views import BaseTemplateView
from observer.apps.base.models import Topic


class EventView(BaseTemplateView):
    def get(self, request):
        sidebar_name = sidebarUtil(request)
        return self.render_to_response('event/list.html', {'name': sidebar_name})


class EventDetailView(BaseTemplateView):
    def get(self, request, id):
        sidebar_name = sidebarUtil(request)
        try:
            event_id = int(id)
            event = Topic.objects.get(id=event_id)
            eval_keywords_list = eval(event.keywords) if event.keywords else []
            keywords_list = [{"name": name, "number": "%.2f" % number} for name, number in eval_keywords_list]
        except Topic.DoesNotExist:
            return HttpResponseRedirect('/event/')
        user = self.request.myuser
        try:
            collection = user.collection
        except Collection.DoesNotExist:
            collection = Collection(user=user)
            collection.save(using='master')
        items = user.collection.events.all()
        iscollected = any(filter(lambda x: x.id == event.id, items))
        return self.render_to_response('event/detail.html', {
            'event': event,
            'keywords_list': keywords_list,
            'isCollected': iscollected,
            'name': sidebar_name})
