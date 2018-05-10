from django.urls import path, re_path
from rest_framework_jwt import views

from observer.base.views import (
                                IndustryView, CCCIndustryView, LicenseIndustryView, 
                                Select2IndustryView, ArticleView, Select2AreaView,
                                InspectionView, DMLinkView, DMLinkAddView, 
                                DMLinkEditView, DMLinkDeleteView, DMWordsView, 
                                RiskDataView, RiskDataAddView, RiskDataEditView, 
                                RiskDataDeleteView, RiskDataUploadView, InspectionDataView, 
                                InspectionDataAddView, InspectionDataEditView, 
                                InspectionDataDeleteView, InspectionDataUploadView, 
                                Select2AliasIndustryView, AliasIndustryAddView,
                                CorpusView, CorpusAddView, CorpusEditView, 
                                CorpusDeleteView, Select2CCCIndustryView, 
                                Select2LicenseIndustryView, CCCIndustryAddView,
                                LicenseIndustryAddView, RiskDataExportView, 
                                InspectionDataExportView, DashboardView, SearchView,
                                )


urlpatterns = [
    path('dashboard', DashboardView.as_view()),  # 整体概览
    path('industries', IndustryView.as_view()),  # 行业列表
    path('articles/<str:category>/', ArticleView.as_view()),  # 文章列表
    path('inspections', InspectionView.as_view()),  # 抽检列表
    path('ccc/<int:cid>/', CCCIndustryView.as_view()),  # 3C行业
    path('license/<int:lid>/', LicenseIndustryView.as_view()),  # License行业

    path('dmlinks', DMLinkView.as_view()),  # 指定监测-链接 列表
    path('dmlink/add', DMLinkAddView.as_view()),  # 添加指定监测-链接
    path('dmlink/edit/<int:did>/', DMLinkEditView.as_view()),  # 修改指定监测-链接
    path('dmlink/delete/<int:did>/', DMLinkDeleteView.as_view()),  # 删除指定监测-链接
    path('dmwords', DMWordsView.as_view()),  # 指定监测-关键词 列表

    # ADMIN 
    path('risk_data', RiskDataView.as_view()),  # 风险数据
    path('risk_data/add', RiskDataAddView.as_view()),  # 风险数据添加
    path('risk_data/edit/<str:aid>/', RiskDataEditView.as_view()),  # 风险数据修改
    path('risk_data/delete/<str:aid>/', RiskDataDeleteView.as_view()),  # 风险数据删除
    path('risk_data/upload/<str:filename>/', RiskDataUploadView.as_view()),  # 风险数据上传
    path('risk_data/export', RiskDataExportView.as_view()),  # 风险数据导出
    path('inspection_data', InspectionDataView.as_view()),  # 抽检数据
    path('inspection_data/add', InspectionDataAddView.as_view()),  # 抽检数据添加
    path('inspection_data/edit/<str:aid>/', InspectionDataEditView.as_view()),  # 抽检数据修改
    path('inspection_data/delete/<str:aid>/', InspectionDataDeleteView.as_view()),  # 抽检数据删除
    path('inspection_data/upload/<str:filename>/', InspectionDataUploadView.as_view()),  # 抽检数据上传
    path('inspection_data/export', InspectionDataExportView.as_view()),  # 抽检数据导出
    path('alias_industry/add', AliasIndustryAddView.as_view()),  # 行业别名添加
    path('ccc_industry/add', CCCIndustryAddView.as_view()),  # CCC行业添加
    path('license_industry/add', LicenseIndustryAddView.as_view()),  # 许可证行业添加
    path('corpus', CorpusView.as_view()),  # 语料词列表
    path('corpus/add', CorpusAddView.as_view()),  # 语料词添加
    path('corpus/edit/<int:cid>/', CorpusEditView.as_view()),  # 语料词编辑
    path('corpus/delete/<int:cid>/', CorpusDeleteView.as_view()),  # 语料词删除

    path('select2/industries', Select2IndustryView.as_view()),  # 行业名称
    path('select2/alias_industries', Select2AliasIndustryView.as_view()),  # 行业别名
    path('select2/ccc_industries', Select2CCCIndustryView.as_view()),  # 3C行业
    path('select2/license_industries', Select2LicenseIndustryView.as_view()),  # License行业
    path('select2/areas', Select2AreaView.as_view()),  # 地域名称

    path('search', SearchView.as_view()),  # 搜索
]

urlpatterns += [
    re_path(r'^token-auth$', views.obtain_jwt_token),
    re_path(r'^token-verify$', views.verify_jwt_token),
    re_path(r'^token-refresh$', views.refresh_jwt_token),
]
