from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.base.models import Industry, AliasIndustry
from observer.base.service.industry import (IndustryData, CCCIndustryData, LicenseIndustryData, 
                                            Select2IndustryData, )
from observer.base.service.article import (ArticleData, )
from observer.base.service.base import (area, )


class BaseView(APIView):

    def __init__(self):
        self.query_params = {}

    def set_params(self, params):
        for k, v in params.items():
            self.query_params[k] = v

    def paging(self, queryset, page, num):
        paginator = Paginator(queryset, num)  # Show $num <QuerySet> per page

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            results = paginator.page(paginator.num_pages)

        return results


class ArticleView(BaseView):

    def __init__(self):
        super(ArticleView, self).__init__()

    def set_params(self, request):
        super(ArticleView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(ArticleView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize0001(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                    'url': x['url'],
                    'title': x['title'],
                    'source': x['source'],
                    'area': area(x['area_id']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                }, result),
        }
            
        return data

    def serialize0002(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                    'url': x['url'],
                    'title': x['title'],
                    'source': x['source'],
                    'area': area(x['area_id']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                }, result),
        }
            
        return data

    def serialize0003(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                    'url': x['url'],
                    'title': x['title'],
                    'source': x['source'],
                    'area': area(x['area_id']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                }, result),
        }
            
        return data

    def get(self, request, category):
        self.set_params(request)

        queryset = ArticleData(params=self.query_params, category=category).get_all()

        return Response(eval('self.serialize%s' % category)(queryset))


class IndustryView(BaseView):

    def __init__(self):
        super(IndustryView, self).__init__()

    def set_params(self, request):
        super(IndustryView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(IndustryView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)

        temp = []
        for l3 in result:
            l2 = l3.parent
            l1 = l2.parent
            temp.append({
                'l4': list(map(lambda x: {
                    'id': x['id'],
                    'name': x['name'],
                    'ccc_id': x['ccc_id'],
                    'license_id': x['license_id'],
                }, AliasIndustry.objects.filter(industry_id=l3.id).values('id', 'name', 'ccc_id', 'license_id'))),
                'l3': {
                    'id': l3.id,
                    'name': l3.name,
                    'desc': l3.desc,
                },
                'l2': {
                    'id': l2.id,
                    'name': l2.name,
                    'desc': l2.desc,
                },
                'l1': {
                    'id': l1.id,
                    'name': l1.name,
                    'desc': l1.desc,
                }, 
            })

        data = {
            'total': total,
            'list': temp,
        }
            
        return data

    def get(self, request):
        self.set_params(request)

        queryset = IndustryData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class CCCIndustryView(BaseView):

    def __init__(self):
        super(CCCIndustryView, self).__init__()

    def set_params(self, request):
        super(CCCIndustryView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(CCCIndustryView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize2(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)

        temp = []
        for l3 in result:
            l2 = l3.parent
            l1 = l2.parent
            temp.append({
                'l3': {
                    'id': l3.id,
                    'name': l3.name,
                    'desc': l3.desc,
                },
                'l2': {
                    'id': l2.id,
                    'name': l2.name,
                    'desc': l2.desc,
                },
                'l1': {
                    'id': l1.id,
                    'name': l1.name,
                    'desc': l1.desc,
                }, 
            })

        data = {
            'total': total,
            'list': temp,
        }
            
        return data

    def get(self, request, cid=None):
        self.set_params(request)

        if not cid:
            queryset = CCCIndustryData(params=self.query_params).get_all()
            return Response(self.serialize(queryset))
        else:
            queryset = CCCIndustryData(params=self.query_params).get_by_id(cid)
            return Response(self.serialize2(queryset))


class LicenseIndustryView(BaseView):

    def __init__(self):
        super(LicenseIndustryView, self).__init__()

    def set_params(self, request):
        super(LicenseIndustryView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(LicenseIndustryView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize2(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)

        temp = []
        for l3 in result:
            l2 = l3.parent
            l1 = l2.parent
            temp.append({
                'l3': {
                    'id': l3.id,
                    'name': l3.name,
                    'desc': l3.desc,
                },
                'l2': {
                    'id': l2.id,
                    'name': l2.name,
                    'desc': l2.desc,
                },
                'l1': {
                    'id': l1.id,
                    'name': l1.name,
                    'desc': l1.desc,
                }, 
            })

        data = {
            'total': total,
            'list': temp,
        }
            
        return data

    def get(self, request, lid=None):
        self.set_params(request)

        if not lid:
            queryset = LicenseIndustryData(params=self.query_params).get_all()
            return Response(self.serialize(queryset))
        else:
            queryset = LicenseIndustryData(params=self.query_params).get_by_id(lid)
            return Response(self.serialize2(queryset))


class Select2IndustryView(BaseView):

    def __init__(self):
        super(Select2IndustryView, self).__init__()

    def set_params(self, request):
        super(Select2IndustryView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = Select2IndustryData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))
