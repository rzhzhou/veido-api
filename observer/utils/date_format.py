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