"""
    keep alive with 'http://192.168.10.215' connection
"""

from django_extensions.management.jobs import MinutelyJob
import requests
from datetime import datetime, timedelta
from json import loads
from cPickle import dump, load


class Job(MinutelyJob):

    __login_cookie = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2l"\
        "kIjoxLCJ1c2VyX2lkIjoxLCJhX25hbWUiOiJ3dWhhbnpoaWppYW4iLCJhX3JlYWx"\
        "uYW1lIjoi566h55CG5ZGYIiwiYV9wd2QiOiI3YjNkNzgzMzFlNDQ0YzNmODBkO"\
        "Dc1Njc4YjA1ODkyYmFiMmY1MTU3IiwiYV9waG9uZSI6bnVsbCwiYV9lbWFpbCI6"\
        "Ind1aGFuemhpamlhbkBzaGVuZHUuaW5mbyIsImFfbG9nbyI6bnVsbCwic3Rh"\
        "dHVzIjoxLCJzeXN0ZW1faWQiOjEsImlzcm9vdCI6MSwiU3lzQWNjb3VudFNhbHQiO"\
        "nsic2FsdCI6ImZjMDhlNDFlZjkzZjIwYTYyYjhmY2I4ODc1ZThmNTJmZTJkZGExYTkifX0.x4IP"\
        "k4Cnka7Z2izoZ2uTMjh7lzpsrJA3zs7hWTqnhFk"

    def execute(self):
        sd = datetime.utcnow()
        ed = sd - timedelta(days=30)
        sd_str = sd.strftime("%Y-%m-%d")
        ed_str = ed.strftime("%Y-%m-%d")
        day_id = self.get_day_id(sd_str, ed_str)
        if not day_id:
            day_id = self.get_day_id(sd_str, ed_str)
        data = self.get_data(sd_str, day_id[0]["date_id"], ed_str, day_id[1]["date_id"])
        if not data:
            data = self.get_data(sd_str, day_id[0]["date_id"], ed_str, day_id[1]["date_id"])
        if not data:
            print "error"
        else:
            dump(data, file("map.json", "w")) 
            print "success"   

    def get_data(self, start_day, start_id, end_day, end_id):
        url = "http://192.168.0.215/api/dashboard?sd=%s&sdId=%s&ed=%s&edId=%s" % (start_day, start_id, end_day, end_id)
        headers = {
            "Authorization" : "Bearer "+self.__login_cookie,
        }
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None
        return loads(res.text)

    def get_day_id(self, start_day, end_day):
        day_id = []
        url = "http://192.168.0.215/api/product/queryDateId?endDate=%s&startDate=%s" % (start_day, end_day)
        headers = {
            "Authorization" : "Bearer " + self.__login_cookie,
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            day_id = loads(res.text)["data"]     
        return day_id


if __name__ == '__main__':
    Job().execute()


