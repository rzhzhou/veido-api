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

        page = int(getattr(self, 'page', 1))
        length = int(getattr(self, 'length', 15))
        title = getattr(self, 'title', None)

        body = {
                "from": page - 1,
                "size": length,
                "sort": [{'pubtime': {"order": "desc"}}],
                "query" : {},
                "highlight" : {
                    "pre_tags" : ["<span class='highlight'>"],
                    "post_tags" : ["</span>"],
                    "fields":{
                      "title":{}
                    }
                },
            }
        if not title:
            body['query']['match_all'] = {}
        else:
            body['query']['match'] = {'title': title}

        return esclient.search(
            index=conf['index'],
            doc_type=conf['type'],
            body=body
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

        page = int(getattr(self, 'page', 1))
        length = int(getattr(self, 'length', 15))
        q1 = getattr(self, 'q1', '')
        q2 = getattr(self, 'q2', '')
        q3 = getattr(self, 'q3', '')
        q4 = getattr(self, 'q4', '')
        q5 = getattr(self, 'q5', '')
        category = getattr(self, 'category', '')
        order = getattr(self, 'order', '')
        area = getattr(self, 'area', '')

        body = {
                "from": page - 1,
                "size": length,
                "query" : {},
                "highlight" : {
                    "pre_tags" : ["<span class='highlight'>"],
                    "post_tags" : ["</span>"],
                    "fields":{
                      "title":{}
                    }
                },
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

        cl = category.split(',')[:-1:]
        if cl:
            if query_string:
                query_string = '%s AND category.name:(%s)' % (query_string, 'OR'.join(cl), )
            else:
                query_string = 'AND category.name:(%s)' % 'OR'.join(cl)

        al = area.split(',')[:-1:]
        if al:
            if query_string:
                query_string = '%s AND area.name:(%s)' % (query_string, 'OR'.join(al), )
            else:
                query_string = 'AND area.name:(%s)' % 'OR'.join(al)

        # sorted
        sort_list = []
        ol = order.split(',')[:-1:]
        if 'pubtime_desc' in ol:
            sort_list.append({'pubtime': {"order": "desc"}})

        if 'pubtime_asc' in ol:
            sort_list.append({'pubtime': {"order": "asc"}})

        if 'score_desc' in ol:
            sort_list.append({'_score': {"order": "desc"}})

        if 'score_asc' in ol:
            sort_list.append({'_score': {"order": "asc"}})



        if not query_string:
            body['query']['match_all'] = {}
        else:
            body['query']['query_string'] = {'query': query_string}

        body['sort'] = [{'pubtime': {"order": "desc"}}, ] if not sort_list else sort_list

        return esclient.search(
            index=conf['index'],
            doc_type=conf['type'],
            body=body
        )
