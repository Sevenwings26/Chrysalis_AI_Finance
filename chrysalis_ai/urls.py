

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('main.urls')),
    path('', include('users.urls')),
    path('market/', include('market.urls')),
    path('ai/', include('ai_tool.urls')),
    path('learn/', include('learn.urls')),
]

