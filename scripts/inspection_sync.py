from django.core.exceptions import ObjectDoesNotExist

from observer.utils.logger import Logger

from observer.base.models import Inspection, Inspection2, InspectionEnterprise, Enterprise


logger = Logger(ln='inspection_sync')
msg = """Scripts: <scripts/inspection_sync.py>"""

def run():
    inspection_guid = Inspection.objects.values_list('guid', flat=True)
    for guid in inspection_guid:
        enterprise_ids = InspectionEnterprise.objects.filter(inspection_id=guid).values_list('enterprise_id', flat=True)

        enterprise = Enterprise.objects.filter(id__in=enterprise_ids)

        inspection_fields = Inspection.objects.filter(guid=guid).values('title', 'url', 'pubtime','source',
        'qualitied', 'unqualitied_patch', 'qualitied_patch', 'inspect_patch', 'category', 'level', 'status', 'industry_id',
        'product_name', 'area_id', 'origin_product')

        if inspection_fields[0]['level'] == '市':
            new_level = 0
        elif inspection_fields[0]['level'] == '省':
            new_level = 1
        elif inspection_fields[0]['level'] == '国':
            new_level = 2

        insepction2 = Inspection2(
            title=inspection_fields[0]['title'],
            url=inspection_fields[0]['url'],
            pubtime=inspection_fields[0]['pubtime'],
            source=inspection_fields[0]['source'],
            qualitied=inspection_fields[0]['qualitied'],
            unqualitied_patch=inspection_fields[0]['unqualitied_patch'],
            qualitied_patch=inspection_fields[0]['qualitied_patch'],
            inspect_patch=inspection_fields[0]['inspect_patch'],
            category=inspection_fields[0]['category'],
            status=inspection_fields[0]['status'],
            level=new_level,
            industry_id=inspection_fields[0]['industry_id'],
            product_name=inspection_fields[0]['product_name'],
            area_id=inspection_fields[0]['area_id'],
            origin_product=inspection_fields[0]['origin_product'],
        )

        if enterprise_ids and enterprise:
            print('!!!!!!', guid)
            for e_id in enterprise_ids:
                try:
                    enterprise = Enterprise.objects.get(id=e_id)
                except Enterprise.DoesNotExist:
                    enterprise = None

                if enterprise:
                    insepction2.save()
                    insepction2.enterprises.add(enterprise)
                    insepction2.save()
        else:
            print('??????', guid)
            insepction2.save()
