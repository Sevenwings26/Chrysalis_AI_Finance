from django.urls import path
from . import views

# app_name = 'learning'

urlpatterns = [
    path('main/', views.learning_home, name='learning_home'),
    path('video/<slug:slug>/', views.video_detail, name='video_detail'),
    path('video/<int:video_id>/watch/', views.mark_video_watched, name='mark_watched'),
]

