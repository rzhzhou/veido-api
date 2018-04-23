from observer.utils.str_format import (str_to_md5str, )
from observer.utils.excel import (read, )
from observer.utils.logger import Logger
from observer.base.models import *


# init logging
logger = Logger(ln='test')
msg = """Scripts: <scripts/test.py>"""


def main():
    title = {'GUID': 0, 
            '标题': 0, 
            'URL': 0, 
            '发布时间': 0, 
            '发布媒体': 0, 
            '风险程度': 0, 
            '地域': 0, 
            '类别': 0, }

    data = read(filename='/mnt/f/article.xlsx', title=title)
    total = len(data)
    dupli = 0

    for i, d in enumerate(data):
        try:
            title = d['标题']
            url = d['URL']
            pubtime = d['发布时间']
            source = d['发布媒体']
            score = d['风险程度']
            area = d['地域']
            category = d['类别']

            a_guid = str_to_md5str(url)

            if Article.objects.filter(guid=a_guid).exists():
                dupli += 1
                continue

            areas = area.split(' ')
            a_ids = Area.objects.filter(name__in=areas).values_list('id', flat=True)
            categories = category.split(' ')
            c_ids = Category.objects.filter(name__in=categories).values_list('id', flat=True)
            for a_id in a_ids:
                if not ArticleArea.objects.filter(article_id=a_guid, area_id=a_id).exists():
                    ArticleArea(
                        article_id=a_guid,
                        area_id=a_id,
                    ).save()

            for c_id in c_ids:
                if not ArticleCategory.objects.filter(article_id=a_guid, category_id=c_id).exists():
                    ArticleCategory(
                        article_id=a_guid,
                        category_id=c_id,
                    ).save()
            
            Article(
                guid=a_guid,
                title=title,
                url=url,
                pubtime=pubtime,
                source=source,
                score=score,
                risk_keyword='',
                invalid_keyword='',
                status=1,
            ).save()

        except Exception as e:
            return {
                'status': 0, 
                'message': '操作失败！Excel %s 行存在问题，错误信息：%s！' % (i + 1, e)
            }

    return {
                'status': 1, 
                'message': '操作成功！共处理%s条数据，成功导入%s条数据，重复数据%s条！' % (total, total - dupli, dupli, )
            }
    

def run():
    print(main())