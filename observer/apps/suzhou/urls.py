from django.urls import path

from observer.apps.suzhou.views import (RiskProductView, RiskEnterprisesView, RiskNewsView,
                                     RiskInspectionView, WholeRiskView, InternetRiskView,)


urlpatterns = [
    path('product', RiskProductView.as_view()),  # 风险产品
    path('enterprises', RiskEnterprisesView.as_view()),  # 风险企业
    path('news', RiskNewsView.as_view()),  # 风险新闻
    path('inspection', RiskInspectionView.as_view()),  # 风险抽检
    path('insight', WholeRiskView.as_view()),  # 整体风险变化趋势
    path('risk', InternetRiskView.as_view()),  # 互联网风险数据变化趋势
]
