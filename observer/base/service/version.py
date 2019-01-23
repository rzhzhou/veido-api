from io import BytesIO

import datetime
from django.core.exceptions import ObjectDoesNotExist

from observer.base.models import VersionRecord
from observer.base.service.abstract import Abstract


class VersionRecordData(Abstract):
    def __init__(self, params):
        super(VersionRecordData, self).__init__(params)

    def get_all(self):

        fields = ('id', 'version', 'content', 'pubtime')

        cond = {}

        args = dict([k, v] for k, v in cond.items() if v)

        queryset = VersionRecord.objects.filter(**args).values(*fields).order_by('-pubtime')

        return queryset


class VersionRecordDataAdd(Abstract):
    def __init__(self, user, params={}):
        super(VersionRecordDataAdd, self).__init__(params)
        self.user = user

    def add(self):
        version = getattr(self, 'version', '')
        content = getattr(self, 'content', '')
        pubtime = datetime.datetime.now()

        if not version or not content or not pubtime:
            return 40

        VersionRecord(
            version = version,
            content = content,
            pubtime = pubtime,
        ).save()

        return 200


class VersionRecordDataEdit(Abstract):
    def __init__(self, user, params={}):
        super(VersionRecordDataEdit, self).__init__(params)
        self.user = user

    def edit(self, cid):
        edit_id = cid
        version = getattr(self, 'version', '')
        content = getattr(self, 'content', '')
        pubtime = getattr(self, 'pubtime', '')


        if not version or not content or not pubtime:
            return 400

        versionrecord = VersionRecord.objects.get(id=edit_id)
        versionrecord.version = version
        versionrecord.content = content
        versionrecord.pubtime = pubtime
        versionrecord.save()

        return 200


class VersionRecordDataDelete(Abstract):
    def __init__(self, user):
        self.user = user

    def delete(self, cid):
        del_ids = cid
        for ids in del_ids.split(","):
            VersionRecord.objects.filter(id=ids).delete()

        return 200
