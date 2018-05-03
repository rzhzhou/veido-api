# OBSERVER/ADMIN ES_API

### ES_API 概览

| 接口编号 |    接口名称   | 接口功能    |  请求方式 |
| :------| :---------- | :---------- |:-------- |
| **0001** | /observer/article/_search | 全文检索 | POST |


*****
### API 详细信息

*****
### **0001**

**1. 接口描述**

本接口 (/observer/article/\_search) 用于全文检索.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| query.match.title | String  |  是     | 标题。|
| highlight | Dict  |  否     | 高亮搜索。 注①|

注：
- ①: [高亮搜索](https://www.elastic.co/guide/cn/elasticsearch/guide/cn/highlighting-intro.html)

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| guid | String | GUID |
| invalid_keyword | String | 无效关键词 |
| pubtime | String | 发布时间 |
| risk_keyword | String | 风险关键词 |
| score | String | 风险程度 |
| source | String | 信息来源 |
| status | String | 状态. 1：有效，0：默认，-1：无效 |
| title | String | 标题 |
| url | String | URL |

**4. 实例**

输入

```
http://192.168.0.104:9200/observer/article/_search
{
    "query" : {
      "match" : {
        "title" : "国抽" 
      }
    },
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "title" : {}
        }
    }
}
```

输出
```
{
  "took": 25,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": 24,
    "max_score": 4.282371,
    "hits": [
      {
        "_index": "observer",
        "_type": "article",
        "_id": "42afce075ef4af3eae32fd28532749a5",
        "_score": 4.282371,
        "_source": {
          "guid": "42afce075ef4af3eae32fd28532749a5",
          "invalid_keyword": "",
          "pubtime": "2018-03-13T00:00:00+08:00",
          "risk_keyword": "",
          "score": 3,
          "source": "中国经济网",
          "status": 0,
          "title": "质检总局：2018年第1批“国抽”产品不合格率7.66%",
          "url": "http://www.ce.cn/cysc/newmain/yc/jsxw/201803/13/t20180313_28458734.shtml"
        },
        "highlight": {
          "title": [
            "质检总局：2018年第1批“<tag1>国</tag1><tag1>抽</tag1>”产品不合格率7.66%"
          ]
        }
      },
      ...
    ]
  }
}
```

