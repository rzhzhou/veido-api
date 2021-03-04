from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django_extensions.admin import ForeignKeyAutocompleteAdmin
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import permission_classes
from observer.apps.dyy.service.videosource import VideoSource
from observer.utils.date_format import date_format
from observer.apps.dyy.service.base import is_task_created
import json

# Create your views here.

class BaseView(APIView):

    def __init__(self):
        self.request = None

    def set_request(self, request):
        self.request = request

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


class VideoSourceView(APIView):

    def __init__(self):
        super(VideoSourceView, self).__init__()

    def serialize(self, result):
        data = map(lambda r: {
            'name': r['name'],
            'url': r['url'],
            'thumb': r['videodetails__thumb'],
            'introduction': r['videodetails__introduction'],
            'score': r['videodetails__score'],
        }, result)

        return data
        # return result

    def get(self, request, vid):
        result = VideoSource().get_all(vid = vid)

        return Response(self.serialize(result))