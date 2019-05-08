import datetime, copy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Area, UserInfo, Article,
                                Category, Inspection, Events,
                                MajorIndustry, ExpertsView)
from observer.base.service.abstract import Abstract
from observer.base.service.base import areas, local_related, qualitied
from observer.utils.date_format import date_format, str_to_date, get_daterange
from observer.utils.str_format import str_to_md5str


class DashboardData(Abstract):

    def __init__(self, params, user):
        self.user = user
        super(DashboardData, self).__init__(params)

    def get_all(self):
        months = get_daterange()

        # i0001 : 质量热点（panel 1）
        # i0002 : 风险快讯（panel 2）
        # i0003 : 业务信息（panel 3）
        # i0004 : 抽检信息（panel 4）

        # i0005 : 质量热点（panel 5）
        # i0006 : 专家视点（panel 6）
        # i0007 : 业务信息（panel 7）
        # i0008 : 风险快讯（panel 8）
        # i0009 : 抽检信息（panel 9）

        self.length = int(getattr(self, 'length', 15))

        return {
            'i0001' : self.get_0001(months),
            'i0002' : self.get_0002(months),
            'i0003' : self.get_0003(months),
            'i0004' : self.get_0004(months),
            'i0005' : self.get_0005(),
            'i0006' : self.get_0006(),
            'i0007' : self.get_0007(),
            'i0008' : self.get_0008(),
            'i0009' : self.get_0009(),
        }

    #环比计算
    def mom(self, pre, cur):
        #上月
        pre_month = float(pre)
        #本月
        cur_month = float(cur)
        #同比
        if not pre_month and cur_month:
            mom = '100'
        elif not cur_month:
            mom = '-'
        else:
            rate = ((cur_month / pre_month) - 1 ) * 100
            mom = round(rate, 2)

        return cur, mom


    def get_0001(self, months):
        ac_id = Category.objects.get(name='质量热点').id
        c = lambda x, y : y.objects.filter(pubtime__gte=x[0], pubtime__lte=x[1], status=1, categories=ac_id).count()

        pre = c(months[0], Article) # 上月截至到本月同一时间新闻数 例如：2018/1/1 ~ 2018/1/20
        cur = c(months[1], Article) # 本月截止到现在的新闻数 例如：2018/2/1 ~ 2018/2/20

        return self.mom(pre, cur)

    def get_0002(self, months):
        ac_id = Category.objects.get(name='风险快讯').id
        c = lambda x, y : y.objects.filter(pubtime__gte=x[0], pubtime__lte=x[1], status=1, categories=ac_id).count()

        pre = c(months[0], Article)
        cur = c(months[1], Article)

        return self.mom(pre, cur)

    def get_0003(self, months):
        ac_ids = Category.objects.filter(parent__name='业务信息').values_list('id', flat=True)
        c = lambda x, y : y.objects.filter(pubtime__gte=x[0], pubtime__lte=x[1], status=1, categories__in=ac_ids).count()

        pre = c(months[0], Article)
        cur = c(months[1], Article)

        return self.mom(pre, cur)

    def get_0004(self, months):
        c = lambda x, y : y.objects.filter(pubtime__gte=x[0], pubtime__lte=x[1]).count()

        pre = c(months[0], Inspection)
        cur = c(months[1], Inspection)

        return self.mom(pre, cur)

    def get_0005(self):
        ac_id = Category.objects.get(name='质量热点').id
        queryset = Article.objects.filter(status=1, categories=ac_id).values('url', 'title', 'pubtime').order_by('-pubtime')[0:self.length]

        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
            }, queryset)

    def get_0006(self):
        ac_id = Category.objects.get(name='专家视点').id
        queryset = Article.objects.filter(status=1, categories=ac_id).values('url', 'title', 'source', 'pubtime').order_by('-pubtime')[0:self.length]

        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'source': x['source'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
            }, queryset)

    def get_0007(self):
        q = lambda x, y : x.objects.filter(status=1, categories=y).values('id', 'url', 'title', 'source', 'pubtime').order_by('-pubtime')[0:self.length]

        return map(lambda c : {
                'id': c.id,
                'name': c.name,
                'list': map(lambda x :{
                    'url': x['url'],
                    'title': x['title'],
                    'source': x['source'],
                    'areas': areas(x['id']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                    }, q(Article, c.id))
            }, Category.objects.filter(parent__name='业务信息'))

    def get_0008(self):
        ac_id = Category.objects.get(name='风险快讯').id
        queryset = Article.objects.filter(status=1, categories=ac_id).values('id', 'url', 'source', 'score', 'title', 'pubtime').order_by('-pubtime')[0:self.length]

        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'source': x['source'],
                'areas': areas(x['id']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                'score': x['score'],
                'local_related': local_related(x['id'], self.user), # 本地风险相关度
            }, queryset)


    def get_0009(self):
        q = lambda x: x.values('title', 'url', 'pubtime', 'source', 'qualitied', 'category', 'level', 'industry',
                               'industry__name', 'area', 'area__name', 'product_name').order_by('-pubtime')[0:self.length]

        return {'local': map(lambda x: {
                        'industry': {'id': x['industry'], 'name': x['industry__name']},
                        'url': x['url'],
                        'level': x['level'],
                        'area': {'id': x['area'], 'name': x['area__name']},
                        'source': x['source'],
                        'qualitied': qualitied(x['qualitied']),
                        'category': x['category'],
                        'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                        'product': x['product_name'],
                    }, q(Inspection.objects.filter(area_id=UserInfo.objects.get(user=self.user).area.id, status=1))),
                'all': map(lambda x: {
                        'industry': {'id': x['industry'], 'name': x['industry__name']},
                        'url': x['url'],
                        'level': x['level'],
                        'area': {'id': x['area'], 'name': x['area__name']},
                        'source': x['source'],
                        'qualitied': qualitied(x['qualitied']),
                        'category': x['category'],
                        'pubtime': date_format(x['pubtime'], '%Y-%m-%d %H:%M:%S'),
                        'product': x['product_name'],
                    }, q(Inspection.objects.filter(status=1).all())),
                }


class V2Data(Abstract):

    def __init__(self, params, user):
        self.user = user
        super(V2Data, self).__init__(params)

    def getTime(self):
        today = datetime.datetime.now().date() # 获取今天日期的date类型
        init = datetime.date(today.year, 1, 1)
        now = datetime.date(today.year, today.month, today.day)

        cond = {
                'pubtime__gte': getattr(self, 'starttime', init),
                'pubtime__lte': getattr(self, 'endtime', now)
            }
        args = dict([k, v] for k, v in cond.items() if v)

        return args

    def compareTime(self):
        # time = getattr(self, 'time',1)
        # today = datetime.datetime.now().date() # 获取今天日期的date类型

        # if time == '本月' or time == '1':
        #     init = datetime.date(today.year, today.month-1, 1)
        #     now = datetime.date(today.year, today.month, 1)
        # elif time == '2':
        #     if today.month <= 3 :
        #         init = datetime.date(today.year-1, 10, 1)
        #         now = datetime.date(today.year, 1, 1)
        #     elif today.month > 3 and today.month <= 6:
        #         init = datetime.date(today.year, 1, 1)
        #         now = datetime.date(today.year, 4, 1)
        #     elif today.month > 6 and today.month <= 9:
        #         init = datetime.date(today.year, 4, 1)
        #         now = datetime.date(today.year, 7, 1)
        #     else:
        #         init = datetime.date(today.year, 7, 1)
        #         now = datetime.date(today.year, 10, 1)
        # else:
        #     init = datetime.date(today.year-1, 1, 1)
        #     now = datetime.date(today.year-1, 12, 31)
        today = datetime.datetime.now().date() # 获取今天日期的date类型
        init = datetime.date(today.year, 1, 1)
        now = datetime.date(today.year, today.month, today.day)
        # 获取过滤器时间
        initTime = getattr(self, 'starttime', init)
        nowTime = getattr(self, 'endtime', now)
        if not initTime:
            initTime = init
            nowTime = now

        startTime = datetime.datetime.strptime(str(initTime), '%Y-%m-%d')
        endTime = datetime.datetime.strptime(str(nowTime), '%Y-%m-%d')

        if startTime.year == endTime.year:
            monthPoor = endTime.month - startTime.month + 1
            lastPoor = startTime.month - monthPoor
            if lastPoor > 0:
                initTime = datetime.date(startTime.year, lastPoor, 1)
                nowTime = datetime.date(startTime.year, startTime.month, 1)
            elif lastPoor == 0:
                initTime = datetime.date(startTime.year-1, 12, 1)
                nowTime = datetime.date(startTime.year, startTime.month, 1)
            else:
                initTime = datetime.date(startTime.year-1, 13+lastPoor, 1)
                nowTime = datetime.date(startTime.year, startTime.month, 1)
        else:
            endTimeMonth = endTime.month
            yearPoor = endTime.year-startTime.year
            endTimeMonth = 12*yearPoor + endTimeMonth
            monthPoor = endTimeMonth - startTime.month + 1
            lastPoor = startTime.month - monthPoor

            if lastPoor > 0:
                initTime = datetime.date(startTime.year, lastPoor, 1)
                nowTime = datetime.date(startTime.year, startTime.month, 1)
            elif lastPoor == 0:
                initTime = datetime.date(startTime.year-yearPoor, 12, 1)
                nowTime = datetime.date(startTime.year, startTime.month, 1)
            else:
                initTime = datetime.date(startTime.year-yearPoor, 13+lastPoor, 1)
                nowTime = datetime.date(startTime.year, startTime.month, 1)

        cond = {
                'pubtime__gte': initTime,
                'pubtime__lt': nowTime,
            }
        args = dict([k, v] for k, v in cond.items() if v)

        return args

    def getHotSpots(self):
        queryset = Article.objects.filter(status=1, categories__id='0001')
        queryset = queryset.values('url', 'title', 'pubtime').order_by('-pubtime')[:10]

        return queryset

    def getEvents(self):
        queryset = Events.objects.annotate(num_articles = Count('articles'))
        queryset = queryset.values('id','title', 'scope', 'grading', 'num_articles').order_by('-num_articles')[:10]

        return queryset

    # def queryEventsChart(init, addTime, title=None):
    #     if not title:
    #         queryEvents = Events.objects.filter(articles__pubtime__gte=init, articles__pubtime__lte=addTime)
    #         queryEvents = queryEvents.annotate(num_articles = Count('articles'))
    #         queryEvents = queryEvents.values_list('title', flat=True).order_by('-num_articles')[:3]
    #     else:
    #         print('ok')
    #         queryEvents = Events.objects.filter(title=title)
    #         queryEvents = queryEvents.filter(articles__pubtime__gte=init, articles__pubtime__lt=addTime)
    #         queryEvents = queryEvents.annotate(num_articles = Count('articles'))
    #         queryEvents = queryEvents.values_list('num_articles', flat=True)

    #     return queryEvents

    def getEventsChart(self):
        today = datetime.datetime.now().date() # 获取今天日期的date类型
        init = datetime.date(today.year, 1, 1)
        now = datetime.date(today.year, today.month, today.day)
        # 获取过滤器时间
        initTime = getattr(self, 'starttime', init)
        nowTime = getattr(self, 'endtime', now)
        if not initTime:
            initTime = init
            nowTime = now

        startTime = datetime.datetime.strptime(str(initTime), '%Y-%m-%d')
        endTime = datetime.datetime.strptime(str(nowTime), '%Y-%m-%d')
        endTimeMonth = endTime.month
        if endTime.year > startTime.year:
            endTimeMonth = 12*(endTime.year-startTime.year) + endTimeMonth

        monthPoor = (endTimeMonth - startTime.month) + 1

        EventData = []
        timeList = []
        data = {}

        if monthPoor <= 8:
            timeList = []
            if endTime.year > startTime.year:
                for i in range(startTime.month, 13):
                    timeList.append(str(startTime.year)+ '.' + str(i))
                    i += 1
                for i in range(1, endTime.month+1):
                    timeList.append(str(endTime.year)+ '.' + str(i))
                    i += 1
            else:
                for i in range(startTime.month, endTime.month+1):
                    timeList.append(str(startTime.year)+ '.' + str(i))
                    i += 1

            now = datetime.date(endTime.year, endTime.month+1, 1)
            init = datetime.date(startTime.year, startTime.month, 1)

            queryTitle = Events.objects.filter(articles__pubtime__gte=init, articles__pubtime__lte=now)
            queryTitle = queryTitle.annotate(num_articles = Count('articles'))
            queryTitle = queryTitle.values_list('title', flat=True).order_by('-num_articles')[:3]

            for title in queryTitle:
                month = startTime.month
                year = startTime.year
                dataList = []
                init = datetime.date(year, month, 1)
                if month == 12:
                    month = 0
                    year += 1

                while (True):
                    addTime = datetime.date(year, month+1, 1)

                    queryset = Events.objects.filter(title=title)
                    queryset = queryset.filter(articles__pubtime__gte=init, articles__pubtime__lt=addTime)
                    queryset = queryset.annotate(num_articles = Count('articles'))
                    queryset = queryset.values_list('num_articles', flat=True)

                    if not queryset:
                        dataList.append(0)
                    else:
                        dataList.append(queryset[0])

                    init = addTime
                    month += 1

                    if endTime.year > startTime.year:
                        if year > startTime.year:
                            if month > endTime.month:
                                break
                        if month == 12:
                            month = 0
                            year += 1
                    else:
                        if month > endTime.month:
                            break

                EventData.append(dataList)

            data = {
                'labels': timeList,
                'series': EventData,
            }

        elif monthPoor > 8 and monthPoor <= 12:
            initMonth = startTime.month
            initYear = startTime.year
            nowMonth = endTime.month
            nowYear = endTime.year

            timeList = []
            if startTime.year == endTime.year:
                if endTime.month == 9:
                    for i in range(1, 4):
                        timeList.append(str(startTime.year) + '年第' + str(i) + '季度')
                else:
                    for i in range(1, 5):
                        timeList.append(str(startTime.year) + '年第' + str(i) + '季度')
            else:
                if startTime.month >= 2 and startTime.month <= 3:
                    for i in range(1, 5):
                        timeList.append(str(startTime.year) + '年第' + str(i) + '季度')
                    for i in range(1, 2):
                        timeList.append(str(endTime.year)+ '年第' + str(i) + '季度')

                elif startTime.month >= 5 and startTime.month <= 6:
                    for i in range(2, 5):
                        timeList.append(str(startTime.year) + '年第' + str(i) + '季度')

                    if endTime.month >= 1 and endTime.month <= 3:
                        for i in range(1, 2):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')
                    else:
                        for i in range(1, 3):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')

                elif startTime.month > 6 and startTime.month <= 9:
                    for i in range(3, 5):
                        timeList.append(str(startTime.year) + '年第' + str(i) + '季度')

                    if endTime.month == 3:
                        for i in range(1, 2):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')
                    elif endTime.month > 3 and endTime.month <= 6:
                        for i in range(1, 3):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')
                    else:
                        for i in range(1, 4):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')
                else:
                    for i in range(4, 5):
                        timeList.append(str(startTime.year) + '年第' + str(i) + '季度')

                    if endTime.month == 6:
                        for i in range(1, 3):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')
                    elif endTime.month > 6 and endTime.month <= 9:
                        for i in range(1, 4):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')
                    else:
                        for i in range(1, 5):
                            timeList.append(str(endTime.year) + '年第' + str(i) + '季度')

            init = datetime.date(initYear, initMonth, 1)
            now = datetime.date(nowYear, nowMonth, 1)

            queryTitle = Events.objects.filter(articles__pubtime__gte=init, articles__pubtime__lte=now)
            queryTitle = queryTitle.annotate(num_articles = Count('articles'))
            queryTitle = queryTitle.values_list('title', flat=True).order_by('-num_articles')[:3]

            for title in queryTitle:
                dataList = []
                year = initYear
                month = initMonth
                addMonth = 1
                init = datetime.date(initYear, initMonth, 1)
                end = 0

                while (True):
                    if month >= 1 and month <= 3:
                        addMonth = 4
                        if year == endTime.year:
                            if endTime.month < addMonth:
                                addMonth = endTime.month

                    elif month > 3 and month <= 6: 
                        addMonth = 7
                        if year == endTime.year:
                            if endTime.month < addMonth:
                                addMonth = endTime.month

                    elif month > 6 and month <= 9:
                        addMonth = 10
                        if year == endTime.year:
                            if endTime.month < addMonth:
                                addMonth = endTime.month

                    else:
                        addMonth = 1
                        
                        if year == endTime.year:
                            addMonth = endTime.month
                            year -= 1

                        year += 1

                    addTime = datetime.date(year, addMonth, 1)

                    queryset = Events.objects.filter(title=title)
                    queryset = queryset.filter(articles__pubtime__gte=init, articles__pubtime__lt=addTime)
                    queryset = queryset.annotate(num_articles = Count('articles'))
                    queryset = queryset.values_list('num_articles', flat=True)

                    if not queryset:
                        dataList.append(0)
                    else:
                        dataList.append(queryset[0])

                    init = addTime
                    month = addMonth

                    if startTime.year == endTime.year:
                        
                        if month == 10:
                            queryset = Events.objects.filter(title=title)
                            queryset = queryset.filter(articles__pubtime__gte=init, articles__pubtime__lt=addTime)
                            queryset = queryset.annotate(num_articles = Count('articles'))
                            queryset = queryset.values_list('num_articles', flat=True)

                            if not queryset:
                                dataList.append(0)
                            else:
                                dataList.append(queryset[0])
                            break

                        elif month == endTime.month:
                            break

                    else:
                        if year == endTime.year and month == endTime.month:
                            queryset = Events.objects.filter(title=title)
                            queryset = queryset.filter(articles__pubtime__gte=init, articles__pubtime__lt=addTime)
                            queryset = queryset.annotate(num_articles = Count('articles'))
                            queryset = queryset.values_list('num_articles', flat=True)

                            if not queryset:
                                dataList.append(0)
                            else:
                                dataList.append(queryset[0])

                            break
                EventData.append(dataList)

            data = {
                'labels': timeList,
                'series': EventData,
            }

        else:
            init = datetime.date(startTime.year, startTime.month, 1)
            now = datetime.date(endTime.year, endTime.month, 1)
            timeList = []
            for i in range(startTime.year, endTime.year+1):
                timeList.append(str(i) + '年')
                
            queryTitle = Events.objects.filter(articles__pubtime__gte=init, articles__pubtime__lte=now)
            queryTitle = queryTitle.annotate(num_articles = Count('articles'))
            queryTitle = queryTitle.values_list('title', flat=True).order_by('-num_articles')[:3]

            for title in queryTitle:
                month = 1
                year = startTime.year
                init = datetime.date(year, startTime.month, 1)
                dataList = []
                end = 0

                while (True):
                    addTime = datetime.date(year+1, month, 1)

                    queryInit = Events.objects.filter(title=title)
                    queryInit = queryInit.filter(articles__pubtime__gte=init, articles__pubtime__lt=addTime)
                    queryInit = queryInit.annotate(num_articles = Count('articles'))
                    queryInit = queryInit.values_list('num_articles', flat=True)

                    if not queryInit:
                        dataList.append(0)
                    else:
                        dataList.append(queryInit[0])

                    init = addTime
                    
                    if end == 1:
                        break

                    if year <= endTime.year:
                        year += 1
                        if year == endTime.year:
                            year = endTime.year - 1
                            month = endTime.month
                            end = 1

                EventData.append(dataList)

            data = {
                'labels': timeList,
                'series': EventData,
            }

        return data

    def getRisknews(self):
        queryset = Article.objects.filter(status=1, categories__name='风险快讯')
        queryset = queryset.values('id', 'url', 'score', 'title', 'pubtime').order_by('-pubtime')[:10]

        return queryset

    def getRiskScore(self):
        pubtime = self.getTime()

        queryset = Article.objects.filter(status=1, categories__name='风险快讯').exclude(score=0)
        queryset = queryset.filter(**pubtime)

        scoreList = [1, 2, 3]
        dataList = []
        for score in scoreList:
            queryScore = queryset.filter(score = score)
            data = {
                'name': '低' if score == 1 else '中' if score == 2 else '高',
                'value':  queryScore.count()
            }

            dataList.append(data)

        return dataList

    def getRiskLocal(self):
        pubtime = self.getTime()

        queryset = Article.objects.filter(status=1, categories__name='风险快讯')
        queryset = queryset.filter(**pubtime).values_list('id', flat=True)[:20]

        relevanceDict = {'1': 0, '2': 0, '3': 0}
        
        for aid in queryset:
            relevance = local_related(aid, self.user)
            relevanceDict[str(relevance)] += 1
  
        relevanceDict['低'] = relevanceDict.pop('1')
        relevanceDict['中'] = relevanceDict.pop('2')
        relevanceDict['高'] = relevanceDict.pop('3')
        relevanceList = []
        for r, v in relevanceDict.items():
            data = {
                'name': r,
                'value': v,
            }
            relevanceList.append(data)

        return relevanceList

    def getInspections(self):
        queryset = Inspection.objects.values('url', 'pubtime', 'qualitied', 'industry', 'source',
                               'industry__name', 'product_name').order_by('-pubtime')[:10]

        return queryset

    def getInspecNum(self):
        queryset = MajorIndustry.objects.annotate(num_industry = Count('inspection'))
        queryset = queryset.values('name', 'num_industry').order_by('-num_industry')[:5]

        return queryset

    def getInspecPass(self):
        pubtime = self.getTime()

        queryset_100 = Inspection.objects.filter(**pubtime).filter(qualitied=1).count()
        queryset_90_100 = Inspection.objects.filter(**pubtime).filter(qualitied__gte=0.9, qualitied__lt=1).count()
        queryset_80_90 = Inspection.objects.filter(**pubtime).filter(qualitied__gte=0.8, qualitied__lt=0.9).count()
        queryset_70_80 = Inspection.objects.filter(**pubtime).filter(qualitied__gte=0.7, qualitied__lt=0.8).count()
        queryset_60_70 = Inspection.objects.filter(**pubtime).filter(qualitied__gte=0.6, qualitied__lt=0.7).count()
        queryset_60 = Inspection.objects.filter(**pubtime).filter(qualitied__lt=0.6).count()

        pass_100 = {
            'name': '100%',
            'value': queryset_100
        }
        pass_90_100 = {
            'name': '90%~100%',
            'value': queryset_90_100
        }
        pass_80_90 = {
            'name': '80%~90%',
            'value': queryset_80_90
        }
        pass_70_80 = {
            'name': '70%~80%',
            'value': queryset_70_80
        }
        pass_60_70 = {
            'name': '60%~70%',
            'value': queryset_60_70
        }
        pass_60 = {
            'name': '低于60%',
            'value': queryset_60
        }

        pass_list = [pass_100, pass_90_100, pass_80_90, pass_70_80, pass_60_70, pass_60]

        return pass_list

    def getQualityBasis(self):
        pubtime = self.getTime()
        lastPubtime = self.compareTime()

        queryCategory = Article.objects.filter(**pubtime)
        standard = queryCategory.filter(categories__name="标准")
        metering = queryCategory.filter(categories__name="计量")
        cerAndAcc = queryCategory.filter(categories__name="认证认可")
        inspecAndTest = queryCategory.filter(categories__name="检验检测")

        queryset = Article.objects.filter(Q(categories__name="标准")|Q(categories__name="检验检测")
            |Q(categories__name="认证认可")|Q(categories__name="检验检测"))

        queryset = queryset.values('url', 'title', 'pubtime', 'categories__name').order_by('-pubtime')[:10]

        data_list = {
            'labels': ["标准", "计量", "认证认可", "检验检测"],
            'series': [[standard.count(), metering.count(), cerAndAcc.count(), inspecAndTest.count()]]
        }

        total = standard.count() + metering.count() + cerAndAcc.count() + inspecAndTest.count()

        lastQueryCategory = Article.objects.filter(**lastPubtime)
        lastStandard = lastQueryCategory.filter(categories__name="标准")
        lastMetering = lastQueryCategory.filter(categories__name="计量")
        lastCerAndAcc = lastQueryCategory.filter(categories__name="认证认可")
        lastInspecAndTest = lastQueryCategory.filter(categories__name="检验检测")

        lastTotal = lastStandard.count() + lastMetering.count() + lastCerAndAcc.count() + lastInspecAndTest.count()
        growth = total - lastTotal
        bulking = round(growth/lastTotal, 2)*100 if lastTotal != 0 else 100

        if growth > 0:
            posaneg = '+'
        else:
            posaneg = ''

        data = {
            'total': total,

            'growth': posaneg + str(growth) + "(" + str(bulking) + "%)",

            'quality': map(lambda q: {
                'url': q['url'],
                'title': q['title'],
                'pubtime': q['pubtime'],
                'category': q['categories__name'],
            }, queryset),

            'qualityLine': data_list
        }

        return data

    def getSafety(self):    
        pubtime = self.getTime()
        lastPubtime = self.compareTime()

        queryCategory = Article.objects.filter(**pubtime)
        product = queryCategory.filter(categories__name="产品质量")
        shoddy = queryCategory.filter(categories__name="假冒伪劣")
        food = queryCategory.filter(categories__name="食品安全")
        drug = queryCategory.filter(categories__name="药品疫苗")
        special = queryCategory.filter(categories__name="特种设备")

        queryset = Article.objects.filter(Q(categories__name="产品质量")|Q(categories__name="假冒伪劣")
            |Q(categories__name="食品安全")|Q(categories__name="药品疫苗")|Q(categories__name="特种设备"))

        queryset = queryset.values('url', 'title', 'pubtime', 'categories__name').order_by('-pubtime')[:10]

        data_list = {
            'labels': ["产品质量", "假冒伪劣", "食品安全", "药品疫苗", "特种设备"],
            'series': [[product.count(), shoddy.count(), food.count(), drug.count(), special.count()]]
        }

        total = product.count() + shoddy.count() + food.count() + drug.count() + special.count()

        lastQueryCategory = Article.objects.filter(**lastPubtime)
        lastProduct = lastQueryCategory.filter(categories__name="产品质量")
        lastShoddy = lastQueryCategory.filter(categories__name="假冒伪劣")
        lastFood = lastQueryCategory.filter(categories__name="食品安全")
        lastDrug = lastQueryCategory.filter(categories__name="药品疫苗")
        lastSpecial = queryCategory.filter(categories__name="特种设备")

        lastTotal = lastProduct.count() + lastShoddy.count() + lastFood.count() + lastDrug.count() + lastSpecial.count()
        growth = total - lastTotal
        bulking = round(growth/lastTotal, 2)*100 if lastTotal != 0 else 100

        if growth > 0:
            posaneg = '+'
        else:
            posaneg = ''

        data = {
            'total': total,

            'growth': posaneg + str(growth) + "(" + str(bulking) + "%)",

            'safety': map(lambda q: {
                'url': q['url'],
                'title': q['title'],
                'pubtime': q['pubtime'],
                'category': q['categories__name'],
            }, queryset),

            'safetyLine': data_list
        }

        return data

    def getMarket(self):     
        pubtime = self.getTime()
        lastPubtime = self.compareTime()

        queryCategory = Article.objects.filter(**pubtime)
        antitrust = queryCategory.filter(categories__name="反垄断")
        price = queryCategory.filter(categories__name="价格监管")
        knowledge = queryCategory.filter(categories__name="知识产权")
        selling = queryCategory.filter(categories__name="传销监管")

        queryset = Article.objects.filter(Q(categories__name="反垄断")|Q(categories__name="价格监管")
            |Q(categories__name="知识产权")|Q(categories__name="传销监管"))

        queryset = queryset.values('url', 'title', 'pubtime', 'categories__name').order_by('-pubtime')[:10]

        data_list = {
            'labels': ["反垄断", "计量", "知识产权", "传销监管"],
            'series': [[antitrust.count(), price.count(), knowledge.count(), selling.count()]]
        }

        total = antitrust.count() + price.count() + knowledge.count() + selling.count()

        lastQueryCategory = Article.objects.filter(**lastPubtime)
        lastAntitrust = lastQueryCategory.filter(categories__name="反垄断")
        lastPrice = lastQueryCategory.filter(categories__name="价格监管")
        lastKnowledge = lastQueryCategory.filter(categories__name="知识产权")
        lastSelling = lastQueryCategory.filter(categories__name="传销监管")

        lastTotal = lastAntitrust.count() + lastPrice.count() + lastKnowledge.count() + lastSelling.count()
        growth = total - lastTotal
        bulking = round(growth/lastTotal, 2)*100 if lastTotal != 0 else 100

        if growth > 0:
            posaneg = '+'
        else:
            posaneg = ''

        data = {
            'total': total,

            'growth': posaneg + str(growth) + "(" + str(bulking) + "%)",

            'market': map(lambda q: {
                'url': q['url'],
                'title': q['title'],
                'pubtime': q['pubtime'],
                'category': q['categories__name'],
            }, queryset),

            'marketLine': data_list
        }

        return data

    def getExpertsView(self):
        pubtime = self.getTime()
        lastPubtime = self.compareTime()

        today = datetime.datetime.now().date() # 获取今天日期的date类型
        init = datetime.date(today.year, 1, 1)
        now = datetime.date(today.year, today.month, today.day)
        # 获取过滤器时间
        initTime = getattr(self, 'starttime', init)
        nowTime = getattr(self, 'endtime', now)
        if not initTime:
            initTime = init
            nowTime = now

        startTime = datetime.datetime.strptime(str(initTime), '%Y-%m-%d')
        endTime = datetime.datetime.strptime(str(nowTime), '%Y-%m-%d')

        i = 1
        month = 10
        year = 2018
        dataList = []
        newInit = datetime.date(endTime.year-1, month, 1)
        while (i <= 8):
            month += 1
            if month > 12:
                month = 1
                year += 1
            newNow = datetime.date(year, month, 1)

            queryset = Article.objects.filter(categories__name = "专家视点")
            queryset = queryset.filter(pubtime__gte=newInit, pubtime__lte=newNow)

            dataList.append(queryset.count())
            newInit = newNow
            i += 1

        data_list = {
            'series': [dataList]
        }

        queryExperts = ExpertsView.objects.values('name', 'portrait', 'articles__url',
                                        'articles__title', 'articles__pubtime')[:7]

        queryTotal = Article.objects.filter(**pubtime)
        queryTotal = queryTotal.filter(categories__name = "专家视点").count()

        queryLastTotal = Article.objects.filter(**lastPubtime)
        queryLastTotal = queryLastTotal.filter(categories__name = "专家视点").count()
        growth = queryTotal - queryLastTotal
        bulking = round(growth/queryLastTotal, 2)*100 if queryLastTotal != 0 else 100

        if growth > 0:
            posaneg = '+'
        else:
            posaneg = ''

        data = {
            'total': queryTotal,

            'growth': posaneg + str(growth) + "(" + str(bulking) + "%)",

            'list' : map(lambda e: {
                'name': e['name'],
                'portrait': e['portrait'],
                'url': e['articles__url'],
                'title': e['articles__title'],
                'pubtime': e['articles__pubtime'],
            }, queryExperts),

            'expertsLine': data_list
        }

        

        return data


class dSonApiData(Abstract):

    def __init__(self, params):
        super(dSonApiData, self).__init__(params)

    def getData(self):
        cond = {
            'categories__id': getattr(self, 'categoryStr'),
        }
        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Article.objects.filter(**args)
        queryset = queryset.values('url', 'title', 'pubtime', 'categories__name').order_by('-pubtime')[:10]

        return queryset    
