from django.conf.urls import url

from observer.apps.yqj.views import (NewsView, EventView,ReferenceView,InsightView,RiskView,
	                                 InspectionView,CategoryView,HomeView)


urlpatterns = [
    url(r'^article$', NewsView.as_view()),#质监热点
    url(r'^event$', EventView.as_view()),#质量事件
    url(r'^reference$', ReferenceView.as_view()),#信息参考
    url(r'^insight$', ReferenceView.as_view()),#专家视点
    url(r'^risk$', RiskView.as_view()),#风险快讯
    url(r'^inspection$', InspectionView.as_view()),#抽检信息
    url(r'^category/(?P<id>\d+)$', CategoryView.as_view()),#业务信息
    url(r'^area/(?P<id>\d+)$', CategoryView.as_view()),#区域状况
    url(r'^$', HomeView.as_view()),#主页
]
