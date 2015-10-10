# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

from backend.base.views import BaseTemplateView
from backend.base.models import Group, ProductKeyword


class ProductView(BaseTemplateView):
    def get(self, reqeust, id):
        if id:
            try:
                prokeyword = ProductKeyword.objects.get(id=id)
                name = prokeyword.newkeyword
            except:
                name = u'全部'
                if id != '0':
                    return HttpResponseRedirect("/product/0/")
        else:
            return HttpResponseRedirect("/product/0/")
        try:
            group = Group.objects.filter(company=u'广东省质监局')
            prokeywords = group[0].productkeyword_set.all()
        except:
            return self.render_to_response('product/product.html', {'product_list': [{'id': '', 'name': ''}],'product': {'name': u'全部'}})
        prokey_len = len(prokeywords)
        prokeyword_list = [{'id': '0', 'name': u'全部'}] + [{'id': prokeywords[i].id, 'name': prokeywords[i].newkeyword} for i in xrange(0, prokey_len)]
        return self.render_to_response('product/product.html', {'product_list': prokeyword_list, 'product': {'name': name}})
