from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.base.models import Industry, AliasIndustry
from observer.base.service.industry import (IndustryData, CCCIndustryData, LicenseIndustryData, 
                                            Select2IndustryData, )
from observer.base.service.article import (ArticleData, RiskData, )
from observer.base.service.inspection import InspectionData
from observer.base.service.area import Select2AreaData
from observer.base.service.desmon import (DMLinkData, DMLinkAdd, DMLinkEdit, DMLinkDelete, 
                                        DMWordsData, 
                                            )
from observer.base.service.base import (areas, categories, local_related, area, industry, )
from observer.utils.date_format import date_format


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
        self.user = request.user
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
                    'areas': areas(x['guid']),
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
                    'areas': areas(x['guid']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                    'score': x['score'],
                    'local_related': local_related(x['guid'], self.user), # 本地风险相关度
                }, result),
        }
            
        return data

    def serialize0003(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                    'categories': categories(x['guid']),
                    'url': x['url'],
                    'title': x['title'],
                    'source': x['source'],
                    'areas': areas(x['guid']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                }, result),
        }
            
        return data

    def get(self, request, category):
        self.set_params(request)

        queryset = ArticleData(params=self.query_params, category=category).get_all()

        return Response(eval('self.serialize%s' % category)(queryset))


class InspectionView(BaseView):

    def __init__(self):
        super(InspectionView, self).__init__()

    def set_params(self, request):
        super(InspectionView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(InspectionView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                    'industry': industry(x['industry_id']),
                    'url': x['url'],
                    'level': x['level'],
                    'area': area(x['area_id']),
                    'source': x['source'],
                    'qualitied': x['qualitied'],
                    'category': x['category'],
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                }, result),
        }
            
        return data

    def get(self, request):
        self.set_params(request)

        queryset = InspectionData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


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


class DMLinkView(BaseView):

    def __init__(self):
        super(DMLinkView, self).__init__()

    def set_params(self, request):
        super(DMLinkView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(DMLinkView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        results = self.paging(queryset)
        data = {'total': total,
                'list': map(lambda r: {
                    'name': r['name'], 
                    'link': r['link'], 
                    'kwords': r['kwords'], 
                    'fwords': r['fwords'], 
                    'status': r['status'], 
                }, results)
                }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = DMLinkData(user=request.user).get_all()

        return Response(self.serialize(queryset))


class DMLinkAddView(BaseView):

    def __init__(self):
        super(DMLinkAddView, self).__init__()

    def set_params(self, request):
        super(DMLinkAddView, self).set_params(request.POST)

    def post(self, request):
        self.set_params(request)

        queryset = DMLinkAdd(user=request.user, params=self.query_params).add_dmlink()

        return Response(queryset)


class DMLinkEditView(BaseView):

    def __init__(self):
        super(DMLinkEditView, self).__init__()

    def set_params(self, request):
        super(DMLinkEditView, self).set_params(request.POST)

    def post(self, request, did):
        self.set_params(request)
        queryset = DMLinkEdit(params=self.query_params).edit_dmlink(did=did)

        return Response(queryset)


class DMLinkDeleteView(BaseView):

    def __init__(self):
        super(DMLinkDeleteView, self).__init__()

    def delete(self, request, did):
        queryset = DMLinkDelete(user=request.user).del_dmlink(did=did)

        return Response(queryset)


class DMWordsView(BaseView):

    def __init__(self):
        super(DMWordsView, self).__init__()

    def set_params(self, request):
        super(DMWordsView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(DMWordsView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        results = self.paging(queryset)
        data = {'total': total,
                'list': map(lambda r: {
                    'industry': r['industry__name'], 
                    'riskword': r['riskword'], 
                    'invalidword': r['invalidword'], 
                }, results)
                }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = DMWordsData().get_all()

        return Response(self.serialize(queryset))


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


class Select2AreaView(BaseView):

    def __init__(self):
        super(Select2AreaView, self).__init__()

    def set_params(self, request):
        super(Select2AreaView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = Select2AreaData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class RiskDataView(BaseView):

    def __init__(self):
        super(RiskDataView, self).__init__()

    def set_params(self, request):
        super(RiskDataView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(RiskDataView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                    'guid': x['guid'],
                    'url': x['url'],
                    'title': x['title'],
                    'score': x['score'],
                    'source': x['source'],
                    'areas': areas(x['guid']),
                    'categories': categories(x['guid']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                }, result),
        }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = RiskData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))
