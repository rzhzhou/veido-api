from observer.apps.base.models import Article as BaseArticle
from observer.apps.yqj.models import Article as YqjArticle
from observer.apps.seer.service.abstract import Abstract


class ArticlesQuerySet(Abstract):

    def __init__(self, params={}):
        super(ArticlesQuerySet, self).__init__(params)

    def get_all_article_list(self):

        # yqj article query
        fields = ('base_article', )
        cond = {
            'category__level': getattr(self, 'level', None),
            'category__name': getattr(self, 'category_name', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        uuids = YqjArticle.objects.filter(**args).values(*fields)

        # base article query
        fields = ('url', 'title', 'pubtime', 'source', 'reprinted', 'area', )
        cond = {
            'guid__in': uuids,
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
        }
        args = dict([k, v] for k, v in cond.items() if v)
        queryset = BaseArticle.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset
