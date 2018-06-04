import pytz

from calendar import monthrange
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from time import mktime

from django.conf import settings


def utc_to_local_time(dt):
    """
    接受一个utc时间参数或者一个时间列表，返回一个本地
    时区的时间或者时间列表(参数和返回值都为datetime类型)
    """
    tz = pytz.timezone(settings.TIME_ZONE)

    utc_to_local = lambda x: x.astimezone(tz) if x.tzinfo else tz.localize(x)

    if isinstance(dt, (str, )):
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


def date_format(time, pattern):
    return utc_to_local_time(time).strftime(pattern)


def str_to_date(date_str):
    if date_str.find('/') != -1:
        year_s, mon_s, day_s = date_str.split('/')
        return datetime(int(year_s), int(mon_s), int(day_s))
    elif date_str.find('-') != -1:
        year_s, mon_s, day_s = date_str.split('-')
        return datetime(int(year_s), int(mon_s), int(day_s))


def get_months():
    minus = lambda x, y: (x + relativedelta(months=y))
    today = date.today()
    first_day = datetime(today.year, today.month, 1)
    return list(map(lambda x: [minus(first_day, x-11), minus(first_day, x-10)], range(0, 12)))
