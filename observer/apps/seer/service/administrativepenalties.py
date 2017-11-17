
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When, Max
from django.db.models import Q

from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class AdministrativePenaltiesQuerySet(Abstract):

    def __init__(self, params={}):
        super(AdministrativePenaltiesQuerySet, self).__init__(params)

    def get_administrativepenalties_list(self):
        fields = ('id', 'title', 'pubtime', 'url', 'publisher')
        
        administrative_penalties = AdministrativePenalties.objects.values(*fields)

        return administrative_penalties.filter(id__lte=administrative_penalties.aggregate(Max('id')).get('id__max')) 
