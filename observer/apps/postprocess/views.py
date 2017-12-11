from datetime import date, datetime, timedelta

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from observer.utils.date.convert import utc_to_local_time, data_format
from observer.apps.postprocess.service.szarticle import (RiskProductData,)

class BaseView(APIView):

    def __init__(self):
        self.today = date.today() + timedelta(days=1)
        self.query_params = {
            'starttime': self.today - timedelta(days=30),
            'endtime': self.today,
        }

    def set_params(self, params):
        for k, v in params.items():
            self.query_params[k] = v
        # self.start=self.query_params.get('start')

        # start, end convert to local datetime
        self.query_params['starttime'], self.query_params['endtime'] = utc_to_local_time(
            [self.query_params['starttime'], self.query_params['endtime']]
        )

        # end add 1 day
        self.query_params['endtime'] = self.query_params[
            'endtime'] + timedelta(days=1)

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


class RiskProductView(BaseView):  # 风险产品

    pass


class RiskEnterprisesView(BaseView):  # 风险企业

    pass


class RiskNewsView(BaseView):  # 风险新闻

    pass 


class RiskInspectionView(BaseView):  # 风险抽检

    pass


class WholeRiskView(BaseView):  # 整体风险变化趋势

    pass


class InternetRiskView(BaseView):  # 互联网风险数据变化趋势

    pass