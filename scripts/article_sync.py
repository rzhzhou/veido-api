from django.core.exceptions import ObjectDoesNotExist

from observer.utils.logger import Logger

from observer.base.models import Article, Article2, ArticleArea, ArticleCategory, Category, Area


logger = Logger(ln='article_sync')
msg = """Scripts: <scripts/article_sync.py>"""

def run():
    article_guid = Article.objects.values_list('guid', flat=True)

    for guid in article_guid:
        area_id = ArticleArea.objects.filter(article_id=guid).values_list('area_id', flat=True)
        area = Area.objects.filter(id__in=area_id)

        category_id = ArticleCategory.objects.filter(article_id=guid).values_list('category_id', flat=True)
        category = Category.objects.filter(id__in=category_id)

        article_fields = Article.objects.filter(guid=guid).values('title', 'url', 'pubtime', 'source', 'score', 'status')

        articel2 = Article2(
            title=article_fields[0]['title'],
            url=article_fields[0]['url'],
            pubtime=article_fields[0]['pubtime'],
            source=article_fields[0]['source'],
            score=article_fields[0]['score'],
            status=article_fields[0]['status'],
        )

        if area_id and area and category_id and category:
            print('!!!!!!', guid)
            articel2.save()
            articel2.areas.add(*area)
            articel2.categories.add(*category)
            articel2.save()
        else:
            print('??????', guid)
            articel2.save()
