from observer.apps.base.models import Area
from observer.apps.yqj.models import ArticleCollection
"""
    article 相关的工具方法
"""

# 判断文章是否收藏
def is_collection(user_id, guid):
	return True if ArticleCollection.objects.filter(collector__id=user_id, article__base_article=guid) else False

# 获取地域名字
def get_area(area_id):
    return Area.objects.get(id=area_id).name
