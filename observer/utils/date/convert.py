# -*- coding: utf-8 -*-
import pytz
from datetime import date, datetime
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
    elif isinstance(dt, date):
        dt = datetime.combine(dt, datetime.min.time())
    elif isinstance(dt, datetime):
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
