# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models import Case, IntegerField, Sum, When
from django.db.models import Q

from observer.apps.origin.models import Inspection
from observer.apps.seer.service.abstract import Abstract
from observer.utils.date.convert import utc_to_local_time


class InspectionQuerySet(Abstract):

    def __init__(self, params={}):
        super(InspectionQuerySet, self).__init__(params)

    def get_inspection_list(self):
        fields = ('id', 'title', 'pubtime', 'url', 'publisher__name', 'qualitied', 'product')

        keywords = getattr(self, 'search[value]', None)

        queryset = Inspection.objects.values(*fields)

        return queryset if not keywords else queryset.filter(Q(publisher__name__contains=keywords) | Q(title__contains=keywords))

