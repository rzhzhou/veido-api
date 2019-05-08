from observer.utils.logger import Logger
from observer.base.models import  Article, MajorIndustries, HistoryIndustries, MajorIndustry

logger = Logger(ln='aricle_majorindustries')
msg = """Scripts: <scripts/aricle_majorindustries.py>"""


def run():
    new_id =''
    product_name =''
    for id in Article.objects.values_list('id', flat=True):

        industry_id = Article.objects.get(id=id).industry_id

        if industry_id == "-1":
            new_id = "-1"
        else:
            product_name = MajorIndustry.objects.get(id=industry_id).name

            new_industry_id = HistoryIndustries.objects.filter(name=product_name).values_list('industry_id', flat=True)

            if new_industry_id:
                new_id = new_industry_id[0]
            else:
                new_id = None


        print('当前行业', product_name, new_id)

        Article.objects.filter(id=id).update(new_industry_id=new_id)