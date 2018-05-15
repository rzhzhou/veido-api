from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Area, UserArea, Article, ArticleArea, 
                                Category, ArticleCategory, Inspection, 
                                )
from observer.base.service.base import (areas, categories, local_related, 
                                        alias_industry, area, qualitied, )
from observer.utils.date_format import (date_format, str_to_date, get_months, )
from observer.utils.str_format import str_to_md5str


class DashboardData():

    def __init__(self, user):
        self.user = user
        super(DashboardData, self).__init__()

    def get_all(self):
        months = get_months()[-2::]
        # i0001 : 质量热点（panel 1）
        # i0002 : 风险快讯（panel 2）
        # i0003 : 业务信息（panel 3）
        # i0004 : 抽检信息（panel 4）

        # i0005 : 质量热点（panel 5）
        # i0006 : 专家视点（panel 6）
        # i0007 : 业务信息（panel 7）
        # i0008 : 风险快讯（panel 8）
        # i0009 : 抽检信息（panel 9）

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
        if not pre_month or not cur_month:
            mom = 'Nan%'
        else:
            rate = ((cur_month / pre_month) - 1 ) * 100
            mom = '{0}%'.format(round(rate, 2))

        return cur, mom


    def get_0001(self, months):
        a_ids = ArticleCategory.objects.filter(category_id='0001').values_list('article_id', flat=True)
        c = lambda x, y, z : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1], status=1, guid__in=z).count()
        
        pre = c(months[0], Article, a_ids)
        cur = c(months[1], Article, a_ids)
        
        return self.mom(pre, cur)

    def get_0002(self, months):
        a_ids = ArticleCategory.objects.filter(category_id='0002').values_list('article_id', flat=True)
        c = lambda x, y, z : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1], status=1, guid__in=z).count()
        
        pre = c(months[0], Article, a_ids)
        cur = c(months[1], Article, a_ids)
        
        return self.mom(pre, cur)

    def get_0003(self, months):
        a_ids = ArticleCategory.objects.filter(category_id='0003').values_list('article_id', flat=True)
        c = lambda x, y, z : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1], status=1, guid__in=z).count()
        
        pre = c(months[0], Article, a_ids)
        cur = c(months[1], Article, a_ids)
        
        return self.mom(pre, cur)

    def get_0004(self, months):
        c = lambda x, y : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
        
        pre = c(months[0], Inspection)
        cur = c(months[1], Inspection)
        
        return self.mom(pre, cur)

    def get_0005(self):
        ac_id = Category.objects.get(name='质量热点').id
        a_ids = ArticleCategory.objects.filter(category_id=ac_id).values_list('article_id', flat=True)
        queryset = Article.objects.filter(status=1, guid__in=a_ids).values('url', 'title', 'pubtime').order_by('-pubtime')[0:1]

        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0006(self):
        ac_id = Category.objects.get(name='专家视点').id
        a_ids = ArticleCategory.objects.filter(category_id=ac_id).values_list('article_id', flat=True)
        queryset = Article.objects.filter(status=1, guid__in=a_ids).values('url', 'title', 'source', 'pubtime').order_by('-pubtime')[0:1]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'source': x['source'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0007(self):
        q = lambda x, y, z : x.objects.filter(status=1, guid__in=y.objects.filter(category_id=z).values_list('article_id', flat=True)).values('guid', 'url', 'title', 'source', 'pubtime').order_by('-pubtime')[0:1]

        return map(lambda c : {
                'id': c.id,
                'name': c.name,
                'i%s' % c.id : map(lambda x :{
                    'url': x['url'],
                    'title': x['title'],
                    'source': x['source'],
                    'areas': areas(x['guid']),
                    'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
                    }, q(Article, ArticleCategory, c.id))
            }, Category.objects.filter(parent__name='业务信息'))

    def get_0008(self):
        ac_id = Category.objects.get(name='风险快讯').id
        a_ids = ArticleCategory.objects.filter(category_id=ac_id).values_list('article_id', flat=True)
        queryset = Article.objects.filter(status=1, guid__in=a_ids).values('guid', 'url', 'source', 'score', 'title', 'pubtime').order_by('-pubtime')[0:1]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'source': x['source'],
                'areas': areas(x['guid']),
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                'score': x['score'],
                'local_related': local_related(x['guid'], self.user), # 本地风险相关度
            }, queryset)

    
    def get_0009(self):
        q = lambda x: x.values('guid', 'title', 'url', 'pubtime', 'source', 'unitem', 'qualitied', 'category', 'level', 'industry_id', 'area_id', ).order_by('-pubtime')[0:1]

        return {'local': map(lambda x: {
                        'industry': alias_industry(x['industry_id']),
                        'url': x['url'],
                        'level': x['level'],
                        'area': area(x['area_id']),
                        'source': x['source'],
                        'qualitied': qualitied(x['qualitied']),
                        'category': x['category'],
                        'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                    }, q(Inspection.objects.filter(area_id=UserArea.objects.get(user=self.user).area.id))),
                'all': map(lambda x: {
                        'industry': alias_industry(x['industry_id']),
                        'url': x['url'],
                        'level': x['level'],
                        'area': area(x['area_id']),
                        'source': x['source'],
                        'qualitied': qualitied(x['qualitied']),
                        'category': x['category'],
                        'pubtime': date_format(x['pubtime'], '%Y-%m-%d'),
                    }, q(Inspection.objects.all())),
                }