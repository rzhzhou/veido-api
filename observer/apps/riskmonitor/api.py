# -*- coding: utf-8 -*-
from tests import test_tools
test_tools()
import pytz
from datetime import datetime, timedelta

from rest_framework.views import APIView
from django.conf import settings

from observer.apps.base.views import BaseTemplateView
from businesslogic.detail import *
from businesslogic.enterprise_rank import *
from businesslogic.homepage import *
from businesslogic.industry_track import *
from businesslogic.statistic import *

class DispatchView(APIView, BaseTemplateView):
	def get(self, request, id):
            type = 'homepage'
            func = getattr(globals()['DispatchView'](), type)
            return func(request, id)

	def homepage(self, request, id):
        #oprint 'ksfjlsfjsldjf'
            tz = pytz.timezone(settings.TIME_ZONE)
            start = tz.localize(datetime.strptime('2015-11-2', '%Y-%m-%d'))
            end = tz.localize(datetime.strptime('2015-11-9', '%Y-%m-%d'))
            start = end - timedelta(days=7) 
            HomeData(start, end).get_all() 
        #print HomeData().get_all()        

	def industry_track(self, request, id):
	    pass

	def enterprise_rank(self, request, id):
	    pass

	def statistic(self, request, id):
	    pass

	def detail(self, request, id):
	    pass
DispatchView().get('homepage', 3)
