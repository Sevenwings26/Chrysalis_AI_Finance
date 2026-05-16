from django.urls import path
from .views import (
    index,
    # about,
    register_view, 
    login_view, 
    logout_view,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)

urlpatterns = [
    path('', index, name='index'),
    # path('about/', about, name='about'),
    path('account/register/', register_view, name='register'),
    path('account/login/', login_view, name='login'),
    path('account/logout/', logout_view, name='logout'),
    
    # Password Reset URLs
    path('account/password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('account/password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/password-reset/confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/password-reset/complete/', 
         CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
