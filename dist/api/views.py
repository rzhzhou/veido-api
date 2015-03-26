#coding=utf-8

import os
import datetime
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from yqj.models import (Article, Area, Weixin, Weibo, Topic, RelatedData, ArticleCategory,
                            save_user, Collection, Topic, hash_password, User)
from serializers import ArticleSerializer
from yqj import authenticate, login_required

def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)
    
    user = authenticate(username, password)
    if user.is_authenticated():
        response = JsonResponse({'status': True})
        response.set_cookie('pass_id', user.id)
        response.set_cookie('name', user.username)
        return response
    else:
        return JsonResponse({'status': False})

@api_view(['POST'])
def registe_view(request):
    print request.method

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)
    users = User.objects.filter(username=username)
    if users:
        return JsonResponse({'status': False})
    try:
        area = Area.objects.get(name=u'武汉')
        save_user(username, password, area)
    except :
        return JsonResponse({'status': False})

    return JsonResponse({'status': True})

    
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class TableAPIView(APIView):
    COLLECTED_TEXT = u'<i class="fa fa-star" data-toggle="tooltip", data-placement="right" title="取消收藏">'
    NO_COLLECTED_TEXT = u'<i class="fa fa-star-o" data-toggle="tooltip", data-placement="right" title="添加收藏">'

    LIMIT_NUMBER = 300
    def __init__(self, request=None):
        self.request = request

    def collected_html(self, item):
        items = self.collected_items()
        return self.COLLECTED_TEXT if self.isIn(item, items) else self.NO_COLLECTED_TEXT

    def isIn(self, item, items):
        if isinstance(item, models.Model):
            item_id = item.id
        else:
            item_id = item['id']

        if item_id is None:
            raise TypeError('item should has id atrribute or id key')
        
        return any(filter(lambda x: x.id == item_id, items))

    def collected_items(self):
        #return []
        user = self.request.myuser
        return user.collection.articles.all()

    def title_html(self, *args):
        title_format = u'<a href="{0}" title="{1}" target="_blank" data-id="{2}" data-type="{3}">{1}</a>'
        return title_format.format(*args)

def get_date_from_iso(datetime_str):
    #return datetime.datetime.strptime("2008-09-03T20:56:35.450686Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        
class ArticleTableView(TableAPIView):
    def get(self, request, id):
        try:
            category = ArticleCategory.objects.get(id=id)
        except ArticleCategory.DoesNotExist:
            return Response({'news': []})
        
        result = []
        articles = category.articles.all()[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(articles, many=True)

        for item in articles:
            collected_html = self.collected_html(item)
            #pubtime = get_date_from_iso(item.pubtime)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)

        return Response({'news': result})

class NewsTableView(TableAPIView):
    def get(self, request):
        result = []
        news = Article.objects.all()[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(news, many=True)

        for item in news:
            collected_html = self.collected_html(item)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)
        
        return Response({"news": result})


class LocationTableView(TableAPIView):
    def get(self, request, location_id):
        try:
            id = int(location_id)
            area = Area.objects.get(id=id)
        except Area.DoesNotExist:
            return Response({'news': []})
        result = []
        news = Article.objects.filter(area=area)[:self.LIMIT_NUMBER]
        serializer = ArticleSerializer(news, many=True)

        for item in news:
            collected_html = self.collected_html(item)
            #pubtime = get_date_from_iso(item.item)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title,item.id, 'article')
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)
        
        return Response({"news": result})


class EventTableView(TableAPIView):
    def collected_items(self):
        user = self.request.myuser
        return user.collection.events.all()

    def get(self, request):
        result = []
        event = Topic.objects.all()[:self.LIMIT_NUMBER]
        for item in event:
            collected_html = self.collected_html(item)
            url = u'/event/%s' % item.id
            title = self.title_html(url, item.title, item.id, 'topic')
            hot_index = item.articles.all().count() + item.weixin.all().count() + item.weibo.all().count()
            time = item.articles.all().order_by('-pubtime')
            if time:
                pubtime = time[0].pubtime
            else:
                pubtime = datetime.datetime.now()
            one_record = [collected_html, title, item.source, item.area.name, pubtime.date(), hot_index]
            result.append(one_record)
        return Response({"event": result})


class EventDetailTableView(TableAPIView):
    def get(self, request, id):
        try:
            event = Topic.objects.get(id=int(id))
        except Topic.DoesNotExist:
            return Response({'news': ''})
        news = event.articles.all()
        result = []
        for item in news:
            collected_html = self.collected_html(item)
            url = u'/news/%s' % item.id
            title = self.title_html(url, item.title, item.id, 'article')
            hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
            one_record = [collected_html, title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
            result.append(one_record)
        return Response({'news': result})


class CollectView(APIView):
    def article_html(self, item):
        url = u'/news/%s' % item.id
        view = ArticleTableView(self.request)
        title = view.title_html(url, item.title, item.id, 'article')
        hot_index = RelatedData.objects.filter(uuid=item.uuid)[0].articles.all().count()
        line = [view.collected_html(item), title, item.publisher.publisher, item.area.name, item.pubtime.date(), hot_index]
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
            pubtime = datetime.datetime.now()
        one_record = [view.collected_html(item), title, item.source, item.area.name, pubtime.date(), hot_index]
        return one_record 

    def get(self, request):
        try:
            self.collection = request.myuser.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save()
        news = [self.article_html(item) for item in self.collection.articles.all()]
        topic = [self.topic_html(item) for item in self.collection.events.all()]

        return Response({'news': news, 'event': topic}) 


class CollecModifyView(View):
    def save(self, item):
        data = {self.related_field: item, 'collection': self.collection}
        if isinstance(item, Article):
            category = item.categorys.all()[0]
            data['category'] =  category.name
        try:
            collection_item = self.get_related_model().objects.create(**data)
            collection_item.save()
        except IntegrityError:
             pass
        
    
    def delete(self, item):
        try:
            collectitem = self.get_collection_model().objects.get(**{self.related_field: item, 'collection': self.collection})
            collectitem.delete()
        except self.get_collection_model.DoesNotExist:
            pass
    
    @property
    def related_field(self):
        return self.data_type.lower()   
   
    def get_related_model(self):
        return models.get_model('yqj', self.data_type.capitalize() + 'Collection')
 
    def _create_collection(self):
        #add a collection to the user
        try:
            _collection = self.request.myuser.collection
        except ObjectDoesNotExist:
            _collection = Collection(user=user)
            _collection.save()
        return _collection

    @property
    def collection(self):
        return self._create_collection()

    def get_model(self):
        return models.get_model('yqj', self.data_type.capitalize())

    def get_collection_model(self):
        return models.get_model('yqj', self.data_type.capitalize() + 'Collection')
   
    def post(self, request, action, *args, **kwargs):
        try:
            print request.POST['type'], request.POST['id']
            self.data_type = request.POST['type']
            pk = request.POST['id']
        except KeyError:
            return HttpResponse(status=404)

        related_fields = ['article', 'topic']
        if self.data_type not in related_fields:
            return HttpResponse(status=400)

        #find the model and get instance
        try:
            model = self.get_model()
            item = model.objects.get(id=pk)
        except model.DoesNotExist:
            return HttpResponse(status=404)

        if action == 'remove':
            self.delete(item)
        elif action == 'add':
            self.save(item)
        return JsonResponse({'status': True})

@login_required
def upload_image(request):
    user = request.myuser
    try:
        f = request.FILES['image']
    except KeyError:
        return HttpResponse(status=400)

    media_path = settings.MEDIA_ROOT
    filename = str(user.id) + os.path.splitext(f.name)[1]

    try:
        new_file = open(os.path.join(media_path, filename), 'w')
        for chunk in f.chunks():
            new_file.write(chunk)
    except OSError:
        return HttpResponseRedirect('/settings/')
    finally:
        new_file.close()
        
    return HttpResponseRedirect('/settings/')

@login_required
def change_passwd(request):
    user = request.myuser
    try:
        old_passwd = request.POST['oldPassword']
        new_passwd = request.POST['newPassword']
        username = request.POST['username']
    except KeyError:
        return HttpResponse(status=400)
    if username != user.username:
        return JsonResponse({'status': False})

    coded = hash_password(old_passwd, user.salt)
    #authencate success
    if user.password == coded:
        user.password = hash_password(new_passwd, user.salt)
        user.save()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})

@login_required
def reset_passwd(request):
    try:
        reseted_user_ids = request.POST['id'].split(',')
        reseted_id_list = map(lambda x: int(x), reseted_user_ids)
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    admin_user = request.myuser
    group_users = admin_user.group.user_set.all()
    group_user_ids = list(map(lambda x: x.id, group_users))

    for user_id in reseted_id_list:
        if user_id in group_user_ids:
            user = User.objects.get(id=user_id)
            user.password = hash_password('123456', user.salt) 
            user.save()
    return JsonResponse({'status': True})

@login_required
def delete_user_view(request):
    try:
        reseted_user_ids = request.POST['id'].split(',')
        reseted_id_list = map(lambda x: int(x), reseted_user_ids)
    except (KeyError, ValueError):
        return HttpResponse(status=400)

    admin_user = request.myuser
    group_users = admin_user.group.user_set.all()
    group_user_ids = list(map(lambda x: x.id, group_users))

    for user_id in reseted_id_list:
        if user_id in group_user_ids and user_id != admin_user.id:
            delete_user = User.objects.get(id=user_id)
            delete_user.delete()
    return JsonResponse({'status': True})

@login_required
def add_user_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400)

    myuser = request.myuser
    if not myuser.isAdmin:
        return HttpResponse(status=401)

    save_user(username, password, myuser.area, myuser.group)
    return JsonResponse({'status': True})
