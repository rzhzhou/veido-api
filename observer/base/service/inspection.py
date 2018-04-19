from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import(Inspection, )
from observer.base.service.abstract import Abstract
from observer.utils.str_format import str_to_md5str


class InspectionData(Abstract):

    def __init__(self, params):
        super(InspectionData, self).__init__(params)

    def get_all(self):

        fields = ('guid', 'title', 'url', 'pubtime', 'source', 'unitem', 'qualitied', 'category', 'level', 'industry_id', 'area_id', )

        cond = {
            'pubtime__gte': getattr(self, 'starttime', None),
            'pubtime__lt': getattr(self, 'endtime', None),
            # 'qualitied__gte': getattr(self, 'starttime', None),
            # 'qualitied__lt': getattr(self, 'endtime', None),
            'category__contains': getattr(self, 'category', None),
            'level': getattr(self, 'level', None),
            'area': getattr(self, 'area', None),
        }

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = Inspection.objects.exclude(status=-1).filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class InspectionDataAdd(Abstract):

    def __init__(self, user, params={}):
        super(InspectionDataAdd, self).__init__(params)
        self.user = user

    def add(self):
        title = getattr(self, 'title', '')
        url = getattr(self, 'url', '')
        pubtime = getattr(self, 'pubtime', '')
        source = getattr(self, 'source', '')
        qualitied = getattr(self, 'qualitied', '')
        category = getattr(self, 'category', '')
        level = getattr(self, 'level', '')
        unitem = getattr(self, 'unitem', '')
        industry_id = getattr(self, 'industry_id', '')
        area_id = getattr(self, 'area_id', '')

        if not url or not pubtime or not source or not qualitied or not category or not level or not industry_id or not area_id:
            return 400

        guid = str_to_md5str('{0}{1}'.format(url, industry_id))

        if Inspection.objects.filter(guid=guid).exists():
            return 202

        Inspection(
            guid=guid,
            title=title,
            url=url,
            pubtime=pubtime,
            source=source,
            unitem=unitem,
            qualitied=qualitied,
            category=category,
            level=level,
            industry_id=industry_id,
            area_id=area_id,
            status=1,
        ).save()

        return 200


class InspectionDataEdit(Abstract): 

    def __init__(self, user, params={}):
        super(InspectionDataEdit, self).__init__(params)
        self.user = user

    def edit(self, aid):
        edit_id = aid
        title = getattr(self, 'title', '')
        url = getattr(self, 'url', '')
        pubtime = getattr(self, 'pubtime', '')
        source = getattr(self, 'source', '')
        qualitied = getattr(self, 'qualitied', '')
        category = getattr(self, 'category', '')
        level = getattr(self, 'level', '')
        unitem = getattr(self, 'unitem', '')
        industry_id = getattr(self, 'industry_id', '')
        area_id = getattr(self, 'area_id', '')

        if not url or not pubtime or not source or not qualitied or not category or not level or not industry_id or not area_id:
            return 400

        guid = str_to_md5str('{0}{1}'.format(url, industry))

        inspection = Inspection.objects.get(guid=edit_id)
        inspection.title = title
        inspection.url = url
        inspection.pubtime = pubtime
        inspection.source = source
        inspection.qualitied = qualitied
        inspection.category = category
        inspection.level = level
        inspection.unitem = unitem
        inspection.industry_id = industry_id
        inspection.area_id = area_id
        inspection.save()

        if guid != edit_id:
            Inspection.objects.filter(guid=guid).delete()

        return 200


class InspectionDataDelete(Abstract): 

    def __init__(self, user):
        self.user = user

    def delete(self, aid):
        del_id = aid
        Inspection.objects.filter(guid=del_id).update(status=-1)
        
        return 200


class InspectionDataUpload(Abstract): 

    def __init__(self, user):
        self.user = user

    def upload(self, file_obj):
        print(file_obj)

        return 200
