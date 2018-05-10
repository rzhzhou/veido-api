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
