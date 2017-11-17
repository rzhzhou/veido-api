
import logging

from celery import shared_task

from crawler.service.base import Crawler
from crawler.service.register import Register
from crawler.utils.crawler import get_exception_info

logger = logging.getLogger("crawlerservice")


@shared_task
def service_worker(app, module, crawlerimpl, rank, url, data):

    success = False
    msg = ''

    c = Crawler().create(app, module, crawlerimpl, rank, url, data)

    if c:
        try:
            c.crawl()
            success = True
            msg = 'CRAWL SUCCEED - %s' % c
        except Exception:
            msg = get_exception_info()
            msg = 'CRAWL FAILED - %s, %s' % (c, msg)

    else:
        msg = 'CREATE FAILED - %s' % url

    if success:
        logger.info(msg)
    else:
        logger.error(msg)

    Register.recycle(app, module, crawlerimpl, rank,
                     url, c.data if c else {}, success)
