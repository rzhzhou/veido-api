from django.urls import path, re_path
from observer.apps.dyy import views


urlpatterns = [
	path('videosource/<int:vid>/', views.VideoSourceView.as_view()), 
]
