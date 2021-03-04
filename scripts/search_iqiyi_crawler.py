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
logger = Logger(ln='search_iqiyi_crawler')
msg = """Scripts: <scripts/search_iqiyi_crawler.py>"""

# 爬取
def run():
	# name = input("请输入影篇名:")
	# url = gat_url(name)
	url = gat_url('海贼王')
	# url = gat_url('大秦赋')
	pagenum = parse_pagenumber(url)
	print(pagenum)
	if pagenum == 0:
		print('000')
	else:
		print(pagenum)
		for i in range(len(pagenum)):
			print('第'+ str(i + 1) +'页..')
			parse_more_page(url, i + 1)



def gat_url(name):
	url = 'https://so.iqiyi.com/so/q_' + name
	return url

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

def get_more_page(url,pageNum):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }
        data = {
        	'pageNum': pageNum,
        }
        response = requests.post(url=url,headers=headers,data=data)
        # 更改编码方式，否则会出现乱码的情况
        response.encoding = "utf-8"
        # print(response.status_code)
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        return None


def parse_pagenumber(url):
	print(url)
	content = get_page(url)

	selector = etree.HTML(content.text)

	sub_page = selector.xpath('//div[@class="csPpFeed_comPage com-mod-small"]/span')

	if not sub_page:
		return 0
	else:
		pages = 0
		for index in range(len(sub_page)):
			page = sub_page[index].xpath('./a/text()')
			if page:
				pages = 0
				pages = page[0]
		return pages

def parse_more_page(url, pagenum):
	print(url)
	content = get_more_page(url, pagenum)

	selector = etree.HTML(content.text)

	sub_content = selector.xpath('//div[@class="qy-mod-img vertical mod_132_176"]')
	for index in range(len(sub_content)):
		title = sub_content[index].xpath('./div/a/@title')
		url = sub_content[index].xpath('./div/a/@href')
		thumb = sub_content[index].xpath('./div/a/img/@src')
		print(title,url,thumb)

