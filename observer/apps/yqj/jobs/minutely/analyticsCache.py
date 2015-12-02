import sys
import os
import requests
import ConfigParser
from datetime import datetime, timedelta, date

from django.conf import settings
from django_extensions.management.jobs import BaseJob
from observer.utils.connector.redis import RedisQueryApi
reload(sys)
sys.setdefaultencoding( "utf-8" )

class Job(BaseJob):

    def Cache(self, datas):
        # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        # conf = ConfigParser.ConfigParser()
        # conf.read(os.path.join(BASE_DIR, "../../../analyticsCache.cfg"))
        # url_cfg = conf.get("master", "url")
        url_cfg = settings.CACHE

        if datas["hset_key"] == "date_range":
            RedisQueryApi().hset(datas["hset_name"], datas["hset_key"], {"start": datas["start"], "end": datas["end"]})
            return None

        url_cache = "%s/api/analytics/1/?type=%s&start=%s&end=%s&cache=0"\
            %(url_cfg, datas["hset_key"], datas["start"], datas["end"])
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }

        res = requests.post(
            url = "%s/api/login/"%url_cfg,
            data = {
            "username": datas["username"],
            "password": datas["password"]}
            )
        headers["Cookie"] = res.headers["set-cookie"]
        result = requests.get(url = url_cache, headers = headers)
        RedisQueryApi().hset(datas["hset_name"], datas["hset_key"], str(result.text))

    def UpdateTimeRange(self, cache, start, end):
        title = ["chart_weibo", "chart_trend", "chart_type", "chart_emotion", "date_range", "statistic"]
        for t in title:
            datas = {
                    "hset_name" : cache,
                    "hset_key" : t,
                    "start" : start,
                    "end" : end,
                    "username" : "wuhan",
                    "password" : "wuhan"
                }
            self.Cache(datas)


    def SevenDays(self):
        ISOFORMAT = '%Y-%m-%d'
        end_date = datetime.now()
        start_date = datetime.now() + timedelta(days=-6)
        start = start_date.strftime(ISOFORMAT)
        end = end_date.strftime(ISOFORMAT)

        self.UpdateTimeRange("CacheSevenDays", start, end)


    def ThrityDays(self):
        ISOFORMAT = '%Y-%m-%d'
        end_date = datetime.now()
        start_date = datetime.now() + timedelta(days=-29)
        start = start_date.strftime(ISOFORMAT)
        end = end_date.strftime(ISOFORMAT)

        self.UpdateTimeRange("CacheThrityDays", start, end)


    def ThisMonth(self):
        STARTDATE = '%Y-%m'
        ENDDATE = '%Y-%m-%d'
        date_now = datetime.now()
        start = date_now.strftime(STARTDATE)+"-01"
        end = date_now.strftime(ENDDATE)

        self.UpdateTimeRange("CacheThisMonth", start, end)


    def LastMonth(self):
        ISOFORMAT = '%Y-%m-%d'
        DAYS = '%d'
        YEAR = '%Y'
        MONTH = '%m'

        date_now = datetime.now()

        start_year = date_now.strftime(YEAR)
        start_month = int(date_now.strftime(MONTH))-1

        if 0 < start_month < 10:
            start_month = '0'+str(start_month)
        elif start_month == 0:
            start_month = 12

        start = start_year + "-" + start_month + "-01"

        end_date = date_now + timedelta(days = -(int(date_now.strftime(DAYS))))
        end = end_date.strftime(ISOFORMAT)
        self.UpdateTimeRange("CacheLastMonth", start, end)

    def execute(self):
        caches = ['SevenDays', 'ThrityDays', 'ThisMonth', 'LastMonth']
        # job = Job()
        for cache in caches:
            eval('self'+'.'+cache+"()")
