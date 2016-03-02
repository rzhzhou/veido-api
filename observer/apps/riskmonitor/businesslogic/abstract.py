# -*- coding: utf-8 -*-
import pytz
import time
from datetime import datetime, timedelta

from django.db.models import Count

from observer.apps.riskmonitor.models import(
    ScoreIndustry, ScoreEnterprise, Industry, Enterprise, RiskNews)
from observer.utils.connector.mysql import query


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

    def news_nums(self, start, end, type, industry='%%', enterprise='%%', source=-1):
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

    def compare(self):

        def count():
            count = RiskNews.objects.aggregate(reprinted=Count('reprinted'))
            return count['reprinted']

        def compare_with_the_statistics_last_year():
            pass

        def compare_with_the_statistics_last_season():
            pass

        def compare_with_the_statistics_last_month():
            pass
