# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from django.conf import settings


def get_timezone(timezone='UTC'):
    tz = pytz.timezone(timezone)
    return tz


def get_loc_dt(tz, dt, as_tz=None):
    dt = datetime.strptime(dt, '%Y-%m-%d')
    if as_tz:
        return tz.localize(dt).astimezone(as_tz)

    return tz.localize(dt)


def utc_to_local_time(dt):
    """
    接受一个utc时间参数或者一个时间列表，返回一个本地
    时区的时间或者时间列表(参数和返回值都为datetime类型)
    """
    tz = pytz.timezone(settings.TIME_ZONE)

    datetime_to_local = lambda x: x.astimezone(
        tz) if x.tzinfo else pytz.utc.localize(x).astimezone(tz)

    while True:
        if isinstance(dt, str):
            dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            continue
        elif isinstance(dt, list):
            return [datetime_to_local(i) for i in dt]
        elif isinstance(dt, datetime):
            return datetime_to_local(dt)
        else:
            raise TypeError
