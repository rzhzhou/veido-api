# -*- coding: utf-8 -*-
from django.views.generic import View
from rest_framework.decorators import api_view
from django.db import models, connection, IntegrityError
from rest_framework.response import Response
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from base.models import Article, Category, RelatedData, ArticleCollection,\
    Collection
from news.views_api import ArticleTableView
from event.views_api import EventTableView
from base.views import BaseAPIView


class CollecModifyView(View):
    def save(self, item):
        data = {self.related_field: item, 'collection': self.collection}
        if isinstance(item, Article):
            try:
                category = item.categorys.all()[0]
            except IndexError:
                category = Category.objects.get(name='其他')
            data['category'] =  category.name
        try:
            collection_item = self.get_related_model().objects.create(**data)
            collection_item.save(using='master')
        except IntegrityError:
             pass

    def _delete(self, item):
        try:
            collectitem = self.get_collection_model().objects.get(**{self.related_field: item, 'collection': self.collection})
            collectitem.delete(using='master')
        except self.get_collection_model.DoesNotExist:
            pass

    @property
    def related_field(self):
        return self.data_type.lower()

    def get_related_model(self):
        return models.get_model('base', self.data_type.capitalize() + 'Collection')

    def _create_collection(self):
        #add a collection to the user
        try:
            _collection = self.request.myuser.collection
        except ObjectDoesNotExist:
            _collection = Collection(user=user)
            _collection.save(using='master')
        return _collection

    @property
    def collection(self):
        return self._create_collection()

    def get_model(self):
        return models.get_model('base', self.data_type.capitalize())

    def get_collection_model(self):
        return models.get_model('base', self.data_type.capitalize() + 'Collection')

    def prepare(self,request):
        data = request.read()
        data_type = data.split('&')[0].split('=')[1]
        id = data.split('&')[1].split('=')[1]
        try:
            self.data_type = data_type
            pk = id
        except KeyError:
            return HttpResponse(status=404)

        related_fields = ['article', 'topic']
        if self.data_type not in related_fields:
            return HttpResponse(status=400)
        try:
            model = self.get_model()
            item = model.objects.get(id=pk)
        except model.DoesNotExist:
            return HttpResponse(status=404)
        return item

    def put(self, request):
        self.save(self.prepare(request))
        return JsonResponse({'status': True})

    def delete(self, request):
        self._delete(self.prepare(request))
        return JsonResponse({'status': True})


class CollectView(BaseAPIView):
    def article_html(self, item):
        url = u'/news/%s' % item.id
        view = ArticleTableView(self.request)
        title = view.title_html(url, item.title, item.id, 'article')
        try:
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
        except:
            hot_index =0
        line = [title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
        #line = [view.collected_html(item), title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
        return line

    def topic_html(self, item):
        url = u'/event/%s' % item.id
        view = EventTableView(self.request)
        title = view.title_html(url, item.title, item.id, 'topic')
        hot_index = item.articles.all().count() + item.weixin.all().count() + item.weibo.all().count()
        time = item.articles.all().order_by('-pubtime')
        if time:
            pubtime = time[0].pubtime
        else:
            pubtime = timezone.now()
        one_record = [title, item.source, item.area.name, pubtime.date(), hot_index]
        return one_record

    def get(self, request, table_type):
        page = int(request.GET['page'])
        try:
            self.collection = request.myuser.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save(using='master')

        if table_type == 'news':
            view = ArticleTableView(self.request)
            items = self.collection.articles.all()
            datas = self.paging(items, settings.NEWS_PAGE_LIMIT, page)
            result = self.news_to_json(datas['items'])
            html_string = render_to_string('news/list_tpl.html', {'news_list':  result})
        elif table_type == 'event':
            view = EventTableView(self.request)
            items = self.collection.events.all()
            datas = self.paging(items, settings.EVENT_PAGE_LIMIT, page)
            result = self.event_to_json(datas['items'])
            html_string = render_to_string('event/list_tpl.html', {'event_list':  result})
        else:
            result = []
            datas = {'taotal_number': 0}
        return Response({'total': datas['total_number'], 'html': html_string})
