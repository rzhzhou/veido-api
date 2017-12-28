from django.urls import path

from observer.apps.yqj.views import (NewsView, EventView, ReferenceView,
                                     InsightView, RiskView, InspectionView,
                                     CategoryView, DashboardView,ArticleByIdView)


urlpatterns = [
    path('dashboard', DashboardView.as_view()),  # 主页
    path('article/<str:guid>', ArticleByIdView.as_view()),  # 质监热点
    path('article', NewsView.as_view()),  # 质监热点
    path('event', EventView.as_view()),  # 质量事件
    path('reference', ReferenceView.as_view()),  # 信息参考
    path('insight', ReferenceView.as_view()),  # 专家视点
    path('risk', RiskView.as_view()),  # 风险快讯
    path('inspection', InspectionView.as_view()),  # 抽检信息
    path('category/<str:name>', CategoryView.as_view()),  # 业务信息
    path('area/<int:id>', CategoryView.as_view()),  # 区域状况
]
