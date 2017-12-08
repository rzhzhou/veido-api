from observer.apps.seer.service.abstract import Abstract
from observer.apps.base.models import Inspection


class InspectionQuerySet(Abstract):  # 抽检信息

    def __init__(self, params={}):
        super(InspectionQuerySet, self).__init__(params)

    def get_all_inspection_list(self):
        fields = ('product', 'title', 'pubtime', 'source', 'qualitied', 'url', 'level', )
        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Inspection.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset
