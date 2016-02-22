# -*- coding: utf-8 -*-
from observer.apps.riskmonitor.models import(
    ScoreIndustry, ScoreEnterprise, ScoreProduct, )
from observer.apps.corpus.models import(
    Corpus, )
from businesslogic.abstract import(
    Abstract, )

class HomeData(Abstract):
    def __init__(self, start, end):
        self.start = start
        self.end = end
	
    def risk_status(self):
        return 'A'
    
    def risk_sum(self):
        indusum = ScoreIndustry.objects.filter(
            pubtime__range=(self.start, self.end), score__gte=60).count()
        entesum = ScoreEnterprise.objects.filter(
            pubtime__range=(self.start, self.end), score__gte=60).count()
        prodsum = 6
        names = ['industry', 'enterprise', 'product']
        option = [{'Industry':indusum}, {'Enterprise': entesum}, {'Product': prodsum}]
        datas = []
        for index, i in enumerate(option):
            print i
            data = {
                'link': i.keys()[0], 
                'amount': i.values()[0],	    
                'icon': i.keys()[0].lower(), 
                'name': names[index]
                }
            datas.append(data)
        return datas 

    def industry(self):
        type = 'abstract'
        indunames = self.risk_industry(self.start, self.end, type)	
        data = {
                'msg': 'dengji',
                'title': 'fxhyTOP',
                'items': [{'name': induname[0], 'level':induname[1] } for induname in indunames] 
        }
        return data 
	
    def enterprise(self):
        type = 'abstract'
        enteobjects = self.risk_enterprise(self.start, self.end, type)
        data = {
            'msg': 'dengji',
            'title': 'fxqiyeTOP',
            'items': [{'name': enteobject[0].name, 'level':enteobject[1] } for enteobject in enteobjects] 
        }
        return data
  
    def risk_keywords(self):
        keywords = Corpus.objects.all()
        keywords = keywords[0].riskword.split(' ')
        data = {
            'msg': 'shuliang',
            'title': 'fxgjzTOP',
            'items': [{'name': keyword, 'level': 5} for keyword in keywords]
        }
        return data

    def risk_data(self):	
        type = 'abstract'
        nums = self.news_nums(self.start, self.end, type)
        data = {
            'curve': True,
            'data': nums,
            'labels': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
            'id': 'riskData'
        }
        return data
         	
    def risk_level(self):
        type = 'abstract'
        data = {
            'curve': False,
            'data': [1, 2, 1, 3, 1, 2, 1],
            'labels': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
            'id': 'rankData'
        }
        return data

    def get_all(self):
        datas = [
            self.risk_status(),
            self.risk_sum(),
            self.industry(),
            self.enterprise(),
            self.risk_keywords(),
            self.risk_data(),
            self.risk_level(),
        ] 
        return datas            










	 
