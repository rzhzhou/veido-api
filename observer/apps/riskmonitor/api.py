# -*- coding: utf-8 -*-
from tests import test_tools
test_tools()

from rest_framework.views import APIView

from observer.apps.base.views import BaseTemplateView
from businesslogic.detail import *
from businesslogic.enterprise_rank import *
from businesslogic.homepage import *
from businesslogic.industry_track import *
from businesslogic.statistic import *

class DispatchView(APIView, BaseTemplateView):
	def get(self, request, id):
		#container = self.requesthead()
		#type = contarner['type']
		func = getattr(globals()['DispatchView'](), type)
		return func(request, id)

	def homepage(self, request, id):
        #oprint 'ksfjlsfjsldjf'
            pass
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
