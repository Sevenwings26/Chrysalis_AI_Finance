from django.urls import path
from .views import (
    register_view, 
    login_view, 
    logout_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Password Reset URLs
    path('login/password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('login/password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('login/password-reset/confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/password-reset/complete/', 
         CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
