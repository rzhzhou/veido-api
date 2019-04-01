import os
from datetime import datetime

from django.contrib.auth.models import Group, User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import FileResponse
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.base.models import (AliasIndustry, Inspection, Nav, NewsReport,
                                  UserInfo, UserNav, VersionRecord)
from observer.base.service.area import SelectAreaData
from observer.base.service.article import (ArticleData, RiskData, RiskDataAdd,
                                           RiskDataAudit, RiskDataDelete,
                                           RiskDataEdit, RiskDataExport,
                                           RiskDataSuzhou, RiskDataUpload,
                                           StatisticsShow, newsCrawlerData,
                                           RiskHarmsData, RiskHarmsManageSave,
                                           RiskHarmsDetailsData, EventsManageData,
                                           EventsDataUpload, EventsAnalysis)
from observer.base.service.base import (alias_industry, area, areas,
                                        categories, content,get_major_category,
                                        get_major_industry, get_user_extra,
                                        get_user_nav, involve_local,
                                        local_related, qualitied, gov_area,
                                        harmPeople, countPeople, harmName)

from observer.base.service.corpus import (CategoryListData, CorpusAdd,
                                          CorpusData, CorpusDelete, CorpusEdit,
                                          CrawlerData)
from observer.base.service.dashboard import DashboardData
from observer.base.service.desmon import (DMLinkAdd, DMLinkData, DMLinkDelete,
                                          DMLinkEdit, DMWordsData, DMWordsFocusData,
                                          DMWordsDelete, MonitorInformationData)
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
                                              InspectionDataUpload,
                                              InspectStatisticsData,
                                              InspectionDataNation,
                                              InspectionDataProAndCity,
                                              InspectionDataLocal,
                                              InspectionDataLocalExport,
                                              InspectionDataNationExport,
                                              InspectionDataProAndCityExport,
                                              )
from observer.base.service.navbar import NavBarEdit
from observer.base.service.news import NewsAdd, NewsDelete, NewsEdit, ViewsData
from observer.base.service.report import (NewsReportData, NewsReportDelete,
                                          NewsReportSuzhou, NewsReportUpload)
from observer.base.service.search import SearchAdvancedData, SearchData
from observer.base.service.user import (GroupData, UserAdd, UserData,
                                        UserDelete, UserEdit, ThemeEdit)
from observer.base.service.version import (VersionRecordData,
                                           VersionRecordDataAdd,
                                           VersionRecordDataDelete,
                                           VersionRecordDataEdit)
from observer.utils.date_format import date_format
from observer.utils.excel import write_by_openpyxl

from observer.base.service.govreports import (GovReportsData, GovReportsAdd, GovReportsDelete,
                                             GovReportsEdit)
from observer.base.service.indicatordata import IndicatorData,IndicatorDelete,IndicatorDataUpload,IndicatorDataExport
from observer.base.service.indicator import IndicatorChart,IndicatorRanking
from observer.base.service.policyregion import  (PolicyAreaData,PolicyAreaTotalData,PolicyAreaAdd,
                                                PolicyPrivateData,PolicPrivatelTotalData,PolicPrivatelAdd,
                                                PolicyIndustryData,PolicyIndustryTotalData,PolicyIndustryAdd)

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
    # 0005---风险伤害

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

    def serialize0005(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'id': x['id'],
                'url': x['url'],
                'title': x['title'],
                'source': x['source'],
                'score': x['score'],
                'areas': areas(x['id']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'people': countPeople(x['harm__id']),
            }, result),
        }

        return data

    def get(self, request, category):
        self.set_request(request)

        queryset = ArticleData(params=request.query_params, category=category).get_all()

        return Response(eval('self.serialize%s' % category)(queryset))


class EventView(APIView):

    def __init__(self):
        super(EventView, self).__init__()

    def serialize(self, result):
        data = map(lambda r: {
            'title': r['title'],
            'socialHarm': r['socialHarm'],
            'scope': r['scope'],
            'grading': r['grading'],
            'pubtime': r['pubtime'],
            'desc': r['desc'],
        }, result)

        return data
    
    def get(self, request, eid):
        result = EventsAnalysis().getEvent(eid = eid)

        return Response(self.serialize(result))


class EventInformationView(BaseView):

    def __init__(self):
        super(EventInformationView, self).__init__()

    def set_request(self, request):
        super(EventInformationView, self).set_request(request)

    def paging(self, queryset):
        return super(EventInformationView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15))

    def serialize(self, result):
        total = result.count()
        resultPage = self.paging(result)
        data = {
            'total': total,
            'list': map(lambda r: {
                'title': r['title'],
                'url': r['url'],
                'keyword': r['eventskeyword__name'],
                'source': r['source'],
                'pubtime': date_format(r['pubtime'], '%Y-%m-%d'),
                'sentiment': r['sentiment'],
            }, resultPage)
        }

        return data

    def get(self, result, eid):
        result = EventsAnalysis().get_data(eid = eid)

        return Response(self.serialize(result))


class EventContentView(APIView):

    def __init__(self):
        super(EventContentView, self).__init__()

    def serialize(self, sentiment, source, areas, keywords):
        data = {
            'sentimentList': map(lambda s: {
                'sentiment': s['sentiment'],
            }, sentiment),

            'source': map(lambda s: {
                'name': s['articles__source'],
                'sum': s['num_source'],
            }, source),

            'areas': map(lambda a: {
                'name': a['name'],
                'sum': a['sum'],
            }, areas),

            'keywords': map(lambda k: {
                'name': k['name'],
                'sum': k['num_eventskeyword'],
            }, keywords),
        }

        return data

    def get(self, request, eid):
        sentiment = EventsAnalysis().getSentiment(eid = eid)
        source = EventsAnalysis().getSource(eid = eid)
        areas = EventsAnalysis().getAreas(eid = eid)
        keywords = EventsAnalysis().getKeywords(eid = eid)

        return Response(self.serialize(sentiment, source, areas, keywords))


class EventSpreadView(APIView):

    def __init__(self):
        super(EventSpreadView, self).__init__()

    def serialize(self, timeTrend, trend):
        data = {
            'time': map(lambda t: {
                'timeTrend': date_format(t['articles__pubtime'], '%Y-%m-%d'),
            }, timeTrend),

            'trend': map(lambda t: {
                'name': t['name'],
                'numTrend': t['numTrend'],
            }, trend),
        }

        return data

    def get(self, request, eid):
        timeTrend = EventsAnalysis().getTimeTrend(eid = eid)
        trend = EventsAnalysis().getTrend(eid = eid)
        # way = EventsAnalysis().getWay(eid = eid)

        return Response(self.serialize(timeTrend, trend))

        
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
                'industry': {'id': x['industry'], 'name': x['industry__name']},
                'origin_product': x['origin_product'],
                'url': x['url'],
                'level': x['level'],
                'area': {'id': x['area'], 'name': x['area__name']},
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


class InspectStatisticsView(BaseView):
    def __init__(self):
        super(InspectStatisticsView, self).__init__()

    def serialize(self, result):

        data = result

        return data

    def get(self, request):

        result = InspectStatisticsData(params = request.query_params).get_statistics_data()

        return Response(self.serialize(result))


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


class SelectCccIndustriesView(BaseView):

    def __init__(self):
        super(SelectCccIndustriesView, self).__init__()

    def set_request(self, request):
        super(SelectCccIndustriesView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'name': '%s - %s' % (x['id'], x['name']),
            },
            queryset
        )

        return data

    def get(self, request):
        self.set_request(request)

        queryset = CCCIndustryData(params=request.query_params).get_level()

        return Response(self.serialize(queryset))


class SelectCpcIndustriesView(BaseView):

    def __init__(self):
        super(SelectCpcIndustriesView, self).__init__()

    def set_request(self, request):
        super(SelectCpcIndustriesView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'name': '%s - %s' % (x['id'], x['name']),
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


class SelectLicenceListView(BaseView):

    def __init__(self):
        super(SelectLicenceListView, self).__init__()

    def set_request(self, request):
        super(SelectLicenceListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'name': '%s - %s' % (x['id'], x['name']),
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


class SelectConsumerListView(BaseView):

    def __init__(self):
        super(SelectConsumerListView, self).__init__()

    def set_request(self, request):
        super(SelectConsumerListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'name': '%s - %s' % (x['id'], x['name']),
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
                'consumer': x['consumer'],
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


class SelectMajorListView(BaseView):

    def __init__(self):
        super(SelectMajorListView, self).__init__()

    def set_request(self, request):
        super(SelectMajorListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'name': x['name'],
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
                'id': r['id'],
                'keyword': r['keyword'],
                'startTime': r['startTime'],
                'endTime': r['stopTime'],
            }, results)
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = DMWordsFocusData(user = request.user).get_all()

        return Response(self.serialize(queryset))


class DMWordsDelView(BaseView):

    def __init__(self):
        super(DMWordsDelView, self).__init__()

    def set_request(self, request):
        super(DMWordsDelView, self).set_request(request)

    def delete(self, request, did):
        queryset = DMWordsDelete(user=request.user).delete(did=did)

        return Response(status=queryset)


class MonitorInformationView(BaseView):
    def __init__(self):
        super(MonitorInformationView, self).__init__()

    def set_request(self, request):
        super(MonitorInformationView, self).set_request(request)

    def paging(self, queryset):
        return super(MonitorInformationView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda r: {
                'title': r['title'],
                'url': r['url'],
                'source': r['source'],
                'area': r['areas__name'],
                'time': date_format(r['pubtime'], '%Y-%m-%d'),
            }, result)
        }

        return data

    def get(self, request, did):
        queryset = MonitorInformationData(user = request.user).get_all(did=did)

        return Response(self.serialize(queryset))


class SelectIndustryView(BaseView):

    def __init__(self):
        super(SelectIndustryView, self).__init__()

    def set_request(self, request):
        super(SelectIndustryView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'name': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = Select2IndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class SelectAliasIndustryView(BaseView):

    def __init__(self):
        super(SelectAliasIndustryView, self).__init__()

    def set_request(self, request):
        super(SelectAliasIndustryView, self).set_request(request)

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


class SelectAreaView(BaseView):

    def __init__(self):
        super(SelectAreaView, self).__init__()

    def set_request(self, request):
        super(SelectAreaView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'name': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = SelectAreaData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class SelectIndustryProductsView(BaseView):

    def __init__(self):
        super(SelectIndustryProductsView, self).__init__()

    def set_request(self, request):
        super(SelectIndustryProductsView, self).set_request(request)

    def serialize(self, queryset):
        data = map(lambda q: {
            'id': q['id'],
            'name': q['name'],
        }, queryset)

        return data

    def get(self, request):
        self.set_request(request)

        queryset = IndustryProductsData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class SelectGroupView(BaseView):

    def __init__(self):
        super(SelectGroupView, self).__init__()

    def set_request(self, request):
        super(SelectGroupView, self).set_request(request)

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
                'keyword': '无' if not x['corpus__keyword'] else x['corpus__keyword'],
                'industry_name': '无' if x['industry__name'] == 'None' else x['industry__name'],
                'industry_parent_name': '无' if x['industry__name'] == 'None' else x['industry__parent__name'],
                'categories': categories(x['id'], admin=True),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                'status': x['status'],
                'harm': '无' if not x['harm__id'] else '已存在',
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
            RiskDataExport(params=request.query_params, user=request.user).export(),
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
                'industry': {'id': x['industry'], 'name': x['industry__name']},
                'origin_product': x['origin_product'],
                'url': x['url'],
                'level': x['level'],
                'area': {'id': x['area'], 'name': x['area__name']},
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
                'industry': {'id':x['inspection__industry'], 'name':x['inspection__industry__name']},
                'product_name': x['inspection__product_name'],
                'source': x['inspection__source'],
                'enterprise': x['name'],
                'area': {'id': x['area'], 'name': x['area__name']},
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
            InspectionDataExport(params=request.query_params, user=request.user).export(),
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
                'industry': {'id': -1, 'name': '无'} if r['industry_id'] == -1 else get_major_industry(r['industry_id']),
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


class SelectCategoryListView(BaseView):

    def __init__(self):
        super(SelectCategoryListView, self).__init__()

    def set_request(self, request):
        super(SelectCategoryListView, self).set_request(request)

    def read_category(self, results):

        data = map(lambda r : {

                'id': r['id'],
                'name': r['name'],

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
                'areas': areas(x['id']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'score': x['score'],
                'local_related': local_related(x['id'], self.user), # 本地风险相关度
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
                            'href': '' if not title['href'] else title['href'],
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


class RouteDataView(BaseView):

    def __init__(self):
        super(RouteDataView, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(RouteDataView, self).set_request(request)

    def serialize(self):
        routers = []
        u_navs_ids = UserNav.objects.filter(user=self.user).values_list('nav', flat=True)
        routes = Nav.objects.filter(id__in=u_navs_ids).exclude(level=1).values('id', 'href', 'component').order_by('index')
        j = 0
        for i, route in enumerate(routes):
            if route['href'] == '':
                j+=1
            else:
                routers.append({
                    'path': route['href'],
                    'alias': '/' if i - j == 0 else '',
                    'component': route['component'],
                })
        data = {
            'routers': routers,
        }

        return data

    def get(self, request):
        self.set_request(request)

        return Response(self.serialize())


class ThemeView(BaseView):

    def __init__(self):
        super(ThemeView, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(ThemeView, self).set_request(request)

    def serialize(self):
        user_theme = UserInfo.objects.get(user_id=self.user).theme

        data = {
            'user_theme': user_theme,
        }

        return data

    def get(self, request):
        self.set_request(request)

        return Response(self.serialize())


class ThemeEditView(BaseView):

    def __init__(self):
        super(ThemeEditView, self).__init__()

    def set_request(self, request):
        self.user = request.user
        super(ThemeEditView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        theme = getattr(self, 'theme', '')

        queryset = ThemeEdit(user=request.user, params=request.data).edit()

        return Response(queryset)


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


class VersionRecordDataView(BaseView):

    def __init__(self):
        super(VersionRecordDataView, self).__init__()

    def set_request(self, request):
        super(VersionRecordDataView, self).set_request(request)

    def paging(self, queryset):
        return super(VersionRecordDataView, self).paging(
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
                'version': x['version'],
                'content': x['content'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d %T'),
            }, result),
        }

        return data

    def get(self, request):
        self.set_request(request)

        queryset = VersionRecordData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class VersionRecordDataAddView(BaseView):

    def __init__(self):
        super(VersionRecordDataAddView, self).__init__()

    def set_request(self, request):
        super(VersionRecordDataAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = VersionRecordDataAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class VersionRecordDataDeleteView(BaseView):
    def __init__(self):
        super(VersionRecordDataDeleteView, self).__init__()

    def set_request(self, request):
        super(VersionRecordDataDeleteView, self).set_request(request)

    def delete(self, request, cid):
        self.set_request(request)

        queryset = VersionRecordDataDelete(user=request.user).delete(cid=cid)

        return Response(status=queryset)


class VersionRecordDataEditView(BaseView):
    def __init__(self):
        super(VersionRecordDataEditView, self).__init__()

    def set_request(self, request):
        super(VersionRecordDataEditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = VersionRecordDataEdit(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class InspectionDataNationView(BaseView):
    def __init__(self):
        super(InspectionDataNationView, self).__init__()

    def set_request(self, request):
        super(InspectionDataNationView, self).set_request(request)

    def paging(self, queryset):
        return super(InspectionDataNationView, self).paging(
            queryset, self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 500))

    def serialize(self, queryset, request):
        areaname = User.objects.filter(username=request.user).values('userarea__area__name')
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'industry':x['inspection__industry__name'],
                'unitem': x['unitem'],
                'area':x['area__name'],
                'involve': involve_local(areaname[0]['userarea__area__name'], x['area__name']),
                # 'pubtime': x['inspection__pubtime'],
            }, result),
        }
        return data

    def get(self, request):
        self.set_request(request)

        queryset = InspectionDataNation(params=request.query_params).get_all()

        return Response(self.serialize(queryset,request))


class InspectionDataProAndCityView(BaseView):
    def __init__(self):
        super(InspectionDataProAndCityView, self).__init__()

    def set_request(self, request):
        super(InspectionDataProAndCityView, self).set_request(request)

    def paging(self, queryset):
        return super(InspectionDataProAndCityView, self).paging(
            queryset, self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'industry':x['industry__name'],
                'qualified':str(round(float(x['qualitied'])*100,2))+'%',
                'source':x['source'],
                'pubtime':x['pubtime']
            }, result),
        }
        return data

    def get(self, request):
        self.set_request(request)

        queryset = InspectionDataProAndCity(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class InspectionDataLocalView(BaseView):
    def __init__(self):
        super(InspectionDataLocalView, self).__init__()

    def set_request(self, request):
        super(InspectionDataLocalView, self).set_request(request)

    def paging(self, queryset):
        return super(InspectionDataLocalView, self).paging(
            queryset, self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15))

    def serialize(self, queryset):
        total = queryset.count()
        result = self.paging(queryset)
        data = {
            'total': total,
            'list': map(lambda x: {
                'industry':x['inspection__industry__name'],
                'enterprise':x['name'],
                'unitem':x['unitem'],
                'source':x['inspection__source']
            }, result),
        }
        return data

    def get(self, request):
        self.set_request(request)

        queryset = InspectionDataLocal(user=request.user, params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class InspectionDataLocalExportView(BaseView):
    def __init__(self):
        super(InspectionDataLocalExportView, self).__init__()

    def get(self, request):
        response = FileResponse(
            InspectionDataLocalExport(user=request.user, params=request.query_params).export(),
            content_type='application/vnd.ms-excel'
        )
        filename = datetime.now().strftime("%Y%m%d%H%M%S")+'_Local_Inspections'+'.xlsx'
        response["Content-Disposition"] = 'attachment; filename='+filename

        return response


class InspectionDataProAndCityExportView(BaseView):
    def __init__(self):
        super(InspectionDataProAndCityExportView, self).__init__()

    def get(self, request):
        response = FileResponse(
            InspectionDataProAndCityExport(user=request.user, params=request.query_params).export(),
            content_type='application/vnd.ms-excel'
        )
        filename = datetime.now().strftime("%Y%m%d%H%M%S")+'_Province_City_Inspections'+'.xlsx'
        response["Content-Disposition"] = 'attachment; filename='+filename

        return response


class InspectionDataNationExportView(BaseView):
    def __init__(self):
        super(InspectionDataNationExportView, self).__init__()

    def get(self, request):
        response = FileResponse(
            InspectionDataNationExport(user=request.user, params=request.query_params).export(),
            content_type='application/vnd.ms-excel'
        )
        filename = datetime.now().strftime("%Y%m%d%H%M%S")+'_Nation_Inspections'+'.xlsx'
        response["Content-Disposition"] = 'attachment; filename='+filename

        return response


class EventsManageView(BaseView):
    def __init__(self):
        super(EventsManageView, self).__init__()

    def set_request(self, request):
        super(EventsManageView, self).set_request(request)

    def paging(self, queryset):
        return super(EventsManageView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, result):
        total = result.count()
        resultPage = self.paging(result)
        data = {
            'total': total,
            'list': map(lambda r : {
                'id': r['id'],
                'title': r['title'],
                'socialHarm': r['socialHarm'],
                'scope': r['scope'],
                'grading': r['grading'],
                'pubtime': date_format(r['pubtime'], "%Y-%m-%d"),
                'desc': r['desc']
            }, resultPage)
        }

        return data
        
    def get(self, request):
        result = EventsManageData(params = request.query_params).get_data()

        return Response(self.serialize(result))


class EventsSaveView(BaseView):

    def __init__(self):
        super(EventsSaveView, self).__init__()

    def post(self, request):
        status = EventsManageData(params = request.data).toSave()

        return Response(status)


class EventsDeleteView(BaseView):

    def __init__(self):
        super(EventsDeleteView, self).__init__()

    def delete(self, request, eid):
        status = EventsManageData(params = request.data).toDel(eid = eid)

        return Response(status)


class EventsUpdataView(BaseView):

    def __init__(self):
        super(EventsUpdataView, self).__init__()

    def post(self, request):
        status = EventsManageData(params = request.data).toUpd()

        return Response(status)


class EventsDataView(BaseView):

    def __init__(self):
        super(EventsDataView, self).__init__()

    def set_request(self, request):
        super(EventsDataView, self).set_request(request)

    def paging(self, queryset):
        return super(EventsDataView, self).paging(
            queryset,
            self.request.query_params.get('page', 1),
            self.request.query_params.get('length', 15)
        )

    def serialize(self, result):
        total = result.count()
        resultPage = self.paging(result)
        data = {
            'total': total,
            'list': map(lambda r: {
                'id': r['id'],
                'title': r['title'],
                'url': r['url'],
                'pubtime': date_format(r['pubtime'], '%Y-%m-%d %H:%M:%S'),
                'source': r['source'],
                'areas': areas(r['id']),
                'keyword': r['eventskeyword__name'],
            }, resultPage)
        }

        return data

    def get(self, request, eid):
        result = EventsManageData(params = request.query_params).LinkData(eid = eid)

        return Response(self.serialize(result))


class EventsUploadView(BaseView):

    def __init__(self):
        super(EventsUploadView, self).__init__()

    def put(self, request, filename, format=None):
        queryset = EventsDataUpload(user=request.user).upload(filename, request.FILES['file'])

        return Response(queryset)


class RiskHarmsManageView(BaseView):
    def __init__(self):
        super(RiskHarmsManageView, self).__init__()

    def post(self, request):

        status = RiskHarmsManageSave(params=request.data).toSave()
        return Response(status=status)


class RiskHarmsDetailsView(BaseView):

    def __init__(self):
        super(RiskHarmsDetailsView, self).__init__()

    def serialize(self, result):

        data = {
            'list': map(lambda r: {
                'productName': '无' if r['article__industry__name'] == 'None' else r['article__industry__name'],
                'usingEnvironment': harmName(r['environment']),
                'temporalMotion': harmName(r['activity']),
                'people': harmPeople(r['id']),
                'psyandphy': harmName(r['mind_body']),
                'behFactors': harmName(r['behavior']),
                'indoorEnvironment': harmName(r['indoor']),
                'outdoorEnvironment': harmName(r['outdoor']),
                'phyHarm': harmName(r['physics']),
                'chemicalHarm': harmName(r['chemical']),
                'biologicalHarm': harmName(r['biology']),
                'damageTypes': harmName(r['damage_types']),
                'degree_damage': harmName(r['damage_degree']),
                'damageReason': harmName(r['damage_reason']),
            }, result),
        }

        return data

    def get(self, request):

        result = RiskHarmsDetailsData(params=request.query_params).get_data()
        return Response(self.serialize(result))


class RiskHarmsView(BaseView):
    def __init__(self):
        super(RiskHarmsView, self).__init__()

    def serialize(self, result):
        data = {
            'list': map(lambda r : {
                'id': r['id'],
                'name': r['name'],
            }, result)
        }

        return data

    def get(self, request):
        result = RiskHarmsData(params=request.query_params).get_data()

        return Response(self.serialize(result))


class GovReportsView(BaseView):

    def __init__(self):
        super(GovReportsView, self).__init__()

    def set_request(self, request):
        super(GovReportsView, self).set_request(request)

    def paging(self, queryset):
        return super(GovReportsView, self).paging(
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
                'level': r['area__level'],
                'year': r['year'],
                'areas': gov_area(r['area_id']),
                'content': r['content'],
            }, results)
        }

        return data

    def get(self, request):

        self.set_request(request)

        queryset = GovReportsData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class GovReportsAddView(BaseView):

    def __init__(self):
        super(GovReportsAddView, self).__init__()

    def set_request(self, request):
        super(GovReportsAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = GovReportsAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class GovReportsDeleteView(BaseView):
    def __init__(self):
        super(GovReportsDeleteView, self).__init__()

    def set_request(self, request):
        super(GovReportsDeleteView, self).set_request(request)

    def delete(self, request, cid):
        self.set_request(request)

        queryset = GovReportsDelete(user=request.user, params=request.data).delete(cid=cid)

        return Response(status=queryset)


class GovReportsEditView(BaseView):

    def __init__(self):
        super(GovReportsEditView, self).__init__()

    def set_request(self, request):
        super(GovReportsEditView, self).set_request(request)

    def post(self, request, cid):
        self.set_request(request)

        queryset = GovReportsEdit(user=request.user, params=request.data).edit(cid=cid)

        return Response(status=queryset)


class IndicatordataparentView(BaseView):

    def __init__(self):
        super(IndicatordataparentView, self).__init__()

    def set_request(self, request):
        super(IndicatordataparentView, self).set_request(request)

    def paging(self, queryset):
        return super(IndicatordataparentView, self).paging(
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
                'name': r['indicator__name'],
                'level': r['indicator__level'],
                'parenttwo': r['indicator__parent_id__name'],
                'parentone': r['indicator__parent_id__parent_id__name'],
                'value': r['value'],
                'unit': r['indicator__unit'],
                'areas': area(r['area__id']),
                'year': r['year'],
            }, results)
        }

        return data

    def get(self, request):

        self.set_request(request)

        queryset = IndicatorData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class IndicatordataparentDeleteView(BaseView):
    def __init__(self):
        super(IndicatordataparentDeleteView, self).__init__()

    def set_request(self, request):
        super(IndicatordataparentDeleteView, self).set_request(request)

    def delete(self, request, cid):
        self.set_request(request)

        queryset = IndicatorDelete(user=request.user, params=request.data).delete(cid=cid)

        return Response(status=queryset)


class SelectIndicatorListView(BaseView):

    def __init__(self):
        super(SelectIndicatorListView, self).__init__()

    def set_request(self, request):
        super(SelectIndicatorListView, self).set_request(request)

    def serialize(self, queryset):
        data = map(
            lambda x: {
                'id': x['id'],
                'name': x['name'],
            },
            queryset
        )

        return data

    def get(self, request):
        self.set_request(request)

        queryset = IndicatorData(params=request.query_params).get_level()

        return Response(self.serialize(queryset))


class IndicatordataparentDataUploadView(BaseView):
    parser_classes = (FileUploadParser,)

    def __init__(self):
        super(IndicatordataparentDataUploadView, self).__init__()

    def put(self, request, filename, format=None):

        queryset = IndicatorDataUpload(user=request.user).upload(filename, request.FILES['file'])

        return Response(queryset)


class IndicatordataparentDataExportView(BaseView):

    def __init__(self):
        super(IndicatordataparentDataExportView, self).__init__()

    def get(self, request):
        response = FileResponse(
            IndicatorDataExport(params=request.query_params, user=request.user).export(),
            content_type='application/vnd.ms-excel'
        )
        response["Content-Disposition"] = 'attachment; filename=indicator.xlsx'

        return response


class IndicatorView(BaseView):

    def __init__(self):
        super(IndicatorView, self).__init__()

    def set_request(self, request):
        super(IndicatorView, self).set_request(request)

    def paging(self, queryset):
        return super(IndicatorView, self).paging(
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
                'onename':r['parent_id__parent_id__name'],
                'twoname': r['parent_id__name'],
                'name': r['name'],
            }, results)
        }

        return data

    def get(self, request):

        self.set_request(request)

        queryset = IndicatorChart(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class IndicatorscoreView(BaseView):

    def __init__(self):
        super(IndicatorscoreView, self).__init__()

    def set_request(self, request):
        super(IndicatorscoreView, self).set_request(request)

    def paging(self, queryset):
        return super(IndicatorscoreView, self).paging(
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
                'value': r['value'],
                'areas': area(r['area_id']),
                'year': r['year'],
                'indicator_name': r['indicator_id__name'],
                'indicator_id': r['indicator_id']
            }, results)
        }

        return data

    def get(self, request, cid):

        self.set_request(request)

        queryset = IndicatorRanking(params=request.query_params).get_all(cid=cid)

        return Response(self.serialize(queryset))


class PolicyAreaView(BaseView):

    def __init__(self):
        super(PolicyAreaView, self).__init__()

    def set_request(self, request):
        super(PolicyAreaView, self).set_request(request)

    def paging(self, queryset):
        return super(PolicyAreaView, self).paging(
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
                'areas': area(r['area__id']),
                'total': r['total'],
                'year': date_format(r['year'], '%Y-%m-%d %H:%M:%S'),
            }, results)
        }

        return data

    def get(self, request):

        self.set_request(request)

        queryset = PolicyAreaData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class PolicyAreaTotalView(BaseView):

    def __init__(self):
        super(PolicyAreaTotalView, self).__init__()

    def set_request(self, request):
        super(PolicyAreaTotalView, self).set_request(request)

    def paging(self, queryset):
        return super(PolicyAreaTotalView, self).paging(
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
                'name': r['policys__name'],
            }, results)
        }

        return data

    def get(self, request, pid):

        self.set_request(request)

        queryset = PolicyAreaTotalData(params=request.query_params).get_all(pid=pid)

        return Response(self.serialize(queryset))


class PolicyRegionAddView(BaseView):

    def __init__(self):
        super(PolicyRegionAddView, self).__init__()

    def set_request(self, request):
        super(PolicyRegionAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = PolicyAreaAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class PolicPrivatelView(BaseView):

    def __init__(self):
        super(PolicPrivatelView, self).__init__()

    def set_request(self, request):
        super(PolicPrivatelView, self).set_request(request)

    def paging(self, queryset):
        return super(PolicPrivatelView, self).paging(
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
                'areas': area(r['area__id']),
                'total': r['total'],
                'year': date_format(r['year'], '%Y-%m-%d %H:%M:%S'),
            }, results)
        }

        return data

    def get(self, request):

        self.set_request(request)

        queryset = PolicyPrivateData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class PolicPrivatelTotalView(BaseView):

    def __init__(self):
        super(PolicPrivatelTotalView, self).__init__()

    def set_request(self, request):
        super(PolicPrivatelTotalView, self).set_request(request)

    def paging(self, queryset):
        return super(PolicPrivatelTotalView, self).paging(
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
                'name': r['policys__name'],
            }, results)
        }

        return data

    def get(self, request, pid):

        self.set_request(request)

        queryset = PolicPrivatelTotalData(params=request.query_params).get_all(pid=pid)

        return Response(self.serialize(queryset))


class PolicPrivatelAddView(BaseView):

    def __init__(self):
        super(PolicPrivatelAddView, self).__init__()

    def set_request(self, request):
        super(PolicPrivatelAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = PolicPrivatelAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)


class PolicyIndustryView(BaseView):

    def __init__(self):
        super(PolicyIndustryView, self).__init__()

    def set_request(self, request):
        super(PolicyIndustryView, self).set_request(request)

    def paging(self, queryset):
        return super(PolicyIndustryView, self).paging(
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
                'areas': area(r['area__id']),
                'industry_class': r['industry_class'],
                'total': r['total'],
                'year': date_format(r['year'], '%Y-%m-%d %H:%M:%S'),
            }, results)
        }

        return data

    def get(self, request):

        self.set_request(request)

        queryset = PolicyIndustryData(params=request.query_params).get_all()

        return Response(self.serialize(queryset))


class PolicyIndustryTotalView(BaseView):

    def __init__(self):
        super(PolicyIndustryTotalView, self).__init__()

    def set_request(self, request):
        super(PolicyIndustryTotalView, self).set_request(request)

    def paging(self, queryset):
        return super(PolicyIndustryTotalView, self).paging(
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
                'name': r['policys__name'],
            }, results)
        }

        return data

    def get(self, request, pid):

        self.set_request(request)

        queryset = PolicyIndustryTotalData(params=request.query_params).get_all(pid=pid)

        return Response(self.serialize(queryset))


class PolicyIndustryAddView(BaseView):

    def __init__(self):
        super(PolicyIndustryAddView, self).__init__()

    def set_request(self, request):
        super(PolicyIndustryAddView, self).set_request(request)

    def post(self, request):
        self.set_request(request)

        queryset = PolicyIndustryAdd(user=request.user, params=request.data).add()

        return Response(status=queryset)
