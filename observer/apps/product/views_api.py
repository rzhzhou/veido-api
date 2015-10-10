# -*- coding: utf-8 -*-
from rest_framework.response import Response

from observer.apps.base.views import BaseAPIView
from observer.apps.base.models import ProductKeyword, Group, Article


class ProductTableView(BaseAPIView):
    def get(self, request, id, page):
        if id:
            try:
                prokey = [ProductKeyword.objects.get(id=id)]
            except ProductKeyword.DoesNotExist:
                group = Group.objects.filter(company=u'广东省质监局')
                prokey = group[0].productkeyword_set.all()
        else:
            group = Group.objects.filter(company=u'广东省质监局')
            prokey = group[0].productkeyword_set.all()

        prokey_len = len(prokey)
        product = [prokey[i].product for i in xrange(prokey_len)]

        data = [p.articles.all() for p in product]
        if data != []:
            item = reduce(lambda x, y: list(set(x).union(set(y))), data)
        else:
            item =[]
        article_ids = [item[i].id for i in range(len(item))]
        item = Article.objects.filter(id__in=article_ids)

        datas = self.paging(item, settings.PRODUCT_LIMIT, page)
        result = self.news_to_json(datas['items'])
        return Response({'total': datas['total_number'], 'data': result})