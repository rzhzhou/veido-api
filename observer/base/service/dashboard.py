from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Area, UserArea, Article,
                                Category, Inspection,
                                )
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
                    }, q(Inspection.objects.filter(area_id=UserArea.objects.get(user=self.user).area.id, status=1))),
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
