from observer.apps.base.models import Inspection as BaseAInspection
from observer.apps.yqj.models import Inspection as YqjInspection
from observer.apps.seer.service.abstract import Abstract


class InspectionQuerySet(Abstract):#抽检信息

    def __init__(self, params={}):
        super(InspectionQuerySet, self).__init__(params)

    def get_all_inspection_list(self):

        fields = ('base_inspection',)
        uuids = YqjInspection.objects.all().values(*fields)
        fields = ('guid','product', 'title', 'pubtime', 'source','url',)
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseAInspection.objects.filter(**args).values(*fields).order_by('-pubtime')
        return queryset