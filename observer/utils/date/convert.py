# -*- coding: utf-8 -*-
import pytz

from calendar import monthrange
from datetime import date, datetime, timedelta
from time import mktime

from django.conf import settings


def utc_to_local_time(dt):
    """
    接受一个utc时间参数或者一个时间列表，返回一个本地
    时区的时间或者时间列表(参数和返回值都为datetime类型)
    """
    tz = pytz.timezone(settings.TIME_ZONE)

    utc_to_local = lambda x: x.astimezone(tz) if x.tzinfo else tz.localize(x)

    if isinstance(dt, (str, unicode)):
        for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S'):
            try:
                dt = datetime.strptime(dt, fmt)
                return utc_to_local(dt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')
    elif isinstance(dt, (list, tuple)):
        return [utc_to_local_time(i) for i in dt]
    elif type(dt) is date:
        dt = datetime.combine(dt, datetime.min.time())
    elif type(dt) is datetime:
        pass
    else:
        raise TypeError

    return utc_to_local(dt)


def datetime_to_timestamp(dt):
    if isinstance(dt, datetime):
        value = int(mktime(dt.timetuple()))
    elif isinstance(dt, int):
        value = dt
    else:
        value = None

    return value


def get_days(days=60, current_date=''):
    if current_date == '':
        current_date = str(date.today())

    current_y_m_d = current_date.split('-')
    current_year = int(current_y_m_d[0])
    current_month = int(current_y_m_d[1])
    current_day = int(current_y_m_d[2])

    total_days = 0
    months = (days / 30) + 1

    for i in xrange(months):
        year = current_year
        month = current_month - i

        if month <= 0:
            month += 12
            year -= 1
        elif month > 12:
            month -= 12
            year += 1

        thedays = monthrange(year, month)[1]
        if i == 0:
            total_days += current_day
        elif i == (months - 1):
            total_days += (thedays - current_day)
        else:
            total_days += thedays

    return total_days


def get_start_end(days=60):

    def date_to_str(dt):
        current_y_m_d = str(dt).split('-')
        current_year = int(current_y_m_d[0])
        current_month = int(current_y_m_d[1])
        current_day = int(current_y_m_d[2])
        return '%s-%s-%s' % (current_year+1 if current_month is 12 else current_year, 1 if current_month is 12 else current_month + 1, 1)

    end_date = date_to_str(date.today())

    start_date = date_to_str(date.today() - timedelta(days=get_days(days)))

    return (start_date, end_date)
