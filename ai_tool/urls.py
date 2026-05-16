from django.urls import path
from .views import (
    chat_page, 
    chat_api, 
    chat_history_api,
    chat_thread_detail,
    delete_chat_thread,
)

urlpatterns = [
    
    # Chat Routes
    path('chat/', chat_page, name='chat_page'),
    path('chat/api/', chat_api, name='chat_api'),
    path('chat/history/', chat_history_api, name='chat_history_api'),
    path('chat/thread/<int:thread_id>/', chat_thread_detail, name='chat_thread_detail'),
    path('chat/thread/<int:thread_id>/delete/', delete_chat_thread, name='delete_chat_thread'),
]

