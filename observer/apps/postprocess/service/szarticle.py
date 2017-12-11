from observer.apps.base.models import Area
from observer.apps.seer.models import AreaIndustry
from observer.apps.seer.service.abstract import Abstract
from datetime import datetime, timedelta
from django.db.models import Count
from observer.utils.date.convert import data_format


class RiskProductData(Abstract):  # 风险产品

    def __init__(self, params={}):
        super(RiskProductData, self).__init__(params)

    def get_all_news_list(self):

        # yqj article query
        fields = ('id', )
        cond = {
            'name': getattr(self, 'area_name', None),
            'level': getattr(self, 'level', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        area_id = Area.objects.filter(**args).values(*fields)
        area_id_list=Area.objects.filter(parent=area_id).values('id')
        
        # base article query
        fields = ('url', 'title', 'pubtime', 'source', 'reprinted', 'area', )
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(
            **args).values(*fields).order_by('-pubtime')

        return queryset