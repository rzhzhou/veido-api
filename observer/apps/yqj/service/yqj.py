from observer.apps.base.models import Area
from observer.apps.yqj.models import ArticleCollection
"""
    yqj 相关的业务工具方法
"""

# 判断文章是否收藏
def is_collection(user_id, guid):
    return True if ArticleCollection.objects.filter(collector__id=user_id, article__base_article=guid) else False
