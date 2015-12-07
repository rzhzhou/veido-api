# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.db.models import Count, Q
from django.shortcuts import render_to_response
from django.views.generic import View
from rest_framework.views import APIView

from observer.apps.base import login_required, get_user_image, sidebarUtil
from observer.apps.base.models import Area, Category, RelatedData, Weibo
from observer.utils.connector.redisconnector import RedisQueryApi


class LoginRequiredMixin(object):
    ALLOWED_METHOD = ['GET']

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class BaseView(View):
    def get_info(self, title='', color=None, types=None, name=None, items=None, link=None):
        data = {
        'title': title,
        'color': color,
        'type': types,
        'name': name,
        'items': items,
        'link': link
        }
        return data

    def paging(self, items, limit, page):
        paginator = Paginator(items, limit)
        try:
            items = paginator.page(page)  # 获取某页对应的记录
        except PageNotAnInteger:
            items = paginator.page(1)  # 如果页码不是个整数 取第一页的记录
        except EmptyPage:
            items = paginator.page(paginator.num_pages)  # 如果页码太大，没有相应的记录 取最后一页的记录

        return {'items': items, 'total_number': paginator.num_pages}

    def news_to_json(self, items):
        result = []
        relateddata_count = RelatedData.objects.filter(
            uuid__in=[obj.uuid for obj in items]).annotate(Count('articles', distinct=True))
        hots = {r.uuid: r.articles__count for r in relateddata_count}

        for data in items:
            item = {}
            item['id'] = data.id
            item['url'] = data.url
            item['title'] = data.title
            item['author'] = data.author
            item['source'] = data.source
            item['content'] = data.content
            item['publisher'] = data.publisher.publisher
            item['location'] = data.area.name
            pubtime = data.pubtime
            if pubtime.tzinfo == pytz.utc:
                item['time'] = pubtime.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d')
            else:
                item['time'] = data.pubtime.strftime('%Y-%m-%d')
            try:
                item['hot'] = hots[data.uuid]
            except IndexError:
                item['hot'] = 0
            result.append(item)
        return result

    def inspection_to_json(self, items):
        result = []
        for data in items:
            item = {}
            item['id'] = data.id
            item['url'] = data.url
            item['event'] = data.name
            item['source'] = data.source
            item['category'] = data.product
            item['quality'] = str(int(data.qualitied * 100)) + "%"
            pubtime = data.pubtime
            if pubtime.tzinfo == pytz.utc:
                item['time'] = pubtime.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d')
            else:
                item['time'] = data.pubtime.strftime('%Y-%m-%d')
            result.append(item)
        return result

    def event_to_json(self, items):
        result = []
        for data in items:
            item = {}
            item['title'] = data.title
            item['id'] = data.id
            item['source'] = data.source
            item['location'] = data.area.name
            item['time'] = data.pubtime.date().strftime('%Y-%m-%d')
            item['hot'] = data.articles.count() + data.weixin.count() + data.weibo.count()
            result.append(item)

        results = sorted(result, key=lambda item: item['time'], reverse=True)

        return results

    def weixin_to_json(self, items):
        result = []
        for data in items:
            item = {}
            item['id'] = data.id
            item['url'] = data.url
            item['author'] = data.publisher.publisher
            item['source'] = data.source
            item['title'] = data.title
            item['photo'] = data.publisher.photo
            item['count'] = data.readnum
            item['likes'] = data.likenum
            item['content'] = data.content
            pubtime = data.pubtime
            if pubtime.tzinfo == pytz.utc:
                item['time'] = pubtime.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H-%M-%S')
            else:
                item['time'] = data.pubtime.strftime('%Y-%m-%d %H-%M-%S')
            result.append(item)
        return result

    def weibo_to_json(self, items):
        result = []
        for data in items:
            item = {}
            item['id'] = data.id
            item['url'] = data.url
            item['author'] = data.publisher.publisher
            item['title'] = data.title
            item['photo'] = data.publisher.photo
            item['likes'] = data.attitudes_count
            item['comments'] = data.comments_count
            item['reprints'] = data.reposts_count
            pubtime = data.pubtime
            if pubtime.tzinfo == pytz.utc:
                item['time'] = pubtime.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d %H-%M-%S')
            else:
                item['time'] = data.pubtime.strftime('%Y-%m-%d %H-%M-%S')
            result.append(item)
        return result

    def set_css_to_weixin(self, items):
        html = ""
        count = u'0'
        for item in items:
            html += """<li class="media">"""
            html += """<div class="media-left">"""
            html += u'<img class="media-object" src="%s" alt="%s">' % (item.publisher.photo, item.publisher.publisher)
            html += """</div>
                       <div class="media-body"> """
            html += u'<h4 class="media-heading">%s</h4>' % (item.publisher.publisher)
            html += u'<p><a href="/weixin/%s/" target="_blank">%s</a></p>' % (item.id, item.title)
            html += """<div class="media-meta">
                       <div class="info pull-right">"""
            html += u'<span>阅读 %s</span>' % count
            html += u'<span><i class="fa fa-thumbs-o-up"></i> %s</span>' % count
            html += """</div>"""
            html += u'<div class="time pull-left">%s</div>' % item.pubtime.strftime('%Y-%m-%d %H:%M')
            html += """</div></div></li>"""
        return html

    def set_css_to_weibo(self, items):
        html = ""
        count = u'0'
        for item in items:
            html += """<li class="media">"""
            html += """<div class="media-left">"""
            html += u'<img class="media-object" src="%s" alt="%s">' % (item.publisher.photo, item.publisher.publisher)
            html += """</div>
                       <div class="media-body"> """
            html += u'<h4 class="media-heading">%s</h4>' % (item.publisher.publisher)
            if len(item.content) < 200:
                html += u'<p>%s</p>' % (item.content)
            else:
                html += u'<p><a href="%s" target="_blank">%s</a></p>' % (item.url, item.title)
            html += """<div class="media-meta">
                       <div class="info pull-right">"""
            html += u'<span>转载 %s</span>' % count
            html += u'<span>评论 %s</span>' % count
            html += u'<span><i class="fa fa-thumbs-o-up"></i> %s</span>' % count
            html += """</div>"""
            html += u'<div class="time pull-left">%s</div>' % item.pubtime.strftime('%Y-%m-%d %H:%M')
            html += """</div></div></li>"""
        return html


class BaseTemplateView(BaseView):
    INCLUDE_SIDEBAR = True
    INCLUDE_USER = True

    def __init__(self, request=None):
        self.request = request

    def render_to_response(self, template_path, context={}):
        if self.INCLUDE_SIDEBAR:
            categories = self.get_article_categories()
            # for ctg in categories:
            #    ctg.id = encrypt(ctg.id)
            context['categories'] = categories
            context['industries'] = [{'id': 0, 'name': u'综合'}]

        if self.INCLUDE_USER:
            user = self.request.myuser
            user.company = user.group.company
            context['user'] = user

        context['user_image'] = get_user_image(user)
        context['locations'] = self.get_locations(user.area)
        return render_to_response(template_path, context)

    def get_article_categories(self):
        business = sidebarUtil(self.request)['business']
        categories = Category.objects.filter(name__in=business)
        return categories

    def get_locations(self, area):
        if area.id == 4:
            return []
        return Area.objects.filter(parent=area, level=area.level + 1)


class BaseAPIView(BaseView, APIView):
    COLLECTED_TEXT = u'<i class="fa fa-star" data-toggle="tooltip", data-placement="right" title="取消收藏">'
    NO_COLLECTED_TEXT = u'<i class="fa fa-star-o" data-toggle="tooltip", data-placement="right" title="添加收藏">'

    def __init__(self, request=None):
        self.request = request

    def collected_html(self, item):
        items = self.collected
        return self.COLLECTED_TEXT if self.isIn(item, items) else self.NO_COLLECTED_TEXT

    def isIn(self, item, items):
        if isinstance(item, models.Model):
            item_id = item.id
        else:
            item_id = item['id']

        if item_id is None:
            raise TypeError('item should has id atrribute or id key')

        return any(filter(lambda x: x.id == item_id, items))

    @property
    def collected(self):
        if getattr(self, '_collected', None) is None:
            self._collected = self.collected_items()
        return self._collected

    def collected_items(self):
        user = self.request.myuser
        try:
            self.collection = user.collection
        except Collection.DoesNotExist:
            self.collection = Collection(user=self.request.myuser)
            self.collection.save(using='master')
        return user.collection.articles.all()

    def title_html(self, *args):
        title_format = u'<a href="{0}" title="{1}" target="_blank" data-id="{2}" data-type="{3}">{1}</a>'
        return title_format.format(*args)

    def pagingfromredis(self, model, limit, page):
        uuids = RedisQueryApi().lrange('hotuuid', 0, -1)
        items = Weibo.objects.filter(uuid__in=uuids)
        # 实例化一个分页对象
        paginator = Paginator(items, limit)
        try:
            # 获取某页对应的记录
            items = paginator.page(page)
        except PageNotAnInteger:
            # 如果页码不是个整数 取第一页的记录
            items = paginator.page(1)
        except EmptyPage:
            # 如果页码太大，没有相应的记录 取最后一页的记录
            items = paginator.page(paginator.num_pages)

        return {'items': items, 'total_number': paginator.num_pages}

    # def requesthead(self, limit=6, limit_list=20, sort='', page=1):
    #     parameter = self.request.GET.dict()
    #     api_type = parameter.pop('type')  if parameter.has_key('type') else ''
    #     sort = parameter.pop('sort') if parameter.has_key('sort') else sort
    #     page = parameter.pop('page') if parameter.has_key('page') else page
    #     limit = limit_list if api_type == 'list' else limit
    #     parameter = {'name':'abc'}

    #     container = dict(parameter, **{
    #         'type': api_type,
    #         'page': page,
    #         'sort': sort,
    #         'limit': limit
    #     })
    #     return container

    def requesthead(self, limit=6, limit_list=20, sort='', page=1, cache=1):
        parameter = self.request.GET.dict()
        api_type = parameter.pop('type')  if parameter.has_key('type') else ''
        sort = parameter.pop('sort') if parameter.has_key('sort') else sort
        page = parameter.pop('page') if parameter.has_key('page') else page
        cache = parameter.pop('cache') if parameter.has_key('cache') else 1
        parameter = {'name':'abc'}

        container = dict(parameter, **{
            'type': api_type,
            'page': page,
            'sort': sort,
            'cache': cache,
            'limit': limit_list,
        })
        return container