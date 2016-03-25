# -*- coding: utf-8 -*-
import pytz
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings

from observer.apps.riskmonitor.models import(
    ScoreIndustry, ScoreEnterprise, Industry,
    Enterprise, RiskNews, Product, RiskNewsPublisher,
    UserIndustry)
from observer.utils.connector.mysql import query
from observer.apps.base.api_function import get_season
from observer.apps.base.views import BaseView


class Abstract(BaseView):

    def pretty_date(self, time=False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        if type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif isinstance(time, datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return u"刚刚"
            if second_diff < 60:
                return str(second_diff) + u"秒前"
            if second_diff < 120:
                return u"1分钟前"
            if second_diff < 3600:
                return str(second_diff / 60) + u"分钟前"
            if second_diff < 7200:
                return u"1小时前"
            if second_diff < 86400:
                return str(second_diff / 3600) + u"小时前"
        if day_diff == 1:
            return u"昨天"
        if day_diff < 7:
            return str(day_diff) + u"天前"
        if day_diff < 31:
            return str(day_diff / 7) + u"周前"
        if day_diff < 365:
            return str(day_diff / 30) + u"个月前"
        return str(day_diff / 365) + u"年前"

    def utc_to_local_time(self, time):
        """
        接受一个utc时间参数或者一个时间列表，返回一个本地
        时区的时间或者时间列表(参数和返回值都为datetime类型)
        """
        tz = pytz.timezone(settings.TIME_ZONE)

        datetime_to_local = lambda x: x.astimezone(
            tz) if x.tzinfo else pytz.utc.localize(x).astimezone(tz)

        if type(time) is list:
            times = [datetime_to_local(i) for i in time]
        else:
            times = datetime_to_local(time)
        return times

    def indu_make_level(self, score):
        level = 'A'
        if score <= 100 and score >= 90:
            level = 'C'
        if score < 90 and score >= 80:
            level = 'B'
        if score < 80:
            level = 'A'
        return level

    def ente_make_level(self, score):
        level = 'A'
        if score <= 100 and score >= 90:
            level = 'C'
        if score < 90 and score >= 80:
            level = 'B'
        if score < 80:
            level = 'A'
        return level

    def indugenerate(self, induscores, user_id):
        for induscore in induscores:
            indu = induscore.industry
            userindus = indu.userindustry_set.filter(user__id=user_id)
            if userindus.exists() and indu.level == 1:
                score = induscore.score
                level = self.indu_make_level(score)
                yield userindus[0].name, level, userindus[0].id

    def entegenerate(self, entescores):
        for entescore in entescores:
            score = entescore.score
            level = self.ente_make_level(score)
            yield entescore.enterprise, level

    def risk_industry(self, start, end, user_id):
        induscore = ScoreIndustry.objects.filter(
            pubtime__range=(start, end)).order_by('-score')
        indunames = self.indugenerate(induscore, user_id)
        try:
            indunames = [i for i in indunames]
        except AttributeError:
            indunames = []

        user_industrys = UserIndustry.objects.filter(user__id=user_id)
        indunames = indunames if indunames else [[i.name, 'A', i.id
                                                  ] for i in user_industrys]
        return indunames

    def risk_enterprise(self, start, end, type):
        entescore = ScoreEnterprise.objects.filter(
            pubtime__range=(start, end)).order_by('-score')
        enteobject = self.entegenerate(entescore)
        count = 3 if type is 'abstract' else Enterprise.objects.all().count()
        try:
            enteobjects = [enteobject.next() for i in xrange(count)]
        except:
            enteobjects = []
        return enteobjects

    def news_nums(self, date_range, industry='%%', enterprise='%%',
                  source='%%', product='%%'):
        industry = industry if industry == '%%' else UserIndustry.objects.get(
            id=industry).industry.id
        query_str = map(
            lambda x: """sum(case when pubtime < '%s' and
                pubtime >= '%s' then 1 else 0 end)"""
            % (x[1], x[0]),
            date_range
        )

        sum_news = lambda x: query("""
            SELECT %s FROM (
            SELECT count(distinct r.`id`), r.`pubtime` FROM %s r
            LEFT JOIN risk_news_industry ri ON r.`id`=ri.`risknews_id`
            LEFT JOIN industry i ON i.`id`=ri.`industry_id`
            LEFT JOIN risk_news_enterprise re ON re.`enterprise_id`=r.`id`
            LEFT JOIN enterprise e ON re.`enterprise_id`=e.`id`
            LEFT JOIN risk_news_area rna ON rna.`risknews_id`=r.`id`
            LEFT JOIN area a ON a.`id`=rna.`area_id`
            LEFT JOIN risknewspublisher rnp ON r.`publisher_id`=rnp.`id`
            WHERE i.`id` like '%s' AND e.`id` like '%s' AND rnp.`id` like '%s'
            GROUP BY r.id) b
            """ % (','.join(query_str), x, industry, enterprise, source))
        risk_news = sum_news('risk_news')[0]
        news_data = [int(0 if i is None else i)
                     for i in risk_news]
        return {'data': news_data}

    def compare(self, start, end, id):

        def count(start, end, id):
            try:
                industry = Industry.objects.get(
                    id=id) if id is not None else None
            except ObjectDoesNotExist:
                raise Http404("Industry does not exist")
            count = RiskNews.objects.filter(
                Q(pubtime__range=(start, end)) & Q(industry=industry
                                                   ) if industry is not None else Q()
            ).aggregate(reprinted=Count('reprinted'))
            return count['reprinted']

        def compare_with_the_statistics_last_year(start, end, id):
            timedelta_one_year = relativedelta(years=1)
            a_period_count = count(start, end, id)
            b_period_count = count(
                start - timedelta_one_year, end - timedelta_one_year, id)
            try:
                increase = (a_period_count - b_period_count) / b_period_count
            except:
                increase = 0
            return increase

        def compare_with_the_statistics_last_season(start, end, id):
            timedelta_one_season = relativedelta(months=3)
            a_period_count = count(start, end, id)
            b_period_count = count(
                start - timedelta_one_season, end - timedelta_one_season, id)
            try:
                increase = (a_period_count - b_period_count) / b_period_count
            except:
                increase = 0
            return increase

        def compare_with_the_statistics_last_month(start, end, id):
            timedelta_one_month = relativedelta(months=1)
            a_period_count = count(start, end, id)
            b_period_count = count(
                start - timedelta_one_month, end - timedelta_one_month, id)
            try:
                increase = (a_period_count - b_period_count) / b_period_count
            except:
                increase = 0
            return increase

        date_range = (end - start).days

        if date_range > 6 * 30:
            season = get_season(start)
            data = [[compare_with_the_statistics_last_year(start, end, id)],
                    [compare_with_the_statistics_last_season(start, end, id)]]
            return {
                'data': data,
                'date': season
            }
        # data range by month    less two axis has data
        else:
            month = start.month
            data = [[compare_with_the_statistics_last_year(start, end, id)],
                    [compare_with_the_statistics_last_month(start, end, id)]]
            return {
                'data': data,
                'date': month
            }

    def source_data(self, industry=None, enterprise=None, product=None, source=None,
                    start=None, end=None, page=1):
        industry = industry if industry == '%%' else UserIndustry.objects.get(
            id=industry).industry.id
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        end = end.strftime('%Y-%m-%d %H:%M:%S')
        data = query("""
            SELECT r.`id`, r.`title`, r.`pubtime`, rnp.`publisher`, count(distinct r.`id`)
            FROM risk_news r
            LEFT JOIN risk_news_industry ri ON r.`id`=ri.`risknews_id`
            LEFT JOIN industry i ON i.`id`=ri.`industry_id`
            LEFT JOIN risk_news_enterprise re ON re.`enterprise_id`=r.`id`
            LEFT JOIN enterprise e ON re.`enterprise_id`=e.`id`
            LEFT JOIN risk_news_area rna ON rna.`risknews_id`=r.`id`
            LEFT JOIN area a ON a.`id`=rna.`area_id`
            LEFT JOIN risknewspublisher rnp ON r.`publisher_id`=rnp.`id`
            WHERE i.`id` LIKE '%s' AND e.`id` LIKE '%s' AND rnp.`id` LIKE '%s'
            AND pubtime >= '%s' AND pubtime < '%s' group by r.`id`
            """ % (industry, enterprise, source, start, end))

        items = []
        data = self.paging(data, 10, page)
        for d in data['items']:
            item = {
                'id': d[0],
                'title': d[1],
                'source': d[3],
                'time': self.utc_to_local_time(d[2]).strftime('%Y-%m-%d %H:%M')
            }
            items.append(item)
        return {'items': items, 'total': data['total_number']}

    def enterprise_rank(self, start=None, end=None, industry=None, page=1):
        industry = industry if industry == '%%' else UserIndustry.objects.get(
            id=industry).industry.id
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        end = end.strftime('%Y-%m-%d %H:%M:%S')
        sql = """
            SELECT e.`id`, e.`name`, se.`score`, COUNT(distinct e.`id`)
            FROM enterprise e
            LEFT JOIN risk_news_enterprise re ON e.`id`=re.`enterprise_id`
            LEFT JOIN risk_news rn ON re.`risknews_id`=rn.`id`
            LEFT JOIN score_enterprise se ON e.`id`=se.`enterprise_id`
            LEFT JOIN risk_news_industry rni ON rn.`id`=rni.`risknews_id`
            LEFT JOIN industry i ON i.`id`=rni.`industry_id`
            WHERE rn.`pubtime` >= '%s'
            AND rn.`pubtime` < '%s'
            AND i.`id` like '%s'
            GROUP BY e.`id` ORDER BY se.`score` %s
            """ % (start, end, industry, 'DESC')
        results = query(sql)
        iteml = []
        data = self.paging(results, 10, page)
        ranking = (page - 1) * 10
        for result in data['items']:
            ranking = ranking + 1
            item = {
                'id': result[0],
                'ranking': ranking,
                'title': result[1],
                'level': self.ente_make_level(result[2]),
                'number': result[3]
            }
            iteml.append(item)
        return {'data': iteml, 'total': data['total_number']}

    def sources(self):
        """
        "source": {
            "labels": ["赢商网", "中国产业调研", "新浪", "华西都市网", "人民网"],
            "data": [
                {"value": "335", "name": "赢商网"},
                {"value": "310", "name": "中国产业调研"},
                {"value": "234", "name": "新浪"},
                {"value": "135", "name": "华西都市网"},
                {"value": "1548", "name": "人民网"}
            ]
        }
        """
        queryset = RiskNews.objects.all().values('publisher').annotate(
            num_publishers=Count('publisher')).order_by('-num_publishers')[:5]

        data = [{'value': q['num_publishers'], 'name': RiskNewsPublisher.objects.get(
            id=q['publisher']).publisher} for q in queryset]
        labels = [d['name'] for d in data]
        return {'labels': labels, 'data': data}
