from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from observer.base.models import Industry, AliasIndustry
from observer.base.service.dashboard import (DashboardData, )
from observer.base.service.search import (SearchData, )
from observer.base.service.industry import (IndustryData, CCCIndustryData, LicenseIndustryData, 
                                            Select2IndustryData, Select2AliasIndustryData, 
                                            AliasIndustryAdd, Select2CCCIndustryData, 
                                            Select2LicenseIndustryData, CCCIndustryAdd, 
                                            LicenseIndustryAdd, )
from observer.base.service.article import (ArticleData, RiskData, RiskDataAdd, RiskDataEdit, 
                                            RiskDataDelete, RiskDataUpload, RiskDataExport, )
from observer.base.service.inspection import (InspectionData, InspectionDataAdd, InspectionDataEdit, 
                                            InspectionDataDelete, InspectionDataUpload, InspectionDataUpload, 
                                            InspectionDataExport, )
from observer.base.service.area import Select2AreaData
from observer.base.service.corpus import (CorpusData, CorpusAdd, CorpusEdit, CorpusDelete, 
                                            )
from observer.base.service.desmon import (DMLinkData, DMLinkAdd, DMLinkEdit, DMLinkDelete, 
                                        DMWordsData, 
                                            )
from observer.base.service.base import (areas, categories, local_related, area, alias_industry, qualitied, )
from observer.utils.date_format import date_format
from observer.utils.excel import write_by_openpyxl


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


class DashboardView(BaseView):

    def __init__(self):
        super(DashboardView, self).__init__()

    def get(self, request):
        return Response(DashboardData(user=request.user).get_all())


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
                    'industry': alias_industry(x['industry_id']),
                    'url': x['url'],
                    'level': x['level'],
                    'area': area(x['area_id']),
                    'source': x['source'],
                    'qualitied': qualitied(x['qualitied']),
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


class Select2AliasIndustryView(BaseView):

    def __init__(self):
        super(Select2AliasIndustryView, self).__init__()

    def set_params(self, request):
        super(Select2AliasIndustryView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = Select2AliasIndustryData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2CCCIndustryView(BaseView):

    def __init__(self):
        super(Select2CCCIndustryView, self).__init__()

    def set_params(self, request):
        super(Select2CCCIndustryView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = Select2CCCIndustryData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2LicenseIndustryView(BaseView):

    def __init__(self):
        super(Select2LicenseIndustryView, self).__init__()

    def set_params(self, request):
        super(Select2LicenseIndustryView, self).set_params(request.GET)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_params(request)

        queryset = Select2LicenseIndustryData(params=self.query_params).get_all()

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
                    'categories': categories(x['guid'], admin=True),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                }, result),
        }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = RiskData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class RiskDataAddView(BaseView):

    def __init__(self):
        super(RiskDataAddView, self).__init__()

    def set_params(self, request):
        super(RiskDataAddView, self).set_params(request.POST)

    def post(self, request):
        self.set_params(request)

        queryset = RiskDataAdd(user=request.user, params=self.query_params).add()

        return Response(status=queryset)


class RiskDataEditView(BaseView):

    def __init__(self):
        super(RiskDataEditView, self).__init__()

    def set_params(self, request):
        super(RiskDataEditView, self).set_params(request.POST)

    def post(self, request, aid):
        self.set_params(request)
        queryset = RiskDataEdit(params=self.query_params).edit(aid=aid)

        return Response(status=queryset)


class RiskDataDeleteView(BaseView):

    def __init__(self):
        super(RiskDataDeleteView, self).__init__()

    def delete(self, request, aid):
        queryset = RiskDataDelete(user=request.user).delete(aid=aid)

        return Response(status=queryset)


class RiskDataUploadView(BaseView):
    parser_classes = (FileUploadParser,)

    def __init__(self):
        super(RiskDataUploadView, self).__init__()

    def put(self, request, filename, format=None):
        queryset = RiskDataUpload(user=request.user).upload(filename, request.FILES['file'])

        return Response(queryset)


class RiskDataExportView(BaseView):

    def __init__(self):
        super(RiskDataExportView, self).__init__()

    def get(self, request):
        response = FileResponse(RiskDataExport(user=request.user).export(), content_type='application/vnd.ms-excel')
        response["Content-Disposition"] = 'attachment; filename=articles.xlsx'

        return response


class InspectionDataView(BaseView):

    def __init__(self):
        super(InspectionDataView, self).__init__()

    def set_params(self, request):
        super(InspectionDataView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(InspectionDataView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                    'guid': x['guid'],
                    'industry': alias_industry(x['industry_id']),
                    'url': x['url'],
                    'level': x['level'],
                    'area': area(x['area_id']),
                    'source': x['source'],
                    'qualitied': qualitied(x['qualitied']),
                    'category': x['category'],
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                }, result),
        }
            
        return data

    def get(self, request):
        self.set_params(request)

        queryset = InspectionData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class InspectionDataAddView(BaseView):

    def __init__(self):
        super(InspectionDataAddView, self).__init__()

    def set_params(self, request):
        super(InspectionDataAddView, self).set_params(request.POST)

    def post(self, request):
        self.set_params(request)

        queryset = InspectionDataAdd(user=request.user, params=self.query_params).add()

        return Response(status=queryset)


class InspectionDataEditView(BaseView):

    def __init__(self):
        super(InspectionDataEditView, self).__init__()

    def set_params(self, request):
        super(InspectionDataEditView, self).set_params(request.POST)

    def post(self, request, aid):
        self.set_params(request)

        queryset = InspectionDataEdit(user=request.user, params=self.query_params).edit(aid=aid)

        return Response(status=queryset)


class InspectionDataDeleteView(BaseView):

    def __init__(self):
        super(InspectionDataDeleteView, self).__init__()

    def delete(self, request, aid):
        queryset = InspectionDataDelete(user=request.user).delete(aid=aid)

        return Response(status=queryset)


class InspectionDataUploadView(BaseView):
    parser_classes = (FileUploadParser,)

    def __init__(self):
        super(InspectionDataUploadView, self).__init__()

    def put(self, request, filename, format=None):

        queryset = InspectionDataUpload(user=request.user).upload(filename, request.FILES['file'])

        return Response(queryset)


class InspectionDataExportView(BaseView):

    def __init__(self):
        super(InspectionDataExportView, self).__init__()

    def get(self, request):
        response = FileResponse(InspectionDataExport(user=request.user).export(), content_type='application/vnd.ms-excel')
        response["Content-Disposition"] = 'attachment; filename=inspections.xlsx'

        return response


class AliasIndustryAddView(BaseView):

    def __init__(self):
        super(AliasIndustryAddView, self).__init__()

    def set_params(self, request):
        super(AliasIndustryAddView, self).set_params(request.POST)

    def post(self, request):
        self.set_params(request)

        queryset = AliasIndustryAdd(user=request.user, params=self.query_params).add()

        return Response(status=queryset)


class CCCIndustryAddView(BaseView):

    def __init__(self):
        super(CCCIndustryAddView, self).__init__()

    def set_params(self, request):
        super(CCCIndustryAddView, self).set_params(request.POST)

    def post(self, request):
        self.set_params(request)

        queryset = CCCIndustryAdd(user=request.user, params=self.query_params).add()

        return Response(status=queryset)


class LicenseIndustryAddView(BaseView):

    def __init__(self):
        super(LicenseIndustryAddView, self).__init__()

    def set_params(self, request):
        super(LicenseIndustryAddView, self).set_params(request.POST)

    def post(self, request):
        self.set_params(request)

        queryset = LicenseIndustryAdd(user=request.user, params=self.query_params).add()

        return Response(status=queryset)


class CorpusView(BaseView):

    def __init__(self):
        super(CorpusView, self).__init__()

    def set_params(self, request):
        super(CorpusView, self).set_params(request.GET)

    def paging(self, queryset):
        return super(CorpusView, self).paging(queryset, self.query_params.get('page', 1), self.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        results = self.paging(queryset)
        data = {'total': total,
                'list': map(lambda r: {
                    'id': r['id'],
                    'industry_id': r['industry__id'], 
                    'industry_name': r['industry__name'], 
                    'riskword': r['riskword'], 
                    'invalidword': r['invalidword'], 
                }, results)
                }

        return data

    def get(self, request):
        self.set_params(request)

        queryset = CorpusData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))


class CorpusAddView(BaseView):

    def __init__(self):
        super(CorpusAddView, self).__init__()

    def set_params(self, request):
        super(CorpusAddView, self).set_params(request.POST)

    def post(self, request):
        self.set_params(request)

        queryset = CorpusAdd(user=request.user, params=self.query_params).add()

        return Response(status=queryset)


class CorpusEditView(BaseView):

    def __init__(self):
        super(CorpusEditView, self).__init__()

    def set_params(self, request):
        super(CorpusEditView, self).set_params(request.POST)

    def post(self, request, cid):
        self.set_params(request)

        queryset = CorpusEdit(user=request.user, params=self.query_params).edit(cid=cid)

        return Response(status=queryset)


class CorpusDeleteView(BaseView):

    def __init__(self):
        super(CorpusDeleteView, self).__init__()

    def delete(self, request, cid):
        queryset = CorpusDelete(user=request.user).delete(cid=cid)

        return Response(status=queryset)


class SearchView(BaseView):

    def __init__(self):
        super(SearchView, self).__init__()

    def set_params(self, request):
        super(SearchView, self).set_params(request.GET)

    def serialize(self, queryset):
        results = queryset['hits']

        data = {
            'total': results['total'],
            'list': results['hits']
        }
        return data

    def get(self, request):
        self.set_params(request)

        queryset = SearchData(params=self.query_params).get_all()

        return Response(self.serialize(queryset))
        