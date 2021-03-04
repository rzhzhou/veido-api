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
logger = Logger(ln='video_crawler')
msg = """Scripts: <scripts/video_crawler.py>"""

# 爬取
def run():
	# name = input("请输入影篇名:")
	# url = gat_url(name)
	url = gat_url('海贼王')
	parse_page(url)

def gat_url(name):
	url = 'http://testsea.diyiwl.wang/ssszz.php?top=10&q='+name+'&dect=1'
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

def parse_page(url):
	v_url = ""
	thumb = ""
	title = ""
	times = ""
	catid = ""
	star = ""
	lianzaijs = ""
	beizhu = ""
	alias_full = ""
	area = ""
	sort = ""
	sub_url = ""
	sub_name = ""
	content = get_page(url)

	v_url = re.findall('"url":"(.*?)",',content.text,re.S)

	# v_url = "http://ziziyy.net/" + v_url[0]
	thumb = re.findall('"thumb":"(.*?)",',content.text,re.S)
	title = re.findall('"title":"(.*?)",',content.text,re.S)
	times = re.findall('"time":"(.*?)",',content.text,re.S)
	catid = re.findall('"catid":"(.*?)",',content.text,re.S)
	star = re.findall('"star":"(.*?)",',content.text,re.S)
	lianzaijs = re.findall('"lianzaijs":"(.*?)",',content.text,re.S)
	beizhu = re.findall('"beizhu":"(.*?)",',content.text,re.S)
	alias_full = re.findall('"alias_full":"(.*?)",',content.text,re.S)
	area = re.findall('"area":"(.*?)",',content.text,re.S)
	sort = re.findall('"sort":"(.*?)"}',content.text,re.S)
	for index in range(len(v_url)):
		v_urls = ''
		v_urls = "http://ziziyy.net" + v_url[index]
		print(index,v_urls)

		videodetails = VideoDetails(
			url = v_urls,
			thumb = thumb[index],
			title = title[index],
			time = times[index],
			catid = catid[index],
			star = star[index],
			lianzaijs = lianzaijs[index],
			beizhu = beizhu[index],
			alias_full = alias_full[index],
			area = area[index],
			sort = sort[index],
		)
		videodetails.save()

		time.sleep(5)
		contents = get_page(v_urls)

		selector = etree.HTML(contents.text)

		sub_content = selector.xpath('//div[@id="stab_1_71"]/ul/li/a')
		for index in range(len(sub_content)):
			sub_name = sub_content[index].text
			sub_url = sub_content[index].xpath('./@href')
			print(sub_name,sub_url)
			VideoContent(
				name = sub_name,
				url = sub_url,
				videodetails_id = videodetails.id,
			).save()


