from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import FileResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.base.models import AliasIndustry
from observer.base.service.area import Select2AreaData
from observer.base.service.article import (ArticleData, RiskData, RiskDataAdd,
                                           RiskDataDelete, RiskDataEdit,
                                           RiskDataExport, RiskDataUpload)
from observer.base.service.base import (alias_industry, area, areas,
                                        categories, local_related, qualitied,
                                        risk_injury)
from observer.base.service.corpus import (CorpusAdd, CorpusData, CorpusDelete,
                                          CorpusEdit)
from observer.base.service.dashboard import DashboardData
from observer.base.service.desmon import (DMLinkAdd, DMLinkData, DMLinkDelete,
                                          DMLinkEdit, DMWordsData)
from observer.base.service.industry import (AliasIndustryAdd, CCCIndustryAdd,
                                            CCCIndustryData,
                                            ConsumerIndustryData, IndustryData,
                                            LicenceIndustryAdd,
                                            LicenceIndustryData,
                                            MajorIndustryData,
                                            Select2AliasIndustryData,
                                            Select2CCCIndustryData,
                                            Select2IndustryData,
                                            Select2LicenceIndustryData)
from observer.base.service.inspection import (InspectionData,
                                              InspectionDataAdd,
                                              InspectionDataDelete,
                                              InspectionDataEdit,
                                              InspectionDataExport,
                                              InspectionDataUnEnterpriseUpload,
                                              InspectionDataUpload)
from observer.base.service.search import SearchAdvancedData, SearchData
from observer.utils.date_format import date_format
from observer.utils.excel import write_by_openpyxl


class BaseView(APIView):

    def __init__(self):
        self.request = None

    def set_request(self, request):
        self.request = request

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

    def set_request(self, request):
        super(DashboardView, self).set_request(request)

    def get(self, request):
        self.set_request(request)

        return Response(DashboardData(params=request.query_params, user=request.user).get_all())


class ArticleView(BaseView):

    def __init__(self):
        super(ArticleView, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(ArticleView, self).set_request(request)

    def paging(self, queryset):
        return super(ArticleView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

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
                'risk_injury': risk_injury(x['guid']),
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

    def serialize0004(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'url': x['url'],
                'title': x['title'],
                'source': x['source'],
                'publisher': x['publisher'],
                'areas': areas(x['guid']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
            }, result),
        }

        return data

    def get(self, request, category):
        self.set_request(request)

        queryset = ArticleData(params=request.query_params, category=category).get_all()

        return Response(eval('self.serialize%s' % category)(queryset))


class InspectionView(BaseView):

    def __init__(self):
        super(InspectionView, self).__init__()

    def set_request(self, request):
        super(InspectionView, self).set_request(request)

    def paging(self, queryset):
        return super(InspectionView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

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
        self.set_request(request)

        queryset = InspectionData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class IndustryView(BaseView):

    def __init__(self):
        super(IndustryView, self).__init__()

    def set_request(self, request):
        super(IndustryView, self).set_request(request)

    def paging(self, queryset):
        return super(IndustryView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

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
                    'licence_id': x['licence_id'],
                }, AliasIndustry.objects.filter(industry_id=l3.id).values('id', 'name', 'ccc_id', 'licence_id'))),
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
        self.set_request(request)

        queryset = IndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class CCCListView(BaseView):

    def __init__(self):
        super(CCCListView, self).__init__()

    def set_request(self, request):
        super(CCCListView, self).set_request(request)

    def paging(self, queryset):
        return super(CCCListView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        """
        'parent__parent__id', 'parent__parent__name', 'parent__parent__desc',
        'parent__id', 'parent__name', 'parent__desc',
        'id', 'name', 'desc',
        """
        result = self.paging(queryset)

        data = {
            'total': result.paginator.count,
            'list': map(lambda x: {
                'l1': {
                    'id': x['parent__parent__id'],
                    'name': x['parent__parent__name'],
                    'desc': x['parent__parent__desc'],
                },
                'l2': {
                    'id': x['parent__id'],
                    'name': x['parent__name'],
                    'desc': x['parent__desc'],
                },
                'l3': {
                    'id': x['id'],
                    'name': x['name'],
                    'desc': x['desc'],
                },
            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = CCCIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2CCCListView(BaseView):

    def __init__(self):
        super(Select2CCCListView, self).__init__()

    def set_request(self, request):
        super(Select2CCCListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'text': '%s - %s' % (x['id'], x['name']),
            },
            queryset
        )

        return data

    def get(self, request):
        self.set_request(request)

        queryset = CCCIndustryData(params=request.query_params).get_level()

        return Response(self.serialize(queryset))


class LicenceListView(BaseView):

    def __init__(self):
        super(LicenceListView, self).__init__()

    def set_request(self, request):
        super(LicenceListView, self).set_request(request)

    def paging(self, queryset):
        return super(LicenceListView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        """
        'parent__parent__id', 'parent__parent__name', 'parent__parent__desc',
        'parent__id', 'parent__name', 'parent__desc',
        'id', 'name', 'desc',
        """
        result = self.paging(queryset)

        data = {
            'total': result.paginator.count,
            'list': map(lambda x: {
                'l1': {
                    'id': x['parent__parent__id'],
                    'name': x['parent__parent__name'],
                    'desc': x['parent__parent__desc'],
                },
                'l2': {
                    'id': x['parent__id'],
                    'name': x['parent__name'],
                    'desc': x['parent__desc'],
                },
                'l3': {
                    'id': x['id'],
                    'name': x['name'],
                    'desc': x['desc'],
                },
            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = LicenceIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2LicenceListView(BaseView):

    def __init__(self):
        super(Select2LicenceListView, self).__init__()

    def set_request(self, request):
        super(Select2LicenceListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'text': '%s - %s' % (x['id'], x['name']),
            },
            queryset
        )

        return data

    def get(self, request):
        self.set_request(request)

        queryset = LicenceIndustryData(params=request.query_params).get_level()

        return Response(self.serialize(queryset))


class ConsumerListView(BaseView):

    def __init__(self):
        super(ConsumerListView, self).__init__()

    def set_request(self, request):
        super(ConsumerListView, self).set_request(request)

    def paging(self, queryset):
        return super(ConsumerListView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        """
        'parent__parent__parent__id', 'parent__parent__parent__name', 'parent__parent__parent__desc',
        'parent__parent__id', 'parent__parent__name', 'parent__parent__desc',
        'parent__id', 'parent__name', 'parent__desc',
        'id', 'name', 'desc',
        """
        result = self.paging(queryset)

        data = {
            'total': result.paginator.count,
            'list': map(lambda x: {
                'l1': {
                    'id': x['parent__parent__parent__id'],
                    'name': x['parent__parent__parent__name'],
                    'desc': x['parent__parent__parent__desc'],
                },
                'l2': {
                    'id': x['parent__parent__id'],
                    'name': x['parent__parent__name'],
                    'desc': x['parent__parent__desc'],
                },
                'l3': {
                    'id': x['parent__id'],
                    'name': x['parent__name'],
                    'desc': x['parent__desc'],
                },
                'l4': {
                    'id': x['id'],
                    'name': x['name'],
                    'desc': x['desc'],
                },
            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = ConsumerIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2ConsumerListView(BaseView):

    def __init__(self):
        super(Select2ConsumerListView, self).__init__()

    def set_request(self, request):
        super(Select2ConsumerListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'text': x['name'],
            },
            queryset
        )

        return data

    def get(self, request):
        self.set_request(request)

        queryset = ConsumerIndustryData(params=request.query_params).get_level()

        return Response(self.serialize(queryset))


class MajorListView(BaseView):

    def __init__(self):
        super(MajorListView, self).__init__()

    def set_request(self, request):
        super(MajorListView, self).set_request(request)

    def paging(self, queryset):
        return super(MajorListView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        """
        'parent__parent__id', 'parent__parent__name', 'parent__parent__desc',
        'parent__id', 'parent__name', 'parent__desc',
        'id', 'name', 'desc',
        """
        result = self.paging(queryset)

        data = {
            'total': result.paginator.count,
            'list': map(lambda x: {
                'l1': {
                    'id': x['parent__parent__id'],
                    'name': x['parent__parent__name'],
                    'desc': x['parent__parent__desc'],
                },
                'l2': {
                    'id': x['parent__id'],
                    'name': x['parent__name'],
                    'desc': x['parent__desc'],
                },
                'l3': {
                    'id': x['id'],
                    'name': x['name'],
                    'desc': x['desc'],
                },
                'licence': x['licence'],
                'ccc': x['ccc'],
            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = MajorIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class MajorView(BaseView):

    def __init__(self):
        super(MajorView, self).__init__()

    def set_request(self, request):
        super(MajorView, self).set_request(request)

    def patch(self, request, pk):
        self.set_request(request)

        value = MajorIndustryData(params=request.data).save(pk)

        return Response(value)


class Select2MajorListView(BaseView):

    def __init__(self):
        super(Select2MajorListView, self).__init__()

    def set_request(self, request):
        super(Select2MajorListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'text': x['name'],
            },
            queryset
        )

        return data

    def get(self, request):
        self.set_request(request)

        queryset = MajorIndustryData(params=request.query_params).get_level()

        return Response(self.serialize(queryset))


class CCCIndustryView(BaseView):

    def __init__(self):
        super(CCCIndustryView, self).__init__()

    def set_request(self, request):
        super(CCCIndustryView, self).set_request(request)

    def paging(self, queryset):
        return super(CCCIndustryView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

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
        self.set_request(request)

        if not cid:
            queryset = CCCIndustryData(params=request.query_params).get_all()
            return Response(self.serialize(queryset))
        else:
            queryset = CCCIndustryData(params=request.query_params).get_by_id(cid)
            return Response(self.serialize2(queryset))


class LicenceIndustryView(BaseView):

    def __init__(self):
        super(LicenceIndustryView, self).__init__()

    def set_request(self, request):
        super(LicenceIndustryView, self).set_request(request)

    def paging(self, queryset):
        return super(LicenceIndustryView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

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
        self.set_request(request)

        if not lid:
            queryset = LicenceIndustryData(params=request.query_params).get_all()
            return Response(self.serialize(queryset))
        else:
            queryset = LicenceIndustryData(params=request.query_params).get_by_id(lid)
            return Response(self.serialize2(queryset))


class DMLinkView(BaseView):

    def __init__(self):
        super(DMLinkView, self).__init__()

    def set_request(self, request):
        super(DMLinkView, self).set_request(request)

    def paging(self, queryset):
        return super(DMLinkView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        total = queryset.count()
        results = self.paging(queryset)
        data = {
            'total': total,
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
        self.set_request(request)

        queryset = DMLinkData(user=request.user).get_all()

        return Response(self.serialize(queryset))


class DMLinkAddView(BaseView):

    def __init__(self):
        super(DMLinkAddView, self).__init__()

    def set_request(self, request):
        super(DMLinkAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = DMLinkAdd(user=request.user, params=request.data).add_dmlink()

        return Response(queryset)


class DMLinkEditView(BaseView):

    def __init__(self):
        super(DMLinkEditView, self).__init__()

    def set_request(self, request):
        super(DMLinkEditView, self).set_request(request)

    def post(self, request, did):
        self.set_request(request)
        queryset = DMLinkEdit(params=request.data).edit_dmlink(did=did)

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

    def set_request(self, request):
        super(DMWordsView, self).set_request(request)

    def paging(self, queryset):
        return super(DMWordsView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        total = queryset.count()
        results = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda r: {
                'industry': r['industry__name'],
                'riskword': r['riskword'],
                'invalidword': r['invalidword'],
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = DMWordsData().get_all()

        return Response(self.serialize(queryset))


class Select2IndustryView(BaseView):

    def __init__(self):
        super(Select2IndustryView, self).__init__()

    def set_request(self, request):
        super(Select2IndustryView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = Select2IndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2AliasIndustryView(BaseView):

    def __init__(self):
        super(Select2AliasIndustryView, self).__init__()

    def set_request(self, request):
        super(Select2AliasIndustryView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = Select2AliasIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2CCCIndustryView(BaseView):

    def __init__(self):
        super(Select2CCCIndustryView, self).__init__()

    def set_request(self, request):
        super(Select2CCCIndustryView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = Select2CCCIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2LicenceIndustryView(BaseView):

    def __init__(self):
        super(Select2LicenceIndustryView, self).__init__()

    def set_request(self, request):
        super(Select2LicenceIndustryView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = Select2LicenceIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2AreaView(BaseView):

    def __init__(self):
        super(Select2AreaView, self).__init__()

    def set_request(self, request):
        super(Select2AreaView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = Select2AreaData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class RiskDataView(BaseView):

    def __init__(self):
        super(RiskDataView, self).__init__()

    def set_request(self, request):
        super(RiskDataView, self).set_request(request)

    def paging(self, queryset):
        return super(RiskDataView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

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
        self.set_request(request)

        queryset = RiskData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class RiskDataAddView(BaseView):

    def __init__(self):
        super(RiskDataAddView, self).__init__()

    def set_request(self, request):
        super(RiskDataAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = RiskDataAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class RiskDataEditView(BaseView):

    def __init__(self):
        super(RiskDataEditView, self).__init__()

    def set_request(self, request):
        super(RiskDataEditView, self).set_request(request)

    def post(self, request, aid):
        self.set_request(request)
        queryset = RiskDataEdit(params=request.data).edit(aid=aid)

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
        response = FileResponse(
            RiskDataExport(user=request.user).export(),
            content_type='application/vnd.ms-excel'
        )
        response["Content-Disposition"] = 'attachment; filename=articles.xlsx'

        return response


class InspectionDataView(BaseView):

    def __init__(self):
        super(InspectionDataView, self).__init__()

    def set_request(self, request):
        super(InspectionDataView, self).set_request(request)

    def paging(self, queryset):
        return super(InspectionDataView, self).paging(queryset, self.request.query_params.get('page', 1), self.request.query_params.get('length', 15))

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
        self.set_request(request)

        queryset = InspectionData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class InspectionDataAddView(BaseView):

    def __init__(self):
        super(InspectionDataAddView, self).__init__()

    def set_request(self, request):
        super(InspectionDataAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = InspectionDataAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class InspectionDataEditView(BaseView):

    def __init__(self):
        super(InspectionDataEditView, self).__init__()

    def set_request(self, request):
        super(InspectionDataEditView, self).set_request(request)

    def post(self, request, aid):
        self.set_request(request)

        queryset = InspectionDataEdit(user=request.user, params=request.data).edit(aid=aid)

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


class InspectionDataUnEnterpriseUploadView(BaseView):
    parser_classes = (FileUploadParser,)

    def __init__(self):
        super(InspectionDataUnEnterpriseUploadView, self).__init__()

    def put(self, request, filename, format=None):

        queryset = InspectionDataUnEnterpriseUpload(user=request.user).upload(
            filename, request.FILES['file'])

        return Response(queryset)


class InspectionDataExportView(BaseView):

    def __init__(self):
        super(InspectionDataExportView, self).__init__()

    def get(self, request):
        response = FileResponse(
            InspectionDataExport(user=request.user).export(),
            content_type='application/vnd.ms-excel'
        )
        response["Content-Disposition"] = 'attachment; filename=inspections.xlsx'

        return response


class AliasIndustryAddView(BaseView):

    def __init__(self):
        super(AliasIndustryAddView, self).__init__()

    def set_request(self, request):
        super(AliasIndustryAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = AliasIndustryAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class CCCIndustryAddView(BaseView):

    def __init__(self):
        super(CCCIndustryAddView, self).__init__()

    def set_request(self, request):
        super(CCCIndustryAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = CCCIndustryAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class LicenceIndustryAddView(BaseView):

    def __init__(self):
        super(LicenceIndustryAddView, self).__init__()

    def set_request(self, request):
        super(LicenceIndustryAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = LicenceIndustryAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class CorpusView(BaseView):

    def __init__(self):
        super(CorpusView, self).__init__()

    def set_request(self, request):
        super(CorpusView, self).set_request(request)

    def paging(self, queryset):
        return super(CorpusView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        total = queryset.count()
        results = self.paging(queryset)
        data = {
            'total': total,
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
        self.set_request(request)

        queryset = CorpusData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class CorpusAddView(BaseView):

    def __init__(self):
        super(CorpusAddView, self).__init__()

    def set_request(self, request):
        super(CorpusAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = CorpusAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class CorpusEditView(BaseView):

    def __init__(self):
        super(CorpusEditView, self).__init__()

    def set_request(self, request):
        super(CorpusEditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = CorpusEdit(user=request.user, params=request.data).edit(cid=cid)

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

    def set_request(self, request):
        super(SearchView, self).set_request(request)

    def serialize(self, queryset):
        results = queryset['hits']

        data = {
            'total': results['total'],
            'list': map(lambda x: {
                'source': x['_source']['source'],
                'category': x['_source']['category'],
                'title': x['_source']['title'] if not x.get('highlight') else x['highlight']['title'][0],
                'risk_keyword': x['_source']['risk_keyword'],
                'pubtime': x['_source']['pubtime'],
                'invalid_keyword': x['_source']['invalid_keyword'],
                'score': x['_source']['score'],
                'url': x['_source']['url'],
                'area': x['_source']['area'],
            }, results['hits']),
        }
        return data

    def get(self, request):
        self.set_request(request)

        queryset = SearchData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class SearchAdvancedView(BaseView):

    def __init__(self):
        super(SearchAdvancedView, self).__init__()

    def set_request(self, request):
        super(SearchAdvancedView, self).set_request(request)

    def serialize(self, queryset):
        return queryset

        results = queryset['hits']

        data = {
            'total': results['total'],
            'list': map(lambda x: {
                'source': x['_source']['source'],
                'category': x['_source']['category'],
                'title': x['_source']['title'] if not x.get('highlight') else x['highlight']['title'][0],
                'risk_keyword': x['_source']['risk_keyword'],
                'pubtime': x['_source']['pubtime'],
                'invalid_keyword': x['_source']['invalid_keyword'],
                'score': x['_source']['score'],
                'url': x['_source']['url'],
                'area': x['_source']['area'],
            }, results['hits']),
        }
        return data

    def get(self, request):
        self.set_request(request)

        queryset = SearchAdvancedData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))
