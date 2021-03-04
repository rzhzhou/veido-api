from observer.utils.date_format import (str_to_date, get_months)
from observer.utils.str_format import (str_to_md5str, )
from observer.utils.logger import Logger
from observer.apps.dyy.models import (VideoDetails, VideoContent)
import requests
from lxml import etree
from requests.exceptions import RequestException
import re
from lxml import html
import time


# init logging
logger = Logger(ln='details_douban_crawler')
msg = """Scripts: <scripts/details_douban_crawler.py>"""


def run():
	parse_more_page('https://movie.douban.com/subject/26754233/?tag=%E7%83%AD%E9%97%A8&from=gaia_video')


def get_page(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }
        response = requests.get(url=url,headers=headers)
        # 更改编码方式，否则会出现乱码的情况
        response.encoding = "utf-8"
        # print(response.status_code)
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        return None

def parse_more_page(url):
    content = get_page(url)

    selector = etree.HTML(content.text)

    # contents = selector.xpath('//div[@class="subject clearfix"]/div[@id="info"]//span/span/text()')
    d_director = selector.xpath('//div[@class="subject clearfix"]/div[@id="info"]/span[1]/span[2]/a/text()')
    d_star = selector.xpath('//div[@class="subject clearfix"]/div[@id="info"]/span[3]/span[2]//a/text()')
    d_videotype = selector.xpath('//div[@class="subject clearfix"]/div[@id="info"]//span[@property="v:genre"]/text()')
    d_introduction = selector.xpath('//div[@id="link-report"]/span/text()')
    print(d_language)
