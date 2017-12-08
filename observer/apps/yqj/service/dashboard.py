from observer.apps.seer.service.abstract import Abstract
from observer.apps.base.models import Inspection, Article as BaseArticle
from observer.apps.yqj.models import Article as YqjArticle


class DashboardQuerySet(Abstract):

    def __init__(self, params={}):
        super(DashboardQuerySet, self).__init__(params)

    def get_data(self):
        # lambda -> return: uuids
        article_uuids = lambda x, y : YqjArticle.objects.filter(category__name=x, category__level=y).values('base_article')
        # lambda -> return: article first10
        queryset_first10 = lambda x, y : BaseArticle.objects.filter(guid__in=x).values(**y).order_by('-pubtime')[0:10]
        # lambda -> return: xx.xx%
        proportion = lambda x, y : '%.2f%%' % (float(x) / float(y) * 100, )

        #质监热点 queryset
        zjrd_queryset = article_uuids('质监热点', 1)
        #质量事件 queryset
        zlsj_queryset = article_uuids('质量事件', 1)
        #风险快讯 queryset
        fxkx_queryset = article_uuids('风险快讯', 1)
        #信息参考 queryset
        xxck_queryset = article_uuids('信息参考', 1)
        #专家视点 queryset
        zjsd_queryset = article_uuids('专家视点', 1)
        #抽检信息 queryset
        inspection_queryset = Inspection.objects.all()

        #总数
        total = BaseArticle.objects.count() + inspection_queryset.count()
        #质监热点 数量 and 占比
        zjrd_count = zjrd_queryset.count()
        zjrd_proportion = proportion(zjrd_count, total) 
        #质量事件 数量 and 占比
        zlsj_count = zlsj_queryset.count()
        zlsj_proportion = proportion(zlsj_count, total) 
        #风险快讯 数量 and 占比
        fxkx_count = fxkx_queryset.count()
        fxkx_proportion = proportion(fxkx_count, total) 
        #抽检信息 数量 and 占比
        inspection_count = inspection_total
        inspection_proportion = proportion(inspection_count, total) 

        #质监热点 first10
        zjrd_list = queryset_first10(zjrd_queryset, ('guid', 'title', 'reprinted', )) 
        #质量事件 first10
        zlsj_list = queryset_first10(zlsj_queryset, ('guid', 'title', 'reprinted', ))
        #信息参考 first10
        xxck_list = queryset_first10(xxck_queryset, ('guid', 'title', 'pubtime', ))
        #专家视点 first10
        zjsd_list = queryset_first10(zjsd_queryset, ('guid', 'title', 'pubtime', ))
        #风险快讯 first10
        fxkx_list = queryset_first10(fxkx_queryset, ('title', 'url', 'source', 'pubtime', 'score', ))
        #抽检信息 first10
        inspection_list = queryset_first10(inspection_queryset, ('product', 'title', 'url', 'qualitied', 'source', 'pubtime', ))

        return (total, zjrd_count, zjrd_proportion, zlsj_count, zlsj_proportion, 
                fxkx_count, fxkx_proportion, inspection_count, inspection_proportion, 
                zjrd_list, zlsj_list, xxck_list, zjsd_list, fxkx_list, inspection_list, )
