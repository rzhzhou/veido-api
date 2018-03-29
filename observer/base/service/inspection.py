from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import(Inspection, )
from observer.base.service.abstract import Abstract


class InspectionData(Abstract):

    def __init__(self, params):
        super(InspectionData, self).__init__(params)

    def get_all(self):

        fields = ('title', 'url', 'pubtime', 'source', 'unitem', 'qualitied', 'category', 'level', 'industry_id', 'area_id', )

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            # 'qualitied__gte': getattr(self, 'starttime', None),
            # 'qualitied__lt': getattr(self, 'endtime', None),
            'category__contains': getattr(self, 'category', None),
            'level': getattr(self, 'level', None),
            'area': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Inspection.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset
