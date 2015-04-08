#coding: utf-8
from datetime import date, datetime

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

if __name__ == '__main__':
    print GetFirstDaySeason(date.today())
