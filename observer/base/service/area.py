from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Area, )
from observer.base.service.abstract import Abstract
from observer.utils.date_format import date_format


class Select2AreaData(Abstract):

    def __init__(self, params):
        super(Select2AreaData, self).__init__(params)

    def get_all(self):
        fields = ('id', 'name', )

        cond = {
            'name__istartswith': getattr(self, 'text', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Area.objects.filter(**args).values(*fields)

        return queryset