from observer.utils.logger import Logger

from django.contrib.auth.models import User
from observer.base.models import Article, Article2, ArticleArea, ArticleCategory, Category, Area, MajorIndustry


logger = Logger(ln='article_sync')
msg = """Scripts: <scripts/article_sync.py>"""

def run():
    article_guid = Article.objects.values_list('guid', flat=True)

    for guid in article_guid:
        area_id = ArticleArea.objects.filter(article_id=guid).values_list('area_id', flat=True)
        area = Area.objects.filter(id__in=area_id)

        category_id = ArticleCategory.objects.filter(article_id=guid).values_list('category_id', flat=True)
        category = Category.objects.filter(id__in=category_id)

        article_fields = Article.objects.filter(guid=guid).values('title', 'url', 'pubtime', 'source',
        'score', 'status', 'industry_id', 'corpus_id')

        user_id = User.objects.filter(id=article_fields[0]['corpus_id'])
        industry_id = MajorIndustry.objects.filter(id=article_fields[0]['industry_id'])

        if user_id.exists():
            user_id = article_fields[0]['corpus_id']
        else:
            user_id = 1

        if industry_id.exists():
            industry_id = article_fields[0]['industry_id']
        else:
            industry_id = -1  # 关联重点行业表None

        article2 = Article2(
            title=article_fields[0]['title'],
            url=article_fields[0]['url'],
            pubtime=article_fields[0]['pubtime'],
            source=article_fields[0]['source'],
            score=article_fields[0]['score'],
            status=article_fields[0]['status'],
            corpus_id=None,
            industry_id=industry_id,
            user_id=user_id,
        )

        if area_id and area and category_id and category:
            print('!!!!!!', guid)
            article2.save()
            article2.areas.add(*area)
            article2.categories.add(*category)
            article2.save()
        else:
            print('??????', guid)
            article2.save()
