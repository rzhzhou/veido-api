from django.core.exceptions import ObjectDoesNotExist

from observer.utils.logger import Logger

from observer.base.models import Enterprise, Enterprise2


logger = Logger(ln='enterprise_sync')
msg = """Scripts: <scripts/enterprise_sync.py>"""

def run():
    enterprises = Enterprise.objects.values('id', 'name', 'area_id', 'unitem', 'status')
    enterprise2_bulk = []
    for enterprise in enterprises:
        enterprise2 = Enterprise2(
            id=enterprise['id'],
            name=enterprise['name'],
            area_id=enterprise['area_id'],
            unitem=enterprise['unitem'],
            status=enterprise['status']
        )
        enterprise2_bulk.append(enterprise2)
        print(enterprise)

    Enterprise2.objects.bulk_create(enterprise2_bulk)
