from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import Area
from observer.utils.date_format import date_format


def area(area_id):
    try:
        return Area.objects.get(id=area_id).name
    except ObjectDoesNotExist:
        return '未知'