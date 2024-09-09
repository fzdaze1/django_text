from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_view, name='video_view'),
    path('download_video/<str:video_title>/',
         views.download_video_view, name='download_video'),
]
