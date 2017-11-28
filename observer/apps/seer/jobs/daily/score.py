import time

from datetime import date, datetime, timedelta
from django_extensions.management.jobs import DailyJob

from observer.apps.origin.models import (Industry, IndustryScore, Area)
from observer.apps.seer.service.industry import IndustryTrack


class Job(DailyJob):

    def get_time_sequence(self):
        time_sequence_list = []

        def date_range(start, stop, step):
            while start < stop:
                yield start
                start += step

        for d in date_range(datetime(2010, 1, 1), datetime(2017, 5, 8), timedelta(hours=24)):
            time_sequence_list.append(d)

        return time_sequence_list

    def handle_data(self, area_name_list, time_sequence_list):
        for area_name in area_name_list:
            area = Area.objects.get(name=area_name)
            for index, item in enumerate(time_sequence_list):
                if index > 6:
                    start = time_sequence_list[index-7]
                    end = item
                    for data in IndustryTrack(params={'start':start, 'end':end, 'area_name':area_name, 'user_id':9}).get_industries():
                        industry = Industry.objects.get(id=data[0])
                        score = data[3]
                        if not IndustryScore.objects.filter(score=score, time=str(start)[0:10], area=area, industry=industry):
                            IndustryScore(score=score, time=str(start)[0:10], area=area, industry=industry).save()
                        
                        time.sleep(1)
                    print "EXCUTE { %s } < %s ~ %s > SUCCESS!" % (area_name, start, end)


    def all_day(self, area_name_list):
        self.handle_data(area_name_list, self.get_time_sequence())

    def one_day(self, area_name_list):
        now = datetime.now()
        time_sequence_list = (now, now+timedelta(days=-1), now+timedelta(days=-2), now+timedelta(days=-3), now+timedelta(days=-4), now+timedelta(days=-5), now+timedelta(days=-6), now+timedelta(days=-7),)
        self.handle_data(area_name_list, time_sequence_list)

    def execute(self):
        self.one_day(('苏州', '全国', '常州'))
