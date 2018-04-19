# OBSERVER/ADMIN API

### API 概览

| 接口编号 |    接口名称   | 接口功能    |  请求方式 |
| :------| :---------- | :---------- |:-------- |
| **0001** | industries | 行业列表 | GET |
| **0002** | ccc | 3C行业列表 | GET |
| **0003** | ccc/<int:id>/ | 3C行业 | GET |
| **0004** | license | 许可证行业列表 | GET |
| **0005** | license/<int:id>/ | 许可证行业 | GET |
| **0006** | articles/0001/ | 质监热点列表 | GET |
| **0007** | articles/0002/ | 风险快讯列表 | GET |
| **0008** | articles/0003/ | 业务信息列表 | GET |
| **0009** | inspections | 抽检信息列表 | GET |
| **1000** | dmlinks | 指定网站监测列表 | GET |
| **1001** | dmlink/add | 指定网站监测 添加 | POST |
| **1002** | dmlink/edit/<int:id>/ | 指定网站监测 修改 | POST |
| **1003** | dmlink/delete/<int:id>/ | 指定网站监测 删除 | DELETE |
| **1004** | dmwords | 指定关键词监测列表 | GET |
| **2001** | select2/industries | 查询行业 | GET |
| **2002** | select2/areas | 查询地域 | GET |
| **2003** | select2/alias_industries | 查询行业别名 | GET |
| **2004** | select2/ccc_industries | 查询3C行业 | GET |
| **2005** | select2/license_industries | 查询许可证行业 | GET |
| **3001** | risk_data | 风险数据列表 | GET |
| **30011** | risk_data/add | 风险数据添加 | POST |
| **30012** | risk_data/edit/<str:guid>/ | 风险数据修改 | POST |
| **30013** | risk_data/delete/<str:guid>/ | 风险数据删除 | DELETE |
| **30014** | risk_data/upload | 风险数据上传 | PUT |
| **3002** | inspection_data | 抽检数据列表 | GET |
| **30021** | inspection_data/add | 抽检数据添加 | POST |
| **30022** | inspection_data/edit/<str:guid>/ | 抽检数据修改 | POST |
| **30023** | inspection_data/delete/<str:guid>/ | 抽检数据删除 | DELETE |
| **30024** | inspection_data/upload | 抽检数据上传 | PUT |
| **3003** | alias_industry/add | 产品(行业别名添加) | POST |
| **3004** | corpus | 语料词列表 | GET |
| **30041** | corpus/add | 语料词添加 | POST |
| **30042** | corpus/edit | 语料词修改 | POST |
| **30043** | corpus/delete | 语料词删除 | DELETE |

*****
### API 详细信息

*****
### **0001**

**1. 接口描述**

本接口 (industries) 用于获取行业列表数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| l1 | Int        |  否     | 大类ID。|
| l2 | Int        |  否     | 中类ID。|
| l3 | Int        |  否     | 小类ID。|

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| l1 | List | 对应 Table 第一列 |
| l2 | List | 对应 Table 第二列 |
| l3 | List | 对应 Table 第三列 |
| l4 | List | 对应 Table 第四列 |
| id | Int | 行业ID |
| name | String | 行业名称 |
| desc | String | 行业描述 |
| ccc_id | Int | 3C行业ID。注：该字段用来标识当前行业是否3C行业，若为 0 ，则说明不是，否则是。 |
| license_id | Int | 许可证行业ID。注：该字段用来标识当前行业是否许可证行业，若为 0 ，则说明不是，否则是。 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/industries?
l1=13&
l2=131&
l3=1311

```

输出
```
{
    "list": [
        {
            "l2": {
                "id": 131,
                "desc": "也称粮食加工，指将稻谷、小麦、玉米、谷子、高粱等谷物去壳、碾磨，加工为成品粮的",
                "name": "谷物磨制"
            },
            "l4": [
                {
                    "ccc_id": 13111,
                    "id": 4,
                    "name": "电线电缆",
                    "license_id": 0
                }
            ],
            "l1": {
                "id": 13,
                "desc": "指直接以农、林、牧、渔业产品为原料进行的谷物磨制、饲料加工、植物油和制糖加工、屠宰及肉类加工、水产品加工，以及蔬菜、水",
                "name": "农副食品加工业"
            },
            "l3": {
                "id": 1311,
                "desc": "指将稻谷去壳、碾磨成大米的生产活动",
                "name": "稻谷加工"
            }
        }
    ],
    "total": 1
}
```


*****
### **0002**

**1. 接口描述**

占位用，该 API 未实现。


*****
### **0003**

**1. 接口描述**

本接口 (ccc/<int:id>/) 用于获取3C行业数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| id | Int        |  是     | 行业ID。 注：通常对应行业列表第四列中的ccc_id|

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| l1 | List | 对应 Table 第一列 |
| l2 | List | 对应 Table 第二列 |
| l3 | List | 对应 Table 第三列 |
| id | Int | 行业ID |
| name | String | 行业名称 |
| desc | String | 行业描述 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/ccc/1000/
```

输出
```
{
    "total": 1,
    "list": [
        {
            "l1": {
                "desc": "",
                "id": 1000,
                "name": "测试用产品"
            },
            "l3": {
                "desc": "",
                "id": 1003,
                "name": "测试用产品3"
            },
            "l2": {
                "desc": "",
                "id": 1001,
                "name": "测试用产品2"
            }
        }
    ]
}
```


*****
### **0004**

**1. 接口描述**

占位用，该 API 未实现。


*****
### **0005**

**1. 接口描述**

本接口 (license/<int:id>/) 用于获取许可证行业数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| id | Int        |  是     | 行业ID。 注：通常对应行业列表第四列中的license_id|

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| l1 | List | 对应 Table 第一列 |
| l2 | List | 对应 Table 第二列 |
| l3 | List | 对应 Table 第三列 |
| id | Int | 行业ID |
| name | String | 行业名称 |
| desc | String | 行业描述 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/license/1000/
```

输出
```
{
    "total": 1,
    "list": [
        {
            "l1": {
                "desc": "",
                "id": 1000,
                "name": "测试用产品"
            },
            "l3": {
                "desc": "",
                "id": 1003,
                "name": "测试用产品3"
            },
            "l2": {
                "desc": "",
                "id": 1001,
                "name": "测试用产品2"
            }
        }
    ]
}
```


*****
### **0006**

**1. 接口描述**

本接口 (articles/0001/) 用于获取质监热点数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| starttime| Date        |  否     | 开始时间. |
| endtime| Date        |  否     | 结束时间 |
| title| String        |  否     | 标题。注：模糊匹配 |
| source| String        |  否     | 来源。注：模糊匹配 |
| areas | Int        |  否     | 地域ID列表。注：精确匹配(多选)。select2 |


**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| url | String | 网址 |
| title | String | 标题 |
| source | String | 来源 |
| areas | List | 地域的列表 |
| pubtime | String | 发布时间 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/articles/0001/
```

输出
```
{
    "total": 61,
    "list": [
        {
            "areas": [
                "咸宁"
            ],
            "source": "中国质量新闻网",
            "url": "http://www.cqn.com.cn/cj/content/2018-03/26/content_5592714.htm",
            "pubtime": "2018-03-26",
            "title": "梁朝伟代言的丸美IPO:3年砸10亿做广告 产品屡上质检黑榜"
        },
        ...
    ]
}
```


*****
### **0007**

**1. 接口描述**

本接口 (articles/0002/) 用于获取风险快讯数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| starttime| Date        |  否     | 开始时间. |
| endtime| Date        |  否     | 结束时间 |
| title| String        |  否     | 标题。注：模糊匹配 |
| source| String        |  否     | 来源。注：模糊匹配 |
| areas | Int        |  否     | 地域ID列表。注：精确匹配(多选)。select2 |
| score | Int        |  否     | 风险程度。注：精确匹配(单选)。select2：1-低，2-中，3-高|


**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| url | String | 网址 |
| title | String | 标题 |
| source | String | 来源 |
| areas | List | 地域的列表 |
| pubtime | String | 发布时间 |
| score | Int | 风险程度。注：0-无，1-低，2-中，3-高 |
| local_related | Int | 本地相关。注：1-低，2-中，3-高  |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/articles/0002/
```

输出
```
{
    "total": 52,
    "list": [
        {
            "url": "http://www.cqn.com.cn/cj/content/2018-03/26/content_5592714.htm",
            "areas": [
                "咸宁"
            ],
            "score": 0,
            "local_related": 1,
            "pubtime": "2018-03-26",
            "title": "梁朝伟代言的丸美IPO:3年砸10亿做广告 产品屡上质检黑榜",
            "source": "中国质量新闻网"
        },
        ...
    ]
}
```


*****
### **0008**

**1. 接口描述**

本接口 (articles/0003/) 用于获取业务信息数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| starttime| Date        |  否     | 开始时间. |
| endtime| Date        |  否     | 结束时间 |
| title| String        |  否     | 标题。注：模糊匹配 |
| source| String        |  否     | 来源。注：模糊匹配 |
| areas | Int        |  否     | 地域ID列表。注：精确匹配(多选)。select2 |
| categories | String        |  否     | 业务类别ID。注：精确匹配(单选)。select2：00039-质量管理，00038-认证监管，00037-计量，00036-特种设备，00035-科技兴检，00034-质量监管，00033-稽查打假，00032-标准化，00031-综合 |


**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| url | String | 网址 |
| title | String | 标题 |
| source | String | 来源 |
| area | List | 地域的列表 |
| pubtime | String | 发布时间 |
| areas | List | 地域的列表 |
| categories | List | 类别的列表 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/articles/0003/
```

输出
```
{
    "total": 61,
    "list": [
        {
            "source": "中国新闻网",
            "categories": [
                "特种设备",
                "认证监管",
                "质量管理"
            ],
            "title": "对儿童安全构成威胁 指尖陀螺被欧盟列为危险品",
            "areas": [
                "北京",
                "上海"
            ],
            "url": "http://dw.chinanews.com/chinanews/content.jsp?id=8467281&classify=zw&pageSize=6&language=chs",
            "pubtime": "2018-03-14"
        },
        ...
    ]
}
```

*****
### **0009**

**1. 接口描述**

本接口 (inspections) 用于获取业务信息数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| starttime| Date        |  否     | 开始时间. |
| endtime| Date        |  否     | 结束时间 |
| title| String        |  否     | 标题。注：模糊匹配 |
| source| String        |  否     | 行政单位。 注：模糊匹配 |
| category| String        |  否     | 抽查类别。 注：模糊匹配 |
| level | Int        |  否     | 抽查级别。 值范围(国 省 市)。 注：精确匹配(单选)。select2 |
| area | Int        |  否     | 地域ID。注：精确匹配(单选)。select2 |


**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| category | String | 抽查类别 |
| qualitied | Double | 抽查合格率 |
| url | String | 网址 |
| industry | String | 产品类别 |
| pubtime | Date | 发布时间 |
| area | String | 抽查地区 |
| level | String | 抽查级别 |
| source | String | 行政单位 |


**4. 实例**

输入

```
http://192.168.0.103:8001/api/inspections
```

输出
```
{
    "total": 18,
    "list": [
        {
            "category": "监督抽查",
            "qualitied": 1.0,
            "url": "http://www.zjbts.gov.cn/HTML/cctg/201803/bca33649-bb42-4046-a529-6b68e27d4aaa.html",
            "industry": "电线电缆 - 许可证",
            "pubtime": "2018-03-26",
            "area": "浙江",
            "level": "省",
            "source": "浙江省质监局"
        },
        ...
    ]
}
```


*****
#### **1000**

**1. 接口描述**

本接口 (dmlinks) 获取当前用户所有指定监测。

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页数。值范围 1~+∞|
| length | Int       |  是     | 列表长度。值范围 15~+∞|

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| name | String | 网站名。 |
| link | String | 网址。 |
| kwords | String | 关键词 |
| fwords | String | 过滤关键词 |
| status | String | 状态。 值范围：(0：待执行；1：执行中；2：完成) |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/dmlinks
```

输出
```
{
    "total": 2,
    "list": [
        {
            "name": "test",
            "kwords": "test1 test2 test3",
            "status": 0,
            "fwords": "test4 test5",
            "link": "http://localhost:8000/admin/base/dmlink/add/"
        }
        ...
    ]
}
```


*****
### **1001**

**1. 接口描述**

本接口 (dmlink/add) 用于新增风险数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| name | String        |  是     | 网站名. |
| link | String        |  是     | 网址. |
| kwords | String        |  否     | 关键词. |
| fwords | String        |  否     | 过滤词. |
| remarks | String        |  否     | 备注信息. |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 1 | Int | 成功 |
| 0 | Int | 服务器异常 |
| -1 | Int | name 为必填项 |
| -2 | Int | link 为必填项 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
#### **1002**

**1. 接口描述**

本接口 (dmlink/edit/<int:id>/) 用于编辑指定监测. 

Tips: 
- <int:id>: 需要修改的指定监测ID

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| name | String        |  是     | 网站名. |
| link | String        |  是     | 网址. |
| kwords | String        |  否     | 关键词. |
| fwords | String        |  否     | 过滤词. |
| remarks | String        |  否     | 备注信息. |

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| 1 | Int | 成功 |
| 0 | Int | 服务器异常 |
| -1 | Int | name 为必填项 |
| -2 | Int | link 为必填项 |

**4. 实例**

输入

```
略
```

输出
```
略
```

*****
#### **1003**

**1. 接口描述**

本接口 (dmlink/delete/<int:id>/) 用于删除指定监测. 

Tips: 
- <int:id>: 需要删除的指定监测ID

**2. 输入参数**

无

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| 1 | Int | 成功 |
| 0 | Int | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
#### **1004**

**1. 接口描述**

本接口 (dmwords) 获取所有指定关键词监测。

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页数。值范围 1~+∞|
| length | Int       |  是     | 列表长度。值范围 15~+∞|

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| riskword | String | 风险语料词 |
| invalidword | String | 无效词 |
| industry | String | 行业 |


**4. 实例**

输入

```
http://192.168.0.103:8001/api/dmwords
```

输出
```
{
    "total": 2,
    "list": [
        {
            "invalidword": "绿帽 戴帽 如何 贫困 笔 穷 高帽 摘",
            "riskword": "风险 劣质 假冒 PH值 褪色 抽查 违规 致癌 防腐剂 产品质量 召回 不安全 纤维含量 造假 质监 污染 甲醛含量 不合格 投诉 抽检 三无 超标 不达标 伤害 整改 预警 异物 色素 异味 隐患",
            "industry": "电线电缆"
        }
        ...
    ]
}
```


*****
### **2001**

**1. 接口描述**

本接口 (select2/industries) 用于查询行业。

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| level |  Int    |  是    | 精确匹配。 值范围：{1：大类, 2：中类, 3：小类}|
| text |  String    |  否     | 模糊查询。注：行业ID或行业名称的 istartwith 匹配。 |
| parent |  Int    |  否     | 精确查询。 大类查询可不传该参数，中类、小类 需要传上一级的ID。|

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| id | String | 关键词唯一性标识符 |
| text | String | 关键词名称 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/select2/industries?
&level=1
&text=农副
```

输出
```
[
    {
        "text": "农副食品加工业",
        "id": 13
    }
]
```


*****
### **2002**

**1. 接口描述**

本接口 (select2/areas) 用于查询地域。

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| text |  String    |  否     | 模糊查询。注：地域名称的 istartwith 匹配。 建议前端限制大于1个字符时才请求API，否则返回太多数据会导致前端加载缓慢。 |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| id | String | 关键词唯一性标识符 |
| text | String | 关键词名称 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/select2/areas?
&text=武
```

输出
```
[
    {
        "id": 89,
        "text": "武陟"
    },
    {
        "id": 178,
        "text": "武汉"
    },
    ...
]
```


*****
### **2003**

**1. 接口描述**

本接口 (select2/alias_industries) 用于查询行业别名。

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| text |  String    |  否     | 模糊查询。注：行业ID或行业名称的 istartwith 匹配。 |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| id | String | 关键词唯一性标识符 |
| text | String | 关键词名称 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/select2/alias_industries?
&text=电
```

输出
```
[
    {
        "text": "电线电缆",
        "id": 5
    },
]
```


*****
### **2004**

**1. 接口描述**

本接口 (select2/ccc_industries) 用于查询3C行业。

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| text |  String    |  否     | 模糊查询。注：行业ID或行业名称的 istartwith 匹配。 |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| id | String | 关键词唯一性标识符 |
| text | String | 关键词名称 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/select2/ccc_industries?
&text=电
```

输出
```
[
    {
        "text": "电线电缆",
        "id": 5
    },
]
```


*****
### **2005**

**1. 接口描述**

本接口 (select2/license_industries) 用于查询许可证行业。

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| text |  String    |  否     | 模糊查询。注：行业ID或行业名称的 istartwith 匹配。 |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| id | String | 关键词唯一性标识符 |
| text | String | 关键词名称 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/select2/license_industries?
&text=电
```

输出
```
[
    {
        "text": "电线电缆",
        "id": 5
    },
]
```


*****
### **3001**

**1. 接口描述**

本接口 (risk_data) 用于获取风险数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| starttime| Date        |  否     | 开始时间. |
| endtime| Date        |  否     | 结束时间 |
| title| String        |  否     | 标题。注：模糊匹配 |
| source| String        |  否     | 来源。注：模糊匹配 |
| areas | Int        |  否     | 地域ID列表。注：精确匹配(多选)；多个值之间用逗号分割。select2 |


**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| guid | String | GUID |
| url | String | 网址 |
| title | String | 标题 |
| source | String | 来源 |
| score | Int | 风险程度 |
| pubtime | String | 发布时间 |
| areas | List | 地域的列表 |
| categories | List | 类别的列表 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/risk_data
```

输出
```
{
    "total": 61,
    "list": [
        {
            "source": "中国新闻网",
            "title": "对儿童安全构成威胁 指尖陀螺被欧盟列为危险品",
            "pubtime": "2018-03-14 00:00:00",
            "url": "http://dw.chinanews.com/chinanews/content.jsp?id=8467281&classify=zw&pageSize=6&language=chs",
            "guid": "528eb39855e876852c1f6371a82ea634",
            "categories": [
                "特种设备",
                "认证监管",
                "质量管理"
            ],
            "score": 2,
            "areas": [
                "北京",
                "上海"
            ]
        },
        ...
    ]
}
```


*****
### **30011**

**1. 接口描述**

本接口 (risk_data/add) 用于新增风险数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| url | String | 是 | 网址.|
| title | String | 否 | 标题.|
| pubtime | String | 是 | 发布时间.|
| score | String | 否 | 风险程度.|
| source | String | 是 | 来源.|
| areas | String | 是 | 地区. 注：多个地域ID之间以逗号分割.|
| categories | String | 是 | 类别. 注：多个类别ID之间以逗号分割.|

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 202 | HTTP Status Code | 服务器已接受请求, 但尚未处理.（该信息已存在，判断依据：URL） |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
#### **30012**

**1. 接口描述**

本接口 (risk_data/edit/<int:id>/) 用于编辑风险数据. 

Tips: 
- <int:id>: 需要修改的风险数据ID

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| title | String | 否 | 标题.|
| pubtime | String | 是 | 发布时间.|
| score | String | 否 | 风险程度.|
| source | String | 是 | 来源.|
| areas | String | 是 | 地区. 注：多个地域ID之间以逗号分割.|
| categories | String | 是 | 类别. 注：多个类别ID之间以逗号分割.|

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```

*****
#### **30013**

**1. 接口描述**

本接口 (risk_data/delete/<int:id>/) 用于删除风险数据. 

Tips: 
- <int:id>: 需要删除的风险数据ID

**2. 输入参数**

无

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| 200 | HTTP Status Code | 请求已成功 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
#### **30014**

**1. 接口描述**

本接口 (risk_data/upload) 用于上传风险数据. 

Tips: 
- 文件格式：xlsx

**2. 输入参数**

无

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| 200 | HTTP Status Code | 请求已成功 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
### **3002**

**1. 接口描述**

本接口 (inspection_data) 用于获取抽检数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| starttime| Date        |  否     | 开始时间. |
| endtime| Date        |  否     | 结束时间 |
| title| String        |  否     | 标题。注：模糊匹配 |
| source| String        |  否     | 行政单位。 注：模糊匹配 |
| category| String        |  否     | 抽查类别。 注：模糊匹配 |
| level | Int        |  否     | 抽查级别。 值范围(国 省 市)。 注：精确匹配(单选)。select2 |
| area | Int        |  否     | 地域ID。注：精确匹配(单选)。select2 |


**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| category | String | 抽查类别 |
| qualitied | Double | 抽查合格率 |
| url | String | 网址 |
| industry | String | 产品类别 |
| pubtime | Date | 发布时间 |
| area | String | 抽查地区 |
| level | String | 抽查级别 |
| source | String | 行政单位 |


**4. 实例**

输入

```
http://192.168.0.103:8001/api/inspection_data
```

输出
```
{
    "total": 18,
    "list": [
        {
            "area": "浙江",
            "qualitied": "96.30%",
            "category": "监督抽查",
            "level": "省",
            "pubtime": "2018-03-26",
            "url": "http://www.zjbts.gov.cn/HTML/cctg/201803/2ec25119-699a-4b66-91dc-033cb1242383.html",
            "source": "浙江省质监局",
            "industry": "电线电缆"
        },
        ...
    ]
}
```


*****
### **30021**

**1. 接口描述**

本接口 (inspection_data/add) 用于新增抽检数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| title | String | 否 | 标题 |
| url | String | 是 | 链接 |
| pubtime | String | 是 | 发布时间 |
| source | String | 是 | 来源 |
| qualitied | Float | 是 | 合格率 |
| category | String | 否 | 类别 |
| level | String | 是 | 检验等级。 注：值范围(国 省 市) |
| unitem | String | 否 | 不合格项 |
| industry_id | Int | 是 | 行业别名ID。 注: 单选。对应select2 api -> select2/alias_industries |
| area_id | Int | 是 | 地域ID。 注：单选。 对应 select2 api -> select2/areas |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 202 | HTTP Status Code | 服务器已接受请求, 但尚未处理.（该信息已存在，判断依据：URL+行业别名ID） |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
#### **30022**

**1. 接口描述**

本接口 (inspection_data/edit/<int:id>/) 用于编辑抽检数据. 

Tips: 
- <int:id>: 需要修改的抽检数据ID

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| title | String | 否 | 标题 |
| url | String | 是 | 链接 |
| pubtime | String | 是 | 发布时间 |
| source | String | 是 | 来源 |
| qualitied | Float | 是 | 合格率 |
| category | String | 否 | 类别 |
| level | String | 是 | 检验等级。 注：值范围(国 省 市) |
| unitem | String | 否 | 不合格项 |
| industry_id | Int | 是 | 行业别名ID。 注: 单选。对应select2 api -> select2/alias_industries |
| area_id | Int | 是 | 地域ID。 注：单选。 对应 select2 api -> select2/areas |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```

*****
#### **30023**

**1. 接口描述**

本接口 (inspection_data/delete/<int:id>/) 用于删除抽检数据. 

Tips: 
- <int:id>: 需要删除的抽检数据ID

**2. 输入参数**

无

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| 200 | HTTP Status Code | 请求已成功 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
#### **30024**

**1. 接口描述**

本接口 (inspection_data/upload) 用于上传抽检数据. 

Tips: 
- 文件格式：xlsx

**2. 输入参数**

无

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| 200 | HTTP Status Code | 请求已成功 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
### **3003**

**1. 接口描述**

本接口 (alias_industry/add) 用于新增产品(行业别名).

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| name | String | 是 | 产品名称 |
| industry_id | Int | 是 | 行业ID。 注: 对应小类的行业ID。 |
| ccc_id | Int | 否 | 3C行业ID。 注: 用户若标识该产品为3C，则通过 select2/ccc_industries 选择一个产品，传递ID到后台。 若无需标识，则传递 空值 或 0 到后台即可。|
| license_id | Int | 否 | 许可证行业ID。 注: 用户若标识该产品为许可证，则通过 select2/license_industries 选择一个产品，传递ID到后台。 若无需标识，则传递 空值 或 0 到后台即可。|

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 202 | HTTP Status Code | 服务器已接受请求, 但尚未处理.（该信息已存在，判断依据：name+industry_id） |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
### **30031**

**1. 接口描述**

本接口 (ccc_industry/add) 用于新增3C行业.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| number | Int | 是 | 行业编号。 |
| name | Int | 是 | 行业名称。 |
| desc | String | 否 | 描述。 |
| level | Int | 否 | 行业等级。 注：如不填写，则默认为 1。|
| parent | Int | 否 | 上一级行业编号。 注：若不填写，则默认为空。 |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 202 | HTTP Status Code | 服务器已接受请求, 但尚未处理.（该信息已存在，判断依据：number） |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
### **30032**

**1. 接口描述**

本接口 (license_industry/add) 用于新增许可证行业.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| number | Int | 是 | 行业编号。 |
| name | Int | 是 | 行业名称。 |
| desc | String | 否 | 描述。 |
| level | Int | 否 | 行业等级。 注：如不填写，则默认为 1。|
| parent | Int | 否 | 上一级行业编号。 注：若不填写，则默认为空。 |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 202 | HTTP Status Code | 服务器已接受请求, 但尚未处理.（该信息已存在，判断依据：number） |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
### **3004**

**1. 接口描述**

本接口 (corpus) 用于获取语料词数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| page | Int        |  是     | 页码. 值范围(1~+&). 默认值: 1|
| length | Int        |  是     | 页长度. 值范围(15~+&). 默认值: 15|
| industry_id | Int        |  否     | 产品ID。 对应select2：select2/alias_industries。|


**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| total| Int | 符合条件的信息数量。 |
| list | List | 符合条件的详细信息列表。 |
| riskword | String | 风险词 |
| invalidword | String | 无效词 |
| industry_id | String | 行业ID |
| industry_name | String | 行业名称 |

**4. 实例**

输入

```
http://192.168.0.103:8001/api/corpus
```

输出
```
{
    "total": 18,
    "list": [
         {
            "invalidword": "绿帽 戴帽 如何 贫困 笔 穷 高帽 摘",
            "riskword": "风险 劣质 假冒 PH值 褪色 抽查 违规 致癌 防腐剂 产品质量 召回 不安全 纤维含量 造假 质监 污染 甲醛含量 不合格 投诉 抽检 三无 超标 不达标 伤害 整改 预警 异物 色素 异味 隐患",
            "industry_name": "电线电缆",
            "industry_id": 5
        },
        ...
    ]
}
```


*****
### **30041**

**1. 接口描述**

本接口 (corpus/add) 用于新增语料词数据.

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| riskword | String | 否 | 风险词。 |
| invalidword | String | 否 | 无效词。 |
| industry_id | Int | 是 | 行业别名ID。 注: 单选。对应select2 api -> select2/alias_industries |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 202 | HTTP Status Code | 服务器已接受请求, 但尚未处理.（该信息已存在，判断依据：industry_id） |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```


*****
#### **30042**

**1. 接口描述**

本接口 (corpus/edit/<int:id>/) 用于编辑语料词数据. 

Tips: 
- <int:id>: 需要修改的语料词数据ID

**2. 输入参数**

| 参数名称 |    类型   | 是否必选 |  描述       |
| :------| :-------- | :------ |:----------|
| riskword | String | 否 | 风险词。 |
| invalidword | String | 否 | 无效词。 |
| industry_id | Int | 是 | 行业别名ID。 注: 单选。对应select2 api -> select2/alias_industries |

**3. 输出参数**

| 参数名称 |    类型   |     描述   |
| :------| :-------- | :-------- |
| 200 | HTTP Status Code | 请求已成功 |
| 400 | HTTP Status Code | 非空字段为空 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```

*****
#### **30043**

**1. 接口描述**

本接口 (corpus/delete/<int:id>/) 用于删除语料词数据. 

Tips: 
- <int:id>: 需要删除的语料词数据ID

**2. 输入参数**

无

**3. 输出参数**

| 参数名称 |    类型   |     描述   | 
| :------| :-------- | :-------- | 
| 200 | HTTP Status Code | 请求已成功 |
| 500 | HTTP Status Code | 服务器异常 |

**4. 实例**

输入

```
略
```

输出
```
略
```
