from elasticsearch import Elasticsearch

from observer.base.service.abstract import Abstract


class SearchData(Abstract):

    def __init__(self, params):
        super(SearchData, self).__init__(params)

    def get_all(self):
        conf ={
            'host': '192.168.0.104',
            'port': '9200',
            'index': 'observer',
            'type': 'article',
        }
        esclient = Elasticsearch([conf])

        start = getattr(self, 'start', 1)
        length = getattr(self, 'length', 15)
        title = getattr(self, 'title', None)

        body = {
                "query" : {},
                "from": start - 1,
                "size": length,
            }

        if not title:
            body['query']['match_all'] = {}
        else:
            body['query']['match'] = {'title': title}

        return esclient.search(
            index=conf['index'],
            doc_type=conf['type'],
            body=body,
        )


class SearchAdvancedData(Abstract):

    def __init__(self, params):
        super(SearchAdvancedData, self).__init__(params)

    def get_all(self):
        conf ={
            'host': '192.168.0.104',
            'port': '9200',
            'index': 'observer',
            'type': 'article',
        }
        esclient = Elasticsearch([conf])

        start = getattr(self, 'start', 1)
        length = getattr(self, 'length', 15)
        q1 = getattr(self, 'q1', None)
        q2 = getattr(self, 'q2', None)
        q3 = getattr(self, 'q3', None)
        q4 = getattr(self, 'q4', None)
        q5 = getattr(self, 'q5', None)
        category = getattr(self, 'category', None)
        order = getattr(self, 'order', None)
        area = getattr(self, 'area', None)

        body = {
                "query" : {},
                "from": start - 1,
                "size": length,
            }

        query_string = ""
        if q1:
            query_string += q1
            if q3:
                query_string += ' AND '
                q3l = q3.split(' ')
                if len(q3l) > 1:
                    query_string += '( %s )' % ' OR '.join(q31)
                else:
                    query_string += '( %s )' % q3

        if q2:
            q2l = q2.split(' ')
            if len(q2l) > 1:
                query_string += ' +'.join(q2l)
            else:
                query_string += ' +%s' % q2

        if q4:
            q4l = q4.split(' ')
            if len(q4l) > 1:
                query_string += ' -'.join(q4l)
            else:
                query_string += ' -%s' % q4

        if q1 or q2 or q3 or q4:
            query_string = 'title:(%s)' % query_string

        if query_string:
            if q5:
                query_string = '%s AND source:(%s)' % (query_string, q5, )
        else:
            if q5:
                query_string = ' source:(%s)' % q5



        if not query_string:
            body['query']['match_all'] = {}
        else:
            body['query']['query_string'] = {'query': query_string}

        print(query_string)
        return esclient.search(
            index=conf['index'],
            doc_type=conf['type'],
            body=body,
        )
