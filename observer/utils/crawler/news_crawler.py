# encoding:utf-8
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz,process
import jieba.posseg as pseg
import jieba
import time
import datetime
import random

from observer.utils.str_format import str_to_md5str
from observer.base.models import (Article, Area, ArticleArea, Category, ArticleCategory)

jieba.load_userdict('observer/utils/dictionary.txt') # 引用自定义分词库 

def newsCrawler(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    
    soup = BeautifulSoup(res.text, 'lxml')

    for i, j in zip(soup.find_all('h3'), soup.find_all("div",class_="c-title-author")):
        news_url = i.a.get('href')
        title = i.a.get_text().strip()
        news_time = j.get_text().split() # 此处会获得 某某报纸网站  和发布时间，运用split() 可以把某某报纸网站和时间分离成词典。
        newspaper = news_time[0] # 取索引头一个是 某某报纸网站
        _time = news_time[1] # 取索引第二个是 发布时间
        guid_id = str_to_md5str(news_url) # 根据链接，加密处理它然后获得唯一标识符
        score_rand = random.randint(0,1)
        status = 2 # 状态
        category = "特种设备"
        # 根据新闻来源过滤不需要的新闻
        newspaper_voc = ('东方财富网', 'IT168', '中国财经报网', '上海热线', '中国起重机械网', '和讯',
         '腾讯大楚网', '政府采购信息网', '市场信息报', '食品伙伴网', '食安中国', '40407网页游戏', '365地产家居网','凤凰娱乐','搜房网')
        title_voc = ('食品','药品','化妆品','广告','加装电梯','电梯品牌','AI','','','','','','','','')
        similarity = 0  # 相似度变量
        similarity_title = 0

        for newspaper_i, title_j in zip(newspaper_voc, title_voc):
            similarity = fuzz.partial_ratio(newspaper, newspaper_i)
            similarity_title = fuzz.partial_ratio(title,title_j)

            if similarity == 100:
                if similarity_title == 100:
                    break
                break
            elif similarity_title == 100:
                break

        if similarity != 100 and similarity_title != 100:
            
            # 在标题中获取地域的信息
            if title.strip().find('省市') != -1:
                new_words = title.strip().replace('省市', '')
            elif title.strip().find('省') != -1:
                new_words = title.strip().replace('省', '')
            elif title.strip().find('市') != -1:
                new_words = title.strip().replace('市', '')
            elif title.strip().find('县') != -1:
                new_words = title.strip().replace('县', '')
            else:
                new_words = title.strip()

            
            areas = pseg.cut(new_words) #  根据自定义分词库来切割出所需地域分词
            area_real = '' # 先设置一个空变量，以便储存下面获得地域
            m = 0
            for area,flag in areas:
                if flag == 'findarea':
                    m += 1
                    if m >= 2:
                        continue
                    area_real = area
                if m == 0:
                    area_real = '全国'
                
            # 获取Area库里的id编号，然后存入ArticleArea，存入方法是将与唯一标识符a_guid绑定，等取出来时，根据a_guid取出来
            area_id = Area.objects.filter(name = area_real)[0].id
            category_id =  Category.objects.filter(name = category)[0].id
            if not ArticleArea.objects.filter(article_id = guid_id, area_id = area_id).exists():
                ArticleArea(
                    article_id = guid_id,
                    area_id = area_id
                ).save()
            if not ArticleCategory.objects.filter(article_id = guid_id, category_id = category_id).exists():
                ArticleCategory(
                    article_id=guid_id,
                    category_id=category_id
                ).save()

            # 接下来处理时间，处理为纯数字，用来下面判断是否为今天的新闻
            _time_two = news_time[1]
            _time_two = _time_two.split('年')
            _time_two = ''.join(_time_two)
            _time_two = _time_two.split('月')
            _time_two = ''.join(_time_two)
            _time_two = _time_two.strip('日')

            # 根据处理，来判断，若是纯数字，则不是今天的新闻，直接在原数据上修改，否则，获取系统时间来覆盖原来的数据
            if _time_two.isdigit():
                _time = _time.replace('年','-')
                _time = _time.replace('月','-')
                _time = _time.strip('日')
                

                Article(
                    guid = guid_id,
                    title = title,
                    url = news_url,
                    score = score_rand,
                    source = newspaper,
                    pubtime = _time,
                    status = status
                ).save()
                    
                    
            else:
                _time = datetime.date.today()  # time.strftime('%Y-%m-%d', time.localtime(time.time()))
                
                Article(
                    guid = guid_id,
                    title = title,
                    url = news_url,
                    score = score_rand,
                    source = newspaper,
                    pubtime = _time,
                    status = status
                ).save()