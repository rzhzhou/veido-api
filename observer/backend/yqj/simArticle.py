#coding:utf-8
# chjsun
import jieba
import math
from datetime import timedelta
import datetime
import time
from backend.base.models import Article


class sim_article():

    def __init__(self, title, pubtime):
        self.article = 'article'
        self.title = title
        self.pubtime = pubtime

    def article_result(self):
        result = _cal_values(self.article,self.title,self.pubtime)
        return result


def _comparison_data(article, pubtime):
    if article == "article":
        start_date = pubtime + datetime.timedelta(days=-7)
        return Article.objects.filter(pubtime__lt=pubtime, pubtime__gt=start_date)


def _cal_values(types, title, pubtime):
    """
    Calculate Similar Data

    Return Type List [<Article>, ?, ?]
    """
    result = []
    for article in _comparison_data(types, pubtime):
        if not title or not article.title:
            continue
        value = _compare_title(title, article.title)
        if value > 0.6:
            result.append(article)
    return result


def _compare_title(a, b):
    a = jieba.cut(a)
    b = jieba.cut(b)
    return _compare(a, b)


def _compare(a, b):
    a1 = [x for x in a]
    b1 = [x for x in b]
    union = list(set(a1).union(set(b1)))
    a_count = [a1.count(x) for x in union]
    b_count = [b1.count(x) for x in union]

    numerator = reduce(lambda x, y: x + y, [(a_count[x] * b_count[x]) for x in xrange(len(union))])
    denominator1 = reduce(lambda x, y: x + y, [(a_count[x] ** 2) for x in xrange(len(union))])
    denominator2 = reduce(lambda x, y: x + y, [(b_count[x] ** 2) for x in xrange(len(union))])

    value = numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))

    return value


# if __name__=="__main__":
#     print _compare_title('沃尔玛在华驴肉商品狐狸肉','沃尔玛在华驴肉商品查出狐肉')