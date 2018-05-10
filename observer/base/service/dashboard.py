from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, F

from observer.base.models import(Area, UserArea, Article, ArticleArea, 
                                Category, ArticleCategory, Inspection, 
                                )
from observer.base.service.base import (areas, categories, )
from observer.utils.date_format import (date_format, str_to_date, get_months)
from observer.utils.str_format import str_to_md5str


class DashboardData():

    def __init__(self, user):
        self.user = user
        super(DashboardData, self).__init__()

    def get_all(self):
        months = get_months()[-2::]
        # 0001 : 质量热点（panel 1）
        # 0002 : 风险快讯（panel 2）
        # 0003 : 业务信息（panel 3）
        # 0004 : 抽检信息（panel 4）
        # 0005 : 热点信息（panel 5）
        # 0006 : 风险快讯（panel 6）
        # 0007 : 业务信息-特种（panel 7）
        # 0008 : 业务信息-标准（panel 7）
        # 0009 : 业务信息-计量（panel 7）
        # 0010 : 业务信息-全国（panel 8）
        # 0011 : 业务信息-本地（panel 8）
        return {
            '0001' : self.get_0001(months),
            '0002' : self.get_0002(months),
            '0003' : self.get_0003(months),
            '0004' : self.get_0004(months),
            '0005' : self.get_0005(),
            '0006' : self.get_0006(),
            '0007' : self.get_0007(),
            '0008' : self.get_0008(),
            '0009' : self.get_0009(),
            '0010' : self.get_0010(),
            '0011' : self.get_0011(),
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
        c = lambda x, y, z : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1], guid__in=z).count()
        
        pre = c(months[0], Article, a_ids)
        cur = c(months[1], Article, a_ids)
        
        return self.mom(pre, cur)

    def get_0002(self, months):
        a_ids = ArticleCategory.objects.filter(category_id='0002').values_list('article_id', flat=True)
        c = lambda x, y, z : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1], guid__in=z).count()
        
        pre = c(months[0], Article, a_ids)
        cur = c(months[1], Article, a_ids)
        
        return self.mom(pre, cur)

    def get_0003(self, months):
        a_ids = ArticleCategory.objects.filter(category_id='0003').values_list('article_id', flat=True)
        c = lambda x, y, z : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1], guid__in=z).count()
        
        pre = c(months[0], Article, a_ids)
        cur = c(months[1], Article, a_ids)
        
        return self.mom(pre, cur)

    def get_0004(self, months):
        c = lambda x, y : y.objects.filter(pubtime__gte=x[0], pubtime__lt=x[1]).count()
        
        pre = c(months[0], Inspection)
        cur = c(months[1], Inspection)
        
        return self.mom(pre, cur)

    def get_0005(self):
        a_ids = ArticleCategory.objects.filter(category_id='0001').values_list('article_id', flat=True)
        queryset = Article.objects.filter(guid__in=a_ids).values('url', 'title', 'pubtime')[0:15]

        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0006(self):
        a_ids = ArticleCategory.objects.filter(category_id='0002').values_list('article_id', flat=True)
        queryset = Article.objects.filter(guid__in=a_ids).values('url', 'title', 'pubtime')[0:15]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0007(self):
        a_ids = ArticleCategory.objects.filter(category_id='00036').values_list('article_id', flat=True)
        queryset = Article.objects.filter(guid__in=a_ids).values('url', 'title', 'pubtime')[0:15]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0008(self):
        a_ids = ArticleCategory.objects.filter(category_id='00032').values_list('article_id', flat=True)
        queryset = Article.objects.filter(guid__in=a_ids).values('url', 'title', 'pubtime')[0:15]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0009(self):
        a_ids = ArticleCategory.objects.filter(category_id='00037').values_list('article_id', flat=True)
        queryset = Article.objects.filter(guid__in=a_ids).values('url', 'title', 'pubtime')[0:15]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0010(self):
        c_ids = Category.objects.filter(parent__id='0003').values_list('id', flat=True)
        a_ids = ArticleCategory.objects.filter(category_id__in=c_ids).values_list('article_id', flat=True)
        queryset = Article.objects.filter(guid__in=a_ids).values('url', 'title', 'pubtime')[0:15]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

    def get_0011(self):
        current_area = UserArea.objects.filter(user=self.user).values_list('area__id', flat=True)
        aa_ids = ArticleArea.objects.filter(area_id__in=current_area).values_list('article_id', flat=True)

        c_ids = Category.objects.filter(parent__id='0003').values_list('id', flat=True)
        a_ids = ArticleCategory.objects.filter(category_id__in=c_ids).values_list('article_id', flat=True)
        queryset = Article.objects.filter(guid__in=set(tuple(aa_ids) + tuple(a_ids))).values('url', 'title', 'pubtime')[0:15]
        
        return map(lambda x : {
                'url': x['url'],
                'title': x['title'],
                'pubtime': date_format(x['pubtime'], '%Y-%m-%d'), 
            }, queryset)

