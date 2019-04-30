from aip import AipNlp
import json

# 百度情感分析AI
def BaiDuAI(title):
	APP_ID = '15920055'
	API_KEY = 'uL33axnNAGZVQAic4V7mEwUm'
	SECRET_KEY = '0aplcVN8GVZgt1KVS0MlEn7qKouiDEnN'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	result = client.sentimentClassify(title);

	string = json.dumps(result, ensure_ascii=False)
	Todict = json.loads(string)['items']

	sentiment = Todict[0]['sentiment']

	return sentiment