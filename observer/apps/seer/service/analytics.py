
from django.db.models import Count


from observer.apps.seer.service.abstract import Abstract
from observer.apps.seer.service.industry import IndustryTrack

from observer.apps.seer.models import AreaIndustry
from observer.apps.base.models import Enterprise


class AnalyticsCal(Abstract):

    def __init__(self, params={}):
        super(AnalyticsCal, self).__init__(params)
        self.industry_track = IndustryTrack(params)

    def get_filters(self):
        args = self.set_args()

        industries = AreaIndustry.objects.filter(
            user__id=self.user_id).values('id', 'name')

        enterprises = []

        products = []

        publishers = RiskNews.objects.filter(
            **args).values('publisher__id', 'publisher__name')

        return (industries, enterprises, products, publishers)

    def industry_chart(self):
        return self.industry_track.trend_chart()

    def cal_publisher_count(self):
        args = self.set_args()

        queryset = RiskNews.objects.filter(**args).values_list('publisher__name').annotate(
            Count('publisher__name')).order_by('-publisher__name__count')[:20]

        return queryset

    def get_chart(self):
        data = {
            'trend': self.industry_chart(),
            'bar': self.keywords_chart(num=10),
            'source': self.cal_publisher_count()
        }
        return data

    def get_all(self):
        chart_data = self.get_chart()
        chart_data['list'] = self.get_news_list()

        return chart_data
