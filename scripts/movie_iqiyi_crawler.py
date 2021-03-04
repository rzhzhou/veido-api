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
logger = Logger(ln='movie_iqiyi_crawler')
msg = """Scripts: <scripts/movie_iqiyi_crawler.py>"""


def run():
	parse_more_page('https://list.iqiyi.com/www/1/-------------11-1-1-iqiyi--.html')


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
	contents = selector.xpath('//ul[@class="qy-mod-ul"]/li')
	for index in range(len(contents)):
		url = contents[index].xpath('./div/div[@class="qy-mod-link-wrap"]/a/@href')
		title = contents[index].xpath('./div/div[2]/p[1]/a/@title')
		star = contents[index].xpath('./div/div[2]/p[2]//a/text()')
		heat = contents[index].xpath('./div/div[2]/p[1]/span/text()')
		print(url,title,star,heat)
