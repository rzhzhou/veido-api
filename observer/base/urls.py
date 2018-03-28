from django.urls import path, re_path
from rest_framework_jwt import views

from observer.base.views import (
								IndustryView, CCCIndustryView, LicenseIndustryView, 
								Select2IndustryView, ArticleView, 
								)


urlpatterns = [
    path('industries', IndustryView.as_view()),  # 行业列表
    path('articles/<str:category>/', ArticleView.as_view()),  # 质监热点列表
    path('ccc/<int:cid>/', CCCIndustryView.as_view()),  # 3C行业
    path('license/<int:lid>/', LicenseIndustryView.as_view()),  # License行业
    path('select2/industries', Select2IndustryView.as_view()),  # 行业名称
]

urlpatterns += [
    re_path(r'^token-auth$', views.obtain_jwt_token),
    re_path(r'^token-verify$', views.verify_jwt_token),
    re_path(r'^token-refresh$', views.refresh_jwt_token),
]
