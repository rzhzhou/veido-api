import os

from django.contrib.auth.models import Group, User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import FileResponse
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.base.models import AliasIndustry, Nav, NewsReport, UserNav
from observer.base.service.area import Select2AreaData
from observer.base.service.article import (ArticleData, RiskData, RiskDataAdd,
                                           RiskDataAudit, RiskDataDelete,
                                           RiskDataEdit, RiskDataExport,
                                           RiskDataSuzhou, RiskDataUpload,
                                           StatisticsShow, newsCrawlerData)
from observer.base.service.base import (alias_industry, area, areas,
                                        categories, get_major_category,
                                        get_major_industry, get_user_extra,
                                        get_user_nav, local_related, qualitied)
from observer.base.service.corpus import (CategoryListData, CorpusAdd,
                                          CorpusData, CorpusDelete, CorpusEdit,
                                          CrawlerData)
from observer.base.service.dashboard import DashboardData
from observer.base.service.desmon import (DMLinkAdd, DMLinkData, DMLinkDelete,
                                          DMLinkEdit, DMWordsData)
from observer.base.service.industry import (AliasIndustryAdd, CCCIndustryAdd,
                                            CCCIndustryData,
                                            ConsumerIndustryData,
                                            CpcIndustryData, IndustryData,
                                            IndustryProductsData,
                                            LicenceIndustryAdd,
                                            LicenceIndustryData,
                                            MajorIndustryData,
                                            Select2AliasIndustryData,
                                            Select2CCCIndustryData,
                                            Select2IndustryData,
                                            Select2LicenceIndustryData)
from observer.base.service.inspection import (EnterpriseData,
                                              EnterpriseDataAudit,
                                              EnterpriseDataDelete,
                                              EnterpriseDataEdit,
                                              EnterpriseDataUnqualified,
                                              InspectionData,
                                              InspectionDataAdd,
                                              InspectionDataAudit,
                                              InspectionDataCrawler,
                                              InspectionDataDelete,
                                              InspectionDataEdit,
                                              InspectionDataExport,
                                              InspectionDataSuzhou,
                                              InspectionDataUnEnterpriseUpload,
                                              InspectionDataUpload)
from observer.base.service.navbar import NavBarEdit
from observer.base.service.news import NewsAdd, NewsDelete, NewsEdit, ViewsData
from observer.base.service.report import (NewsReportData, NewsReportDelete,
                                          NewsReportSuzhou, NewsReportUpload)
from observer.base.service.search import SearchAdvancedData, SearchData
from observer.base.service.user import (GroupData, UserAdd, UserData,
                                        UserDelete, UserEdit)
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
    # 0001---质量热点
    # 0002---风险快讯
    # 0003---业务信息
    # 0004---专家视点

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
                'areas': areas(x['id']),
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
                'areas': areas(x['id']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'score': x['score'],
                'local_related': local_related(x['id'], self.user), # 本地风险相关度
            }, result),
        }

        return data

    def serialize0003(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'categories': categories(x['id']),
                'url': x['url'],
                'title': x['title'],
                'source': x['source'],
                'areas': areas(x['id']),
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
                'areas': areas(x['id']),
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
                'id': x['id'],
                'industry': {'id': x['industry'], 'text': x['industry__name']},
                'origin_product': x['origin_product'],
                'url': x['url'],
                'level': x['level'],
                'area': {'id': x['area'], 'text': x['area__name']},
                'source': x['source'],
                'qualitied': qualitied(x['qualitied']),
                'unqualitied_patch': x['unqualitied_patch'],
                'qualitied_patch': x['qualitied_patch'],
                'inspect_patch': x['inspect_patch'],
                'category': x['category'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'product': x['product_name'],
                'status': x['status'],
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


class SelectCpcisView(BaseView):
    """docstring for SelectCpcisView"""
    def __init__(self):
        super(SelectCpcisView, self).__init__()

    def set_request(self, request):
        super(SelectCpcisView, self).set_request(request)

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

        queryset = CpcIndustryData(params=request.query_params).get_level()

        return Response(self.serialize(queryset))


class CpcListView(BaseView):
    def __init__(self):
        super(CpcListView, self).__init__()

    def set_request(self, request):
        super(CpcListView, self).set_request(request)

    def paging(self, queryset):
        return super(CpcListView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )
    def serialize(self, queryset):
        """
        'id', 'name', 'desc',
        """
        result = self.paging(queryset)

        data = {
            'total': result.paginator.count,
            'list': map(lambda x: {
                'id': x['id'],
                'name': x['name'],
                'desc': x['desc'],
                'level': x['level'],
            }, result),
        }

        return data
    def get(self, request):
        self.set_request(request)

        queryset = CpcIndustryData(params=request.query_params).get_all()

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
        'id', 'name', 'desc',
        """
        result = self.paging(queryset)

        data = {
            'total': result.paginator.count,
            'list': map(lambda x: {
                'id': x['id'],
                'name': x['name'],
                'desc': x['desc'],
                'level': x['level'],
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

# 产品总分类
class CpcIndustryView(BaseView):
    def __init__(self):
        super(CpcIndustryView, self).__init__()

    def set_request(self, request):
        super(CpcIndustryView, self).set_request(request)

    def paging(self, queryset):
        return super(CpcIndustryView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )
    def serialize2(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)

        temp = []
        for l5 in result:
            l4 = l5.parent
            l3 = l4.parent
            l2 = l3.parent
            l1 = l2.parent
            temp.append({
                'l5': {
                    'id': l5.id,
                    'name': l5.name,
                    'desc': l5.desc,
                },
                'l4': {
                    'id': l4.id,
                    'name': l4.name,
                    'desc': l4.desc,
                },
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
            queryset = CpcIndustryData(params=request.query_params).get_all()
            return Response(self.serialize(queryset))
        else:
            queryset = CpcIndustryData(params=request.query_params).get_by_id(lid)
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
                'industry': get_major_industry(r['industry_id']),
                'riskword': r['riskword'],
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = DMWordsData(params=request.query_params).get_all()

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


class Select2IndustryProductsView(BaseView):

    def __init__(self):
        super(Select2IndustryProductsView, self).__init__()

    def set_request(self, request):
        super(Select2IndustryProductsView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = IndustryProductsData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class Select2GroupView(BaseView):

    def __init__(self):
        super(Select2GroupView, self).__init__()

    def set_request(self, request):
        super(Select2GroupView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'text': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = GroupData(params=request.query_params).get_all()

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
                'id': x['id'],
                'url': x['url'],
                'title': x['title'],
                'score': x['score'],
                'source': x['source'],
                'areas': areas(x['id']),
                'categories': categories(x['id'], admin=True),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                'status': x['status'],
            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = RiskData(user=request.user, params=request.query_params).get_all()

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


class RiskDataAuditView(BaseView):

    def __init__(self):
        super(RiskDataAuditView, self).__init__()

    def set_request(self, request):
        super(RiskDataAuditView, self).set_request(request)

    def post(self, request, aid):
        self.set_request(request)
        queryset = RiskDataAudit(params=request.data).edit(aid=aid)

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
                'id': x['id'],
                'industry': {'id': x['industry'], 'text': x['industry__name']},
                'origin_product': x['origin_product'],
                'url': x['url'],
                'level': x['level'],
                'area': {'id': x['area'], 'text': x['area__name']},
                'source': x['source'],
                'qualitied': qualitied(x['qualitied']),
                'unqualitied_patch': x['unqualitied_patch'],
                'qualitied_patch': x['qualitied_patch'],
                'inspect_patch': x['inspect_patch'],
                'category': x['category'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'product': x['product_name'],
                'status': x['status'],

            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = InspectionData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class EnterpriseDataUnqualifiedView(BaseView):
    def __init__(self):
        super(EnterpriseDataUnqualifiedView, self).__init__()

    def set_request(self, request):
        super(EnterpriseDataUnqualifiedView, self).set_request(request)

    def paging(self, queryset):
        # 传给前台的'length',15 key可以自定义,前台不指定 默认15条/页
        return super(EnterpriseDataUnqualifiedView, self).paging(
            queryset, self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'industry': {'id':x['inspection__industry'],'text':x['inspection__industry__name']},
                'product_name': x['inspection__product_name'],
                'source': x['inspection__source'],
                'enterprise': x['name'],
                'area': area(x['area_id']),
                'unitem': x['unitem'],
                'pubtime': x['inspection__pubtime'],
            }, result),
        }
        return data

    def get(self, request):
        self.set_request(request)

        queryset = EnterpriseDataUnqualified(
            params=request.query_params).get_all()

        return Response(self.serialize(queryset))

class EnterpriseDataListView(BaseView):

    def __init__(self):
        super(EnterpriseDataListView, self).__init__()

    def set_request(self, request):
        super(EnterpriseDataListView, self).set_request(request)

    def paging(self, queryset):
        return super(EnterpriseDataListView, self).paging(
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
                'id': x['id'],
                'name': x['name'],
                'unitem': x['unitem'],
                'area': area(x['area_id']),
                'status': x['status'],
            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = EnterpriseData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class EnterpriseDataEditView(BaseView):

    def __init__(self):
        super(EnterpriseDataEditView, self).__init__()

    def set_request(self, request):
        super(EnterpriseDataEditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)
        queryset = EnterpriseDataEdit(params=request.data).edit(cid=cid)

        return Response(status=queryset)


class EnterpriseDataDeleteView(BaseView):

    def __init__(self):
        super(EnterpriseDataDeleteView, self).__init__()

    def delete(self, request, cid):
        queryset = EnterpriseDataDelete(user=request.user).delete(cid=cid)

        return Response(status=queryset)


class EnterpriseDataAuditView(BaseView):

    def __init__(self):
        super(EnterpriseDataAuditView, self).__init__()

    def set_request(self, request):
        super(EnterpriseDataAuditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)
        queryset = EnterpriseDataAudit(params=request.data).edit(cid=cid)

        return Response(status=queryset)


class EnterpriseDataView(BaseView):

    def __init__(self):
        super(EnterpriseDataView, self).__init__()

    def set_request(self, request):
        super(EnterpriseDataView, self).set_request(request)

    def paging(self, queryset):
        return super(EnterpriseDataView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 8)
        )

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)

        temp = []
        for index in result:
            temp.append({
                'name': index.name,
                'area': area(index.area_id),
                'unitem': index.unitem,
            })

        data = {
            'total': total,
            'list': temp,
        }

        return data

    def get(self, request, eid=None):
        self.set_request(request)

        queryset = EnterpriseData(params=request.query_params).get_by_id(eid)

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

    def post(self, request, cid):
        self.set_request(request)

        queryset = InspectionDataEdit(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class InspectionDataDeleteView(BaseView):

    def __init__(self):
        super(InspectionDataDeleteView, self).__init__()

    def delete(self, request, cid):
        queryset = InspectionDataDelete(user=request.user).delete(cid=cid)

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


class InspectionDataCrawlerView(BaseView):

    def __init__(self):
        super(InspectionDataCrawlerView, self).__init__()

    def set_request(self, request):
        super(InspectionDataCrawlerView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = InspectionDataCrawler(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class InspectionDataAuditView(BaseView):

    def __init__(self):
        super(InspectionDataAuditView, self).__init__()

    def set_request(self, request):
        super(InspectionDataAuditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = InspectionDataAudit(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


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
                'status': r['status'],
                'riskword': r.get('riskword', ''),
                'industry': {'id': r.get('industry_id', 0), 'text': '无'} if not r.get('industry_id') else get_major_industry(r['industry_id']),
                'keyword': r.get('keyword', ''),
                'category': get_major_category(r['category_id']) if r.get('category_id', None) else r.get('category_id', ''),
            }, results)

        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = DMWordsData(user=request.user, params=request.query_params).get_all()

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


class CategoryListView(BaseView):

    def __init__(self):
        super(CategoryListView, self).__init__()

    def set_request(self, request):
        super(CategoryListView, self).set_request(request)

    def read_category(self, results):

        data = map(lambda r : {

                'category_id' : r['id'],
                'category' : r['name'],

            },results)


        return data

    def get(self, request):
        self.set_request(request)

        results = CategoryListData(params = request.query_params).get_all()

        return Response(self.read_category(results))



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

    def set_request(self, request):
        super(CorpusDeleteView, self).set_request(request)

    def delete(self, request, cid):
        queryset = CorpusDelete(user=request.user, params=request.data).delete(cid=cid)

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
                'pubtime': x['_source']['pubtime'],
                'score': x['_source']['score'],
                'url': x['_source']['url'],
                'area': x['_source']['area'],
                'industry_id': x['_source']['industry_id'],
                'corpus_id': x['_source']['corpus_id'],
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


class CrawlerView(BaseView):

    def __init__(self):
        super(CrawlerView, self).__init__()

    def set_request(self, request):
        super(CrawlerView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = CrawlerData(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class InspectionDataViewSuzhou(BaseView):

    def __init__(self):
        super(InspectionDataViewSuzhou, self).__init__()

    def set_request(self, request):
        super(InspectionDataViewSuzhou, self).set_request(request)

    def paging(self, queryset):
        page = (int(self.request.query_params.get('start', 0)) /
                int(self.request.query_params.get('length', 10))) + 1
        return super(InspectionDataViewSuzhou, self).paging(queryset, page, self.request.query_params.get('length', 10))

    def serialize(self, queryset):
        results = self.paging(queryset)
        recordsTotal = queryset.count()
        data = {
            "draw": self.request.query_params.get('draw', 1),
            "recordsTotal": recordsTotal,
            "recordsFiltered": InspectionDataSuzhou(params=self.request.query_params).get_inspection_list(str(self.request.query_params.get('search[value]')).strip()).count(),
            "data": map(lambda x: {
                'id': x['id'],
                'industry': get_major_industry(x['industry_id']),
                'titleAndurl': [get_major_industry(x['industry_id']), x['url']],
                'level': x['level'],
                'area': area(x['area_id']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'source': x['source'],
                'qualitied': qualitied(x['qualitied']),
                'unqualitied_patch': x['unqualitied_patch'],
                'qualitied_patch': x['qualitied_patch'],
                'inspect_patch': x['inspect_patch'],
                'category': x['category'],
                'product': x['product_name'],
                'status': x['status'],
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        limit = int(request.query_params.get('limit', 0))

        queryset = InspectionDataSuzhou(
            params=request.query_params).get_inspection_list(str(request.query_params.get('search[value]')).strip()).order_by('-pubtime')

        if limit:
            queryset = queryset[:limit]

        return Response(self.serialize(queryset))


class RiskDataViewSuzhou(BaseView):

    def __init__(self):
        super(RiskDataViewSuzhou, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(RiskDataViewSuzhou, self).set_request(request)

    def paging(self, queryset):
        page = (int(self.request.query_params.get('start', 0)) /
                int(self.request.query_params.get('length', 10))) + 1
        return super(RiskDataViewSuzhou, self).paging(queryset, page, self.request.query_params.get('length', 10))

    def serialize(self, queryset):
        results = self.paging(queryset)
        recordsTotal = queryset.count()
        data = {
            "draw": self.request.query_params.get('draw', 1),
            "recordsTotal": recordsTotal,
            "recordsFiltered": RiskDataSuzhou(params=self.request.query_params).get_risk_data_list(str(self.request.query_params.get('search[value]')).strip()).count(),
            "data": map(lambda x: {
                'titleAndurl': [x['title'], x['url']],
                'source': x['source'],
                'areas': areas(x['guid']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'score': x['score'],
                'local_related': local_related(x['guid'], self.user), # 本地风险相关度
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        limit = int(request.query_params.get('limit', 0))

        queryset = RiskDataSuzhou(
            params=request.query_params).get_risk_data_list(str(request.query_params.get('search[value]')).strip()).order_by('-pubtime')

        if limit:
            queryset = queryset[:limit]

        return Response(self.serialize(queryset))


class NewsReportViewSuzhou(BaseView):

    def __init__(self):
        super(NewsReportViewSuzhou, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(NewsReportViewSuzhou, self).set_request(request)

    def paging(self, queryset):
        page = (int(self.request.query_params.get('start', 0)) /
                int(self.request.query_params.get('length', 10))) + 1
        return super(NewsReportViewSuzhou, self).paging(queryset, page, self.request.query_params.get('length', 10))

    def serialize(self, queryset):
        results = self.paging(queryset)
        recordsTotal = queryset.count()
        data = {
            "draw": self.request.query_params.get('draw', 1),
            "recordsTotal": recordsTotal,
            "recordsFiltered": NewsReportSuzhou(params=self.request.query_params).get_news_report_list(str(self.request.query_params.get('search[value]')).strip()).count(),
            "data": map(lambda x: {
                'id': x['id'],
                'group': x['group__name'],
                'year': x['year'],
                'period': x['period'],
                'news_type': x['news_type'],
                'publisher': x['publisher'],
                'pubtime': x['pubtime'],
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        limit = int(request.query_params.get('limit', 0))

        queryset = NewsReportSuzhou(
            params=request.query_params).get_news_report_list(str(request.query_params.get('search[value]')).strip()).order_by('-pubtime')

        if limit:
            queryset = queryset[:limit]

        return Response(self.serialize(queryset))


class NavBarView(BaseView):

    def __init__(self):
        super(NavBarView, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(NavBarView, self).set_request(request)

    def serialize(self):
        navs = []
        u_navs_ids = UserNav.objects.filter(user=self.user).values_list('nav', flat=True)
        L1 = Nav.objects.filter(id__in=u_navs_ids, level=1).values('name','id').order_by('index')
        if L1:
            for category in L1:
                navs.append({
                    'category': category['name'],
                })

                L2 = Nav.objects.filter(id__in=u_navs_ids, level=2, parent_id=category['id']).values('name', 'id', 'href', 'icon').order_by('index')
                if L2:
                    for title in L2:
                        childrens = Nav.objects.filter(id__in=u_navs_ids, level=3, parent_id=title['id']).values_list('name')
                        navs.append({
                            'icon': title['icon'],
                            'title': title['name'],
                            'href': '' if title['href'] == '0' else title['href'],
                            'children': list(map(lambda x: {
                                'title': x['name'],
                                'href': x['href'],
                            }, Nav.objects.filter(id__in=u_navs_ids, level=3, parent_id=title['id']).values('name', 'href').order_by('index'))) if childrens else ''
                        })

        data = {
            'menus': navs,
        }

        return data

    def get(self, request):
        self.set_request(request)

        return Response(self.serialize())


class NavBarEditView(BaseView):

    def __init__(self):
        super(NavBarEditView, self).__init__()

    def set_request(self, request):
        super(NavBarEditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = NavBarEdit(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class UserView(BaseView):

    def __init__(self):
        super(UserView, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(UserView, self).set_request(request)

    def paging(self, queryset):
        return super(UserView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        count = len(queryset)
        results = self.paging(queryset)
        data = {
            'total': count,
            'list': map(lambda x: {
                'id': x['id'],
                'username': x['username'],
                'first_name': x['first_name'],
                'last_name': x['last_name'],
                'email': x['email'],
                'is_active': x['is_active'],
                'user_nav': get_user_nav(x['id']),
                'extra': get_user_extra(x['id']),
            }, results),
            'current_user': {
                'id': self.user.id,
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'is_active': self.user.is_active,
                'user_nav': get_user_nav(self.user.id),
                'extra': get_user_extra(self.user.id),
            }
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = UserData(user=request.user).get_all()

        return Response(self.serialize(queryset))


class UserAddView(BaseView):

    def __init__(self):
        super(UserAddView, self).__init__()

    def set_request(self, request):
        super(UserAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = UserAdd(user=request.user, params=request.data).add_user()

        return Response(status=queryset)


class UserEditView(BaseView):

    def __init__(self):
        super(UserEditView, self).__init__()

    def set_request(self, request):
        super(UserEditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = UserEdit(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class UserDeleteView(BaseView):

    def __init__(self):
        super(UserDeleteView, self).__init__()

    def set_request(self, request):
        super(UserDeleteView, self).set_request(request)

    def delete(self, request, cid):
        self.set_request(request)

        queryset = UserDelete(user=request.user).delete(cid=cid)

        return Response(status=queryset)


class UserNavView(BaseView):

    def __init__(self):
        super(UserNavView, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(UserNavView, self).set_request(request)

    def get(self, request, cid):
        self.set_request(request)
        menus = []
        group_names = Group.objects.filter(user=self.user).values_list('name', flat=True)
        name_and_id = Nav.objects.values('name','id').order_by('index')

        # 如果当前操作的是'超级管理员'
        if '超级管理员' in group_names:
            L1 = name_and_id.filter(level=1)
            for category in L1:
                menus.append({
                    'id': category['id'],
                    'label': category['name'],
                    'children': list(map(lambda x: {
                        'id': x['id'],
                        'label': x['name'],
                        'children': list(map(lambda y: {
                            'id': y['id'],
                            'label': y['name'],
                        }, Nav.objects.filter(level=3, parent_id=x['id']).values('name', 'id').order_by('index'))) if Nav.objects.filter(level=3, parent_id=x['id']) else ''
                    }, Nav.objects.filter(level=2, parent_id=category['id']).values('name', 'id').order_by('index'))) if Nav.objects.filter(level=2, parent_id=category['id']) else ''
                })
        else:
            u_navs_ids = UserNav.objects.filter(user=self.user).values_list('nav', flat=True)
            L1 = name_and_id.filter(id__in=u_navs_ids, level=1)

            if L1:
                for category in L1:
                    menus.append({
                        'id': category['id'],
                        'label': category['name'],
                        'children': list(map(lambda x: {
                            'id': x['id'],
                            'label': x['name'],
                            'children': list(map(lambda y: {
                                'id': y['id'],
                                'label': y['name'],
                            }, Nav.objects.filter(id__in=u_navs_ids, level=3, parent_id=x['id']).values('name', 'id').order_by('index'))) if Nav.objects.filter(id__in=u_navs_ids, level=3, parent_id=x['id']) else ''
                        }, Nav.objects.filter(id__in=u_navs_ids, level=2, parent_id=category['id']).values('name', 'id').order_by('index'))) if Nav.objects.filter(id__in=u_navs_ids, level=2, parent_id=category['id']) else ''
                    })

        data = {
            'menus': menus,
        }

        return Response(data)


class NewsView(BaseView):

    def __init__(self):
        super(NewsView, self).__init__()

    def set_request(self, request):
        super(NewsView, self).set_request(request)

    def paging(self, queryset):
        return super(NewsView, self).paging(
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
                'title': r['title'],
                'photo': r['photo'],
                'content': r['content'],
                'pubtime': r['pubtime'],
                'tag': r['tag'],
                'views': r['views'],
                'abstract': r['abstract'],
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = ViewsData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class NewsAddView(BaseView):

    def __init__(self):
        super(NewsAddView, self).__init__()

    def set_request(self, request):
        super(NewsAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = NewsAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class NewsDeleteView(BaseView):
    def __init__(self):
        super(NewsDeleteView, self).__init__()

    def set_request(self, request):
        super(NewsDeleteView, self).set_request(request)

    def delete(self, request, cid):
        self.set_request(request)

        queryset = NewsDelete(user=request.user, params=request.data).delete(cid=cid)

        return Response(status=queryset)


class NewsEditView(BaseView):
    def __init__(self):
        super(NewsEditView, self).__init__()

    def set_request(self, request):
        super(NewsEditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = NewsEdit(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class newsCrawlerView(BaseView):

    def __init__(self):
        super(newsCrawlerView, self).__init__()

    def set_request(self, request):
        super(newsCrawlerView, self).set_request(request)

    def post(self, request):
        self.set_request(request)
        queryset = newsCrawlerData(user = request.user, params = request.data).edit()
        return Response(status = queryset)


class NewsReportView(BaseView):

    def __init__(self):
        super(NewsReportView, self).__init__()

    def set_request(self, request):
        super(NewsReportView, self).set_request(request)

    def paging(self, queryset):
        return super(NewsReportView ,self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15),
        )

    def serialize(self, queryset):
        total = queryset.count()
        results = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'id': x['id'],
                'group': x['group__name'],
                'year': x['year'],
                'period': x['period'],
                'news_type': x['news_type'],
                'publisher': x['publisher'],
                'pubtime': x['pubtime'],
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = NewsReportData(user=request.user, params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class NewsReportUploadView(BaseView):

    def __init__(self):
        super(NewsReportUploadView, self).__init__()

    def set_request(self, request):
        super(NewsReportUploadView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = NewsReportUpload(user=request.user, params=request.data).add()

        return Response(status=queryset)


def news_report_download(request, cid):

    fields = NewsReport.objects.filter(id=cid).values('file', 'year', 'period', 'news_type')[0]

    try:
        response = FileResponse(open(fields['file'], 'rb'))
        response['Content-Type'] ='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response['Content-Disposition'] = 'attachment; filename=report.docx'

        return response
    except Exception as e:
        return Response(str(e))


class NewsReportDeleteView(BaseView):

    def __init__(self):
        super(NewsReportDeleteView, self).__init__()

    def set_request(self, request):
        super(NewsReportDeleteView, self).set_request(request)

    def delete(self, request, cid):
        self.set_request(request)

        queryset = NewsReportDelete(user=request.user, params=request.data).delete(cid=cid)

        return Response(status=queryset)


class StatisticsView(BaseView):
    def __init__(self):
        super(StatisticsView, self).__init__()

    def serialize(self, result):

        data = {
            'list': map(lambda r :{
                'user': r['user'],
                'times': r['times'],
            }, result)
        }

        return data

    def get(self, request):
        result = StatisticsShow(params = request.query_params).get_data()
        return Response(self.serialize(result))
