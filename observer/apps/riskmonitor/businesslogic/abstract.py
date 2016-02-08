# -*- coding: utf-8 -*-

from observer.apps.riskmonitor.models import(
    ScoreIndustry, Industry, Enterprise, RiskNews)


class Abstract():
    def indu_make_level(self, score):
        if score <= 100 and score >= 90:
            level = 'A'
        if score < 90 and score >=80:
            level = 'B'
        if score <80:
            level = 'C'
        return level

    def ente_make_level(self, score):
        if score <= 100 and score >= 90:
            level = 'A'
        if score < 90 and score >=80:
            level = 'B'
        if score <80:
            level = 'C'
        return level

    def indugenerate(self, induscores):
        for induscore in induscores:
            indu = induscore.industry
            score = induscore.score
            level = indu_make_level(score)		
            if indu.level==1:
                yield indu.name, level

    def entegenerate(self, entescores):
        for entescore in entescores:
            score = entescore.score
            level = ente_make_level(score)	
            yield entescore.enterprise, level

    def risk_industry(self, start, end, type):
        induscore = ScoreIndustry.objects.filter(
        pubtime__range(start, end)).order_by('-score')
        indunames = indugenerate(induscore)
        count = 3 if type is 'abstract' else Industry.objects.filter(level=1).count()
        indunames = [indunames.next() for i in xrange(count)]
        return indunames 

    def risk_enterprise(self, start, end, type):
        entescore = ScoreEnterprise.objects.filter(
        pubtime__range(start, end)).order_by('-score')
        enteobject = entegenerate(entescore)
        count = 3 if type is 'abstract' else Enterprise.objects.all().count()
        enteobjects = [enteobject.next() for i in xrange(count)]
        return enteobjects

    def news_nums(self, start, end, type, industry=-1, enterprise=-1, source=-1):
        risknews = RiskNews.objects.filter(industry=industry, enterprise=enterprise, publisher=source)
        days = (end - start).days
        start = start.astimezone(pytz.utc)
        start = time.strftime('%Y-%m-%d %X', start.timetuple())
        start = datetime.strptime(start, '%Y-%m-%d %X')
        date = [(start + timedelta(days=x)) for x in xrange(days)]
        date_range = [(i, i + timedelta(days=1)) for i in date]
        query_str = map(
            lambda x: "sum(case when pubtime < '%s' and pubtime >= '%s' then 1 else 0 end)"
            % (x[1], x[0]),
            date_range
        )
        sum_result = lambda x: risknews.raw('select %s from %s' % (','.join(query_str), x))
        news_data = [i for i in sum_result('risk_news')[0]]
        return news_data
