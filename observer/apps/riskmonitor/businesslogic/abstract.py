# -*- coding: utf-8 -*-
import pytz
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import Count
from django.db.models import Q

from observer.apps.riskmonitor.models import(
    ScoreIndustry, ScoreEnterprise, Industry,
    Enterprise, RiskNews, Product, RiskNewsPublisher)
from observer.utils.connector.mysql import query
from observer.apps.base.api_function import get_season


class Abstract():

    def indu_make_level(self, score):
        level = 'C'
        if score <= 100 and score >= 90:
            level = 'A'
        if score < 90 and score >= 80:
            level = 'B'
        if score < 80:
            level = 'C'
        return level

    def ente_make_level(self, score):
        level = 'C'
        if score <= 100 and score >= 90:
            level = 'A'
        if score < 90 and score >= 80:
            level = 'B'
        if score < 80:
            level = 'C'
        return level

    def indugenerate(self, induscores):
        for induscore in induscores:
            indu = induscore.industry
            score = induscore.score
            level = self.indu_make_level(score)
            if indu.level == 1:
                yield indu.name, level

    def entegenerate(self, entescores):
        for entescore in entescores:
            score = entescore.score
            level = self.ente_make_level(score)
            yield entescore.enterprise, level

    def risk_industry(self, start, end, type):
        induscore = ScoreIndustry.objects.filter(
            pubtime__range=(start, end)).order_by('-score')
        indunames = self.indugenerate(induscore)
        count = 3 if type is 'abstract' else Industry.objects.filter(
            level=1).count()
        try:
            indunames = [indunames.next() for i in xrange(count - 1)]
        except:
            indunames = []
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

    def news_nums(self, start, end, industry='%%', enterprise='%%', source=-1):
        days = (end - start).days
        datel = [(start + timedelta(days=i)) for i in xrange(days)]
        start = start.astimezone(pytz.utc)
        start = time.strftime('%Y-%m-%d %X', start.timetuple())
        start = datetime.strptime(start, '%Y-%m-%d %X')
        date = [(start + timedelta(days=x)) for x in xrange(days)]
        date_range = [(i, i + timedelta(days=1)) for i in date]
        if source == -1:
            query_str = map(
                lambda x: """sum(case when pubtime < '%s' and
                    pubtime >= '%s' then 1 else 0 end)"""
                % (x[1], x[0]),
                date_range
            )
        else:
            query_str = map(
                lambda x: """sum(case when pubtime < '%s' and
                    pubtime >= '%s' and source = %s then 1 else 0 end)"""
                % (x[1], x[0], source),
                date_range
            )
        sum_news = lambda x: query("""
            SELECT %s FROM %s r LEFT JOIN
            risk_news_industry ri ON r.`id`=ri.`risknews_id`
            LEFT JOIN industry i ON i.`id`=ri.`industry_id`
            LEFT JOIN risk_news_enterprise re ON re.`enterprise_id`=r.`id`
            LEFT JOIN enterprise e ON re.`enterprise_id`=e.`id`
            LEFT JOIN risk_news_area rna ON rna.`risknews_id`=r.`id`
            LEFT JOIN area a ON a.`id`=rna.`area_id`
            WHERE i.`id` like '%s' AND e.`id` like '%s'
            """ % (','.join(query_str), x, industry, enterprise, ))
        news_data = [i for i in sum_news('risk_news')[0]]
        date = map(lambda x: x.strftime("%m-%d"), datel)
        return {'data': news_data, 'date': date}

    def compare(self, start, end, id):

        def count(start, end, id):
            industry = Industry.objects.get(id=id)
            count = RiskNews.objects.filter(
                pubtime__range=(start, end), industry=industry).aggregate(
                reprinted=Count('reprinted'))
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
                    start=None, end=None):
        industry = Industry.objects.get(
            id=industry) if industry else None
        enterprise = Enterprise.objects.get(
            id=enterprise) if enterprise else None
        product = Product.objects.get(
            id=product) if product else None

        data = RiskNews.objects.filter(
            Q(industry=industry) if industry == None else Q()
            & Q(enterprise=enterprise) if enterprise == None else Q()
            & Q(product=product) if product == None else Q()
            & Q(source=source) if source == None else Q()
            & Q(pubtime__range=(start, end)))
        items = []
        for d in data:
            item = {
                'id': d.id,
                'title': d.title,
                'source': d.source,
                'time': d.pubtime
            }
            items.append(item)
        return {'items': items, 'total': data.count()}

    def source(self):
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
