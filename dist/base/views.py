# -*- coding: utf-8 -*-
from django.views.generic import View
from yqj import login_required


class LoginRequiredMixin(object):
    ALLOWED_METHOD = ['GET']

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class BaseView(LoginRequiredMixin, View):
    INCLUDE_SIDEBAR = True
    INCLUDE_USER = True

    def render_to_response(self, template_path, context={}):
        if self.INCLUDE_SIDEBAR:
            categories = self.get_article_categories()
            #for ctg in categories:
            #    ctg.id = encrypt(ctg.id)
            context['categories'] = categories
            context['industries'] = categories

        if self.INCLUDE_USER:
            user = self.request.myuser
            user.company = user.group.company
            context['user'] = user

        context['user_image'] = get_user_image(user)
        context['locations'] = self.get_locations(user.area)
        return render_to_response(template_path, context)

    def get_article_categories(self):
        return Category.objects.filter(~(Q(name='其他' )|Q(name='政府' )|Q(name='事件' )|Q(name='质监热点' )
            |Q(name='指定监测' )))

    def get_locations(self, area):
        #area = Area.objects.get(id=int(location_id))
        if area.id == 4:
            return []
        return Area.objects.filter(parent=area, level=area.level+1)

    def set_css_to_weixin(self, items):
        html = ""
        count = u'0'
        for item in items:
            html += """<li class="media">"""
            html += """<div class="media-left">"""
            html +=  u'<img class="media-object" src="%s" alt="%s">' % (item.publisher.photo, item.publisher.publisher)
            html += """</div>
                       <div class="media-body"> """
            html +=  u'<h4 class="media-heading">%s</h4>' % (item.publisher.publisher)
            html +=  u'<p><a href="/weixin/%s/" target="_blank">%s</a></p>' % (item.id, item.title)
            html += """<div class="media-meta">
                       <div class="info pull-right">"""
            html +=  u'<span>阅读 %s</span>' % count
            html +=  u'<span><i class="fa fa-thumbs-o-up"></i> %s</span>' % count
            html += """</div>"""
            html +=  u'<div class="time pull-left">%s</div>' % item.pubtime.strftime('%Y-%m-%d %h:%m')
            html += """</div></div></li>"""
        return html

    def set_css_to_weibo(self, items):
        pass

    def paging(self, model, limit, page):
        #limit  每页显示的记录数 page 页码
        items = model.objects.all()
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
