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
from scapy.all import *

# init logging
logger = Logger(ln='source_crawler')
msg = """Scripts: <scripts/source_crawler.py>"""

def run():
	urls = 'https://www.iqiyi.com/v_pa5rm8r7do.html'
	urls = 'https://jx.618g.com/?url=' + urls
	# urls = 'https://jx.618g.com/?url=https://www.iqiyi.com/v_1dgrhxvammc.html'

	source = get_page(urls)
	print(source.text)
	selector = etree.HTML(source.text)

	print(selector)
	sub_content = selector.xpath('//div[@id="a1"]/iframe/@src')
	print(sub_content)
	sub_content = sub_content[0].split("?url=")[1]
	print(sub_content)


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