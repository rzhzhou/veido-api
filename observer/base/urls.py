from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from observer.base import views


urlpatterns = [
    path('dashboard', views.DashboardView.as_view()),  # 整体概览
    path('industries', views.IndustryView.as_view()),  # 行业列表
    path('articles/<str:category>/', views.ArticleView.as_view()),  # 文章列表
    path('inspections', views.InspectionView.as_view()),  # 抽检列表
    path('ccc', views.CCCListView.as_view()),  # 3C行业
    path('ccc/<int:cid>/', views.CCCIndustryView.as_view()),  # 3C行业
    path('cpc', views.CpcListView.as_view()),  # 产品总分类
    path('licence', views.LicenceListView.as_view()),  # Licence行业
    path('licence/<int:lid>/', views.LicenceIndustryView.as_view()),  # Licence行业
    path('consumer', views.ConsumerListView.as_view()),  # 消费品目录
    path('major', views.MajorListView.as_view()),  # 重点产品目录
    path('major/<int:pk>', views.MajorView.as_view()),  # 重点产品

    path('dmlinks', views.DMLinkView.as_view()),  # 指定监测-链接 列表
    path('dmlink/add', views.DMLinkAddView.as_view()),  # 添加指定监测-链接
    path('dmlink/edit/<int:did>/', views.DMLinkEditView.as_view()),  # 修改指定监测-链接
    path('dmlink/delete/<int:did>/', views.DMLinkDeleteView.as_view()),  # 删除指定监测-链接
    path('dmwords', views.DMWordsView.as_view()),  # 指定监测-关键词 列表

    # ADMIN
    path('risk_data', views.RiskDataView.as_view()),  # 风险数据
    path('risk_data/add', views.RiskDataAddView.as_view()),  # 风险数据添加
    path('risk_data/audit/<str:aid>/', views.RiskDataAuditView.as_view()), # 风险数据审核
    path('risk_data/edit/<str:aid>/', views.RiskDataEditView.as_view()),  # 风险数据修改
    path('risk_data/delete/<str:aid>/', views.RiskDataDeleteView.as_view()),  # 风险数据删除
    path('risk_data/upload/<str:filename>/', views.RiskDataUploadView.as_view()),  # 风险数据上传
    path('risk_data/export', views.RiskDataExportView.as_view()),  # 风险数据导出
    path('risk_data/news_crawler/',views.newsCrawlerView.as_view()), # 电梯风险新闻爬取
    path('inspection_data', views.InspectionDataView.as_view()),  # 抽检数据
    path('enterprise_data', views.EnterpriseDataListView.as_view()), # 不合格企业列表
    path('enterprise_data/edit/<int:cid>/', views.EnterpriseDataEditView.as_view()), # 不合格企业修改
    path('enterprise_data/delete/<str:cid>/', views.EnterpriseDataDeleteView.as_view()), # 不合格企业删除
    path('enterprise_data/audit/<str:cid>/', views.EnterpriseDataAuditView.as_view()), # 不合格企业审核
    path('enterprise_data/<str:eid>/', views.EnterpriseDataView.as_view()), # 不合格企业
    path('inspection_data/add', views.InspectionDataAddView.as_view()),  # 抽检数据添加
    path('inspection_data/edit/<int:cid>/', views.InspectionDataEditView.as_view()),  # 抽检数据修改
    path('inspection_data/delete/<str:cid>/', views.InspectionDataDeleteView.as_view()),  # 抽检数据删除
    path('inspection_data/upload/<str:filename>/', views.InspectionDataUploadView.as_view()),  # 抽检数据上传
    path('inspection_data/un_enterprise/upload/<str:filename>/', views.InspectionDataUnEnterpriseUploadView.as_view()),  # 抽检数据不合格企业上传
    path('inspection_data/export', views.InspectionDataExportView.as_view()),  # 抽检数据导出
    path('inspection_data/crawler/<str:cid>/', views.InspectionDataCrawlerView.as_view()),  # 抽检数据爬取不合格企业
    path('inspection_data/audit/<str:cid>/', views.InspectionDataAuditView.as_view()), # 抽检数据审核
    path('alias_industry/add', views.AliasIndustryAddView.as_view()),  # 行业别名添加
    path('ccc_industry/add', views.CCCIndustryAddView.as_view()),  # CCC行业添加
    path('licence_industry/add', views.LicenceIndustryAddView.as_view()),  # 许可证行业添加
    path('corpus', views.CorpusView.as_view()),  # 语料词列表
    path('corpus/add', views.CorpusAddView.as_view()),  # 语料词添加
    path('corpus/edit/<int:cid>/', views.CorpusEditView.as_view()),  # 语料词编辑
    path('corpus/delete/<str:cid>/', views.CorpusDeleteView.as_view()),  # 语料词删除
    path('users', views.UserView.as_view()), # 用户管理
    path('users/add', views.UserAddView.as_view()), # 用户添加
    path('users/edit/<int:cid>/', views.UserEditView.as_view()), # 用户修改
    path('users/delete/<str:cid>/', views.UserDeleteView.as_view()), # 用户删除

    path('select2/industries', views.Select2IndustryView.as_view()),  # 行业名称
    path('select2/alias_industries', views.Select2AliasIndustryView.as_view()),  # 行业别名
    path('select2/ccc_industries', views.Select2CCCListView.as_view()),  # 3C行业
    path('select/cpc_industries', views.SelectCpcisView.as_view()),
    path('select2/licence_industries', views.Select2LicenceListView.as_view()),  # Licence行业
    path('select2/consumer_industries', views.Select2ConsumerListView.as_view()),  # 消费品目录
    path('select2/major_industries', views.Select2MajorListView.as_view()),  # 重点产品目录
    path('select2/areas', views.Select2AreaView.as_view()),  # 地域名称
    path('select2/industry_products', views.Select2IndustryProductsView.as_view()),  # 行业产品

    path('search', views.SearchView.as_view()),  # 搜索
    path('search/advanced', views.SearchAdvancedView.as_view()),  # 高级搜索

    path('crawler/<str:cid>/', views.CrawlerView.as_view()), #语料词爬取数据

    # SUZHOU
    path('risk_data_suzhou', views.RiskDataViewSuzhou.as_view()), # 新闻信息
    path('inspection_suzhou', views.InspectionDataViewSuzhou.as_view()), # 抽检信息

    # 侧边栏
    path('nav_bar', views.NavBarView.as_view()), # 侧边栏导航
    path('nav_bar/edit/<str:cid>/', views.NavBarEditView.as_view()), # 分配侧边栏导航

    # 官网
    path('news', views.NewsView.as_view()), # 公司动态
    path('news/add', views.NewsAddView.as_view()), # 发布一则公司动态
    path('news/delete/<str:cid>/', views.NewsDeleteView.as_view()), # 删除公司动态
    path('news/edit/<int:cid>/', views.NewsEditView.as_view()), # 修改公司动态
]

# urlpatterns += [
#     re_path(r'^token-auth$', obtain_jwt_token),
#     re_path(r'^token-verify$', verify_jwt_token),
# ]
