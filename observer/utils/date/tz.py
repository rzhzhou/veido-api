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
