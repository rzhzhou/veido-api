# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
import time
from dateutil.relativedelta import relativedelta
from yqj.models import Category, Article


def smart_time(starttime, endtime):
    date_range = endtime - starttime
    if int(date_range.days) > 0 and int(date_range.days) <= 7:
        return [endtime - relativedelta(days=i) for i in range(1, int(date_range.days) + 1)]
    else:
        return [endtime - relativedelta(days=i) for i in range(1, int(date_range.days) + 1, 2)]


def analytics_data(starttime, endtime):
    time_range = smart_time(starttime, endtime)
    date_range = endtime - starttime
    alltime = [starttime + relativedelta(days=i) for i in range(date_range.days)]
    
    for i in alltime:
        print i
    print '#####'
    for i in time_range:
        print i

    data_article = {}
    articles_count = 0
    count = 1
    for i in alltime:
        category = Category.objects.filter(name=u'综合')[0]
        articles_count = category.articles.filter(pubtime=i).count() + articles_count
        if i in time_range:
            data_article[i] = articles_count
            print articles_count
            articles_count = 0

        starttime += relativedelta(days=count)
        count += 1
    return data_article


if __name__ == '__main__':
    print datetime.now() - relativedelta(months=1)
    analytics_data(date.today() - relativedelta(months=1), date.today())