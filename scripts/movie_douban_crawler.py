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
logger = Logger(ln='movie_douban_crawler')
msg = """Scripts: <scripts/movie_douban_crawler.py>"""


def run():
	for page_num in range(0,2):
		page_start = page_num * 20
		parse_more_page('https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='+ str(page_start))


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
	d_url = re.findall('"url":"(.*?)",',content.text,re.S)
	d_thumb = re.findall('"cover":"(.*?)",',content.text,re.S)
	d_score = re.findall('"rate":"(.*?)",',content.text,re.S)
	d_title = re.findall('"title":"(.*?)",',content.text,re.S)

	for index in range(len(d_url)):

		print(d_url[index],d_thumb[index],d_score[index],d_title[index])
