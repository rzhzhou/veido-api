import jieba
from observer.base.models import KeywordsStatistical

# 通过jieba中文分词库来分析文章title
def cutKeywords(title, eventId):
	keywords = jieba.lcut(title, cut_all=False)

	newlist = []
	for k in keywords:

	    if len(k) > 1:
	    	newlist.append(k)

	for name in newlist:
		keyword = KeywordsStatistical.objects.filter(name = name, events_id = eventId)

		if keyword.exists():
			keyword = keyword[0]
			keyword.number = keyword.number + 1
			keyword.save()
		else:
			KeywordsStatistical(
				name = name,
				number = 1,
				events_id = eventId,
			).save()
