from observer.apps.base.models import Area
"""
    article 相关的工具方法
"""

# 判断文章是否收藏
def is_collection(self, guid):
    pass

# 获取地域名字
def get_area(self, area_id):
    return Area.objects.get(id=area_id).name
