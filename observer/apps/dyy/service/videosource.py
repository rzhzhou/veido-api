from observer.apps.dyy.models import (Category, VideoType, Star, Director, VideoDetails, VideoContent)
from observer.apps.dyy.service.abstract import Abstract

class VideoSource(object):
	"""docstring for VideoSource"""
	def __init__(self):
		super(VideoSource, self).__init__()

	def get_all(self, vid):
		fields = ('name' , 'url', 'videodetails__thumb', 'videodetails__introduction', 'videodetails__score')

		queryset = VideoContent.objects.filter(videodetails_id = vid).values(*fields)
		print(queryset)

		return queryset





