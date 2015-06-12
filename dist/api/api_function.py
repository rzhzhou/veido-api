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


def judgedecad(pubtime):
    decad = ''
    if pubtime.day in [1, 2 ,3, 4, 5, 6, 7, 8, 9, 10]:
        decad = u'%s月上旬'%pubtime.month
    elif pubtime.day in [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
        decad = u'%s月中旬'%pubtime.month
    else:
        decad = u'%s月下旬'%pubtime.month
    return decad


def weekrange(decad_range):
    week_range=list(judgedecad(time) for time in decad_range)
    exchange = []
    for i in week_range:
        if not i in exchange:
            exchange.append(i)
    return exchange


def year_range(min_date, max_date, date_range, articles):
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


def season_range(min_date, max_date, date_range, articles):
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
        start_time = GetFirstDaySeason(max_date) - relativedelta(months = 12)
        # #datetime.date(min_date.year,start_month,1)
        range_date = [ start_time + relativedelta(months = i) for i in range(0, 13, 3) ]                      
        data = {}
        data['negative'] = [ negative[date] for date in range_date]
        data['positive'] = [ positive[date] for date in range_date]
        data['neutral'] = [ neutral[date] for date in range_date]
        data['date'] = [ str(date.year) + get_season(date) for date in range_date]
        return JsonResponse(data)


def months_range(min_date, max_date, date_range, articles):
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


def week_range(min_date, max_date, date_range, articles):
    negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
    for art in articles:
        pubtime = art.pubtime.date()
        decad = judgedecad(pubtime)
        factor = art.feeling_factor
        if factor > 0.9:
            positive[decad] += 1
        elif factor <0.1 and factor >0:
            negative[decad] += 1
        else:
            neutral[decad] += 1
    end_decad = max_date - relativedelta(days = 30)
    decad_range = [(end_decad + relativedelta(days = i)) for i in range(0, 31)]
    week_range=weekrange(decad_range)
    data = {}
    data['positive'] = [positive[decad] for decad in week_range]
    data['negative'] = [negative[decad] for decad in week_range]
    data['neutral'] = [neutral[decad] for decad in week_range]
    data['date'] = week_range
    return JsonResponse(data)


def days_range(min_date, max_date, date_range, articles):
        # today = min_date
        end_day = max_date
        # min_date
        negative, positive, neutral = defaultdict(int), defaultdict(int), defaultdict(int)
        for art in articles:
            factor = art.feeling_factor           
            days = art.pubtime.date()
            if factor > 0.9:
                positive[days] += 1
            elif factor < 0.1 and factor >0:
                negative[days] += 1
            else:
                neutral[days] += 1
        range_time = end_day - relativedelta(days = 6)
        #range_days = [(rangel = rangel + relativedelta(days = i)) for i in range(1,7,1) ]
        range_days = []
        for i in range(0,7,1):
            a = range_time + relativedelta(days = i)
            range_days.append(a)
        data = {}
        data['positive'] = [positive[days] for days in range_days]
        data['negative'] = [negative[days] for days in range_days]
        data['neutral'] = [neutral[days] for days in range_days]
        data['date'] = [(range_time + relativedelta(days = i)).strftime("%m-%d") for i in range(0, 7, 1)]
        return JsonResponse(data)


def unstable():
    data = {}
    data['positive'] = None
    data['negative'] = None
    data['neutral'] = None
    data['date'] = None
    return JsonResponse(data)


if __name__ == '__main__':
    print date.today()
    print GetFirstDaySeason(date.today())
