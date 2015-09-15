class MyDB2Router(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'corpus':
            return 'corpus'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'corpus':
            return 'corpus'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'corpus' or obj2._meta.app_label == 'corpus':
            return True
        return None

    def allow_syncdb(self, db, model):

        if db == 'corpus':
            return model._meta.app_label == 'corpus'
        elif model._meta.app_label == 'corpus':
            return False
        return None