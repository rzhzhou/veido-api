from observer.utils.logger import Logger
from observer.base.models import Inspection, MajorIndustry, HistoryIndustries, MajorIndustries


logger = Logger(ln='new_inspection_industry_sync')
msg = """Scripts: <scripts/new_inspection_industry_sync.py>"""

def run():
    new_id = ''
    for id in Inspection.objects.values_list('id', flat=True):

        product_name = Inspection.objects.get(id=id).product_name

        new_industry_id = HistoryIndustries.objects.filter(name=product_name).values_list('industry_id', flat=True)

        if new_industry_id:
            new_id = new_industry_id[0]
        else:
            new_id = '-1'

        print('当前行业', product_name, new_id)

        Inspection.objects.filter(id=id).update(new_industry_id=new_id)
