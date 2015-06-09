#coding: utf-8
from datetime import date, datetime, timedelta
import time
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from collections import defaultdict
from dateutil.relativedelta import relativedelta

seasons = [(u'第一季度', (date(1,  1,  1),  date(1,  3, 31))),
           (u'第二季度', (date(1,  4,  1),  date(1,  6, 30))),
           (u'第三季度', (date(1,  7,  1),  date(1,  9, 30))),
           (u'第四季度', (date(1,  10, 1),  date(1, 12, 31)))]


def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=1)
    for season, (start, end) in seasons:
        if start <= now <= end:
            return season
    assert 0, 'never happens'

def GetFirstDaySeason(now):
    if isinstance(now, datetime):
        now = now.date()
    nowtime = now.replace(year=1)
    for season, (start, end) in seasons:
        if start <= nowtime <= end:
            return datetime(now.year, start.month, start.day)
    assert 0, 'never happens'

def byYear(min_date, max_date, date_range, articles):
    negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
    timel = [ ]
    for art in articles:
        date = art.pubtime.date().year
        timel.append(date)
        factor = art.feeling_factor
        if factor > 0.8:
            positive[date] += 1
        elif factor < 0.2 and factor > 0:
            negative[date] += 1
        else:
            neutral[date] += 1
    time = [(max_date.year - i) for i in range(0,6,1)]
    time1 = time[:]
    time1.sort()

    data= {}
    data['negative'] = [ negative[date] for date in time1 ]
    data['positive'] = [positive[date] for date in time1 ]
    data['neutral'] = [neutral[date] for date in time1 ]
    data['date'] = time1
    print data['negative']
    return JsonResponse(data)

def bySeason(min_date, max_date, date_range, articles):
        #get first day of the current season
        current_date = GetFirstDaySeason(datetime.now()) #2015-4-1
        #only get recent 4 season data
        begin_date =  current_date - relativedelta(year=1) #0001-4-1
        negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
        for art in articles:
            date = GetFirstDaySeason(art.pubtime)
            if date < begin_date:
                continue
            factor = art.feeling_factor
            if factor > 0.9:
                positive[date] += 1
            elif factor < 0.1 and factor > 0:
                negative[date] += 1
            else:
                neutral[date] += 1
        start_time=GetFirstDaySeason(min_date)
        # #datetime.date(min_date.year,start_month,1)
        range_date = [ start_time + relativedelta(months=i) for i in range(0, 12, 3) ]                      
        data = {}
        data['negative'] = [ negative[date] for date in range_date]
        data['positive'] = [ positive[date] for date in range_date]
        data['neutral'] = [ neutral[date] for date in range_date]
        data['date'] = [ str(date.year) + get_season(date) for date in range_date]
        return JsonResponse(data)

def byMonths(min_date, max_date, date_range, articles):
            #get first day of the current month
        current_date = max_date.replace(day=1)
        #only get recent 6 months data
        begin_date =  current_date - relativedelta(months=6)
        negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
        for art in articles:
            date = art.pubtime.date().replace(day=1)
            if date < begin_date:
                continue
            factor = art.feeling_factor
            if factor > 0.9:
                positive[date] += 1
            elif factor < 0.1 and factor > 0:
                negative[date] += 1
            else:
                neutral[date] += 1
        range_date = [ current_date - relativedelta(months=i) for i in range(6, -1, -1) ]
        data = {}
        data['negative'] = [ negative[date] for date in range_date]
        data['positive'] = [ positive[date] for date in range_date]
        data['neutral'] = [ neutral[date] for date in range_date]
        data['date'] = [ date.strftime("%Y-%m") for date in range_date]
        return JsonResponse(data)

def byDays(min_date, max_date, date_range, articles):
            #find the first day of current week
        # today = datetime.datetime.now().date()
        today = min_date
        first_day = today - timedelta(days=today.weekday())
        begin_date =  first_day - relativedelta(weeks=6)
        get_week = lambda x : (x - first_day).days / 7 + 1
        negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
        for art in articles:
            week = get_week(art.pubtime.date())
            if week > 6:
                continue
            factor = art.feeling_factor
            if factor > 0.9:
                positive[week] += 1
            elif factor < 0.1 and factor > 0:
                negative[week] += 1
            else:
                neutral[week] += 1
        range_week = range(0, 6, 1)
        data = {}
        data['positive'] = [ positive[week] for week in range_week ]
        data['negative'] = [ negative[week] for week in range_week ]
        data['neutral'] = [ neutral[week] for week in range_week ]
        data['date'] = [ (first_day + timedelta(days=i*7)).strftime("%m-%d") for i in range_week ]
        return JsonResponse(data)

if __name__ == '__main__':
    print date.today()
    print GetFirstDaySeason(date.today())
