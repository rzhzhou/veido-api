import requests
import re
import urllib
import time
import random
import json
from bs4 import BeautifulSoup
import re
from django.core.exceptions import ObjectDoesNotExist

from observer.utils.logger import Logger

from observer.base.models import Enterprise, Area, AddInformation


logger = Logger(ln='enterprise_information')
msg = """Scripts: <scripts/enterprise_information.py>"""

def crawlers(name):
	for x in range(len(name)) :
		print(name[x])
		try:
			run2(name[x])
		except Exception as e:
			print(name[x] + '基本信息爬取失败')
		try:
			location(name[x])
		except Exception as e:
			print(name[x] + '经纬度爬取失败')
			continue

		print('\n')

	# run2('齐鲁电缆有限公司')

def run2(name):
	url1=paquurl('https://www.qichacha.com/search?key='+name)
	print(url1)
	if url1 is None:
		print(name+'公司一级链接未找到！')
	# paqu2(a)
	else:
		tableValueList = []
		num = 0
		cookie = "UM_distinctid=1692c9121f53f4-0fba41913ca082-1333063-1fa400-1692c9121f6776; zg_did=%7B%22did%22%3A%20%221692c9127ef367-00035bb2a86a34-1333063-1fa400-1692c9127f08a9%22%7D; _uab_collina=155123090958382328207448; acw_tc=74d3b6ca15589404067368855e2ee48526a763e65b42a8809e53cb3862; QCCSESSID=hb420sfmoai29ld0qt7qj8klm1; CNZZDATA1254842228=1161624522-1551230360-https%253A%252F%252Fwww.google.com%252F%7C1560323840; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1559544057,1559544844,1559618268,1560326644; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201560326643222%2C%22updated%22%3A%201560326788083%2C%22info%22%3A%201560326643231%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22646f87a280ed76d83fa308ba242a4a6f%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1560326788"

		time.sleep(random.uniform(0,10))
		session = requests.Session()
		req =session.get(url1,headers=get_headers(cookie))
		soup = BeautifulSoup(req.text,'lxml')

		tableValueList.append(soup.find('h2' , class_="seo font-20").text)
		for href in soup.find_all('span',class_="cvlu"):
			num = num + 1
			if num==2:
				if href.a == None:
					url = '暂无'
					tableValueList.append(url)
					continue
				url = href.a.get('href')
				if url == None:
					continue

				if href.a == None and url == None:
					url = '暂无'
					continue

				tableValueList.append(url)


		for message in soup(id="Cominfo"):
			table_ntable = message.find_all('table')


			table = 0
			for a in table_ntable:

				if table == 0:
					table += 1
					continue

				compose = 0
				tdNum = 1
				for td in a.find_all('td'):
					# if compose == 0:
					# 	tableKeyList.append(td.get_text("|", strip=True))
					tdText = td.get_text("|", strip=True) # 去掉换行符

					if tdNum == 38:
						tdText = tdText.split('|')[0]
						areaString = tdText

					if compose == 1:
						tableValueList.append(tdText)
						compose = -1

					tdNum += 1
					compose += 1

		try:
			for x in range(len(tableValueList)):
				if x == 14:
					province = tableValueList[x][:-1]
					print(province)

					areas = Area.objects.filter(parent_id__parent__name=province).values_list('name',flat=True)
					if not areas:
						y = Area.objects.filter(name=province).values_list('id',flat=True)
						tableValueList.append(y[0])

				if x == 20:
					for y in areas:
						if tableValueList[x].find(y) != -1:
							y = Area.objects.filter(name=y).values_list('id',flat=True)
							print(y[0])
							tableValueList.append(y[0])
		except Exception as e:
			print(name + '区域名称未找到')




		Enterprise.objects.filter(JGMC=name).update(FDDBR=tableValueList[0],URL=tableValueList[1],
				ZCZJ=tableValueList[3],JYZT=tableValueList[4],TYDM=tableValueList[6],DATATYPE=tableValueList[10],
				JJHY2011=tableValueList[11],PZJGMC=tableValueList[13],ZGDM=tableValueList[19],
				JGDZ=tableValueList[20],JYFW=tableValueList[21])

		try:
			Enterprise.objects.filter(JGMC=name).update(area_id=tableValueList[22])
		except Exception as e:
			print(name + '区域名称未添加成功！')


def get_headers(cookie=''):

	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
		"Cache-Control": "max-age=0",
		"Connection": "keep-alive",
		"Cookie": cookie,
		"Host": "www.qichacha.com",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
	}

	return headers


def paquurl(url):
	cookie = "UM_distinctid=1692c9121f53f4-0fba41913ca082-1333063-1fa400-1692c9121f6776; zg_did=%7B%22did%22%3A%20%221692c9127ef367-00035bb2a86a34-1333063-1fa400-1692c9127f08a9%22%7D; _uab_collina=155123090958382328207448; acw_tc=74d3b6ca15589404067368855e2ee48526a763e65b42a8809e53cb3862; QCCSESSID=hb420sfmoai29ld0qt7qj8klm1; CNZZDATA1254842228=1161624522-1551230360-https%253A%252F%252Fwww.google.com%252F%7C1560323840; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1559544057,1559544844,1559618268,1560326644; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201560326643222%2C%22updated%22%3A%201560326777255%2C%22info%22%3A%201560326643231%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22646f87a280ed76d83fa308ba242a4a6f%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1560326778"
	time.sleep(random.uniform(0,10))
	session =requests.Session()

	req =session.get(url,headers=get_headers(cookie))
	soup = BeautifulSoup(req.text,'lxml')


	for link in soup.find_all('a', 'ma_h1'):
		a=link.get('href')
		return "http://www.qichacha.com"+a


def location(name):
	session =requests.Session()
	headers ={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
			"Cache-Control": "max-age=0",
			"Connection": "keep-alive",
			"Cookie": "guid=9bd4-a37e-32be-e5ee; UM_distinctid=16ab580d42a120-077229500e9df7-6353160-1fa400-16ab580d42b5f4; cna=JyTEFNKADFcCATut2tkztVof; passport_login=MzE3MTQ4NTE3LGFtYXBBOGVnNDZrMGgsdjI2bzJsemVjeXRtdG1heWJkN25reXZoN3pmY3d3dGMsMTU1ODYwMTUzNyxPVEk0TmpVME9ETTNObUV3TVRoaE56WTFNRFl5T0dabU9USmlOV001TmprPQ%3D%3D; isg=BK6u_LwBfn78toqnd9bH7k3V_wSwB3LF4roDA9h1DbFsu00VQDvKuOX6c2fyY2rB; l=bBxY-TM7vVBAsyjiBOfgCuI8ai7t0QAf1sPzw4_GxICPOU5J50PNWZtlxdLvC3GVa6j6R3kM34SbBzY7EyznQ; key=4ec54a768525c215861c75382353da1f; dev_help=YTgFbCnF1KR4h%2FU7TTYOm2FjMmJkMTE5MmY1ZDRlNGI2NjIyZTIyNGIxYWJjNzYwYzUxNDJmN2MyNGUxNjRhOWVmMmMwMjA2OTZiMTc2MWaA3i2muvW93gAGUgzQt7aErqRvdkd4tzEofr2%2BUVzVyf3BLHyRdKCF0BohJJ2428COgrvE8HzzskQwuBxuebKDOeluz2TXxu7QTJ5WCc3HfbfavFPwsKg9guzo1OhUulw%3D",
			"Host": "restapi.amap.com",
			"Upgrade-Insecure-Requests": "1",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
			}
	url = 'https://restapi.amap.com/v3/place/text?key=9d2600cc3d439544bb36cc55becd2b74&keywords='+name+'types=%E4%BC%81%E4%B8%9A&city=&children=1&offset=20&page=1&extensions=all'
	req = session.get(url,headers=headers)
	soup = BeautifulSoup(req.text,'lxml')

	location = json.loads(soup.p.text)['pois'][0]['location']

	x = location.split(',')[0]
	y = location.split(',')[1]


	enterpriseinformation_id = Enterprise.objects.filter(JGMC=name).values_list('id',flat=True)
	print(x,y,enterpriseinformation_id[0])
	addInformation = AddInformation(
		x = x,
		y = y,
		enterprise_id = enterpriseinformation_id[0],
		)
	addInformation.save()






