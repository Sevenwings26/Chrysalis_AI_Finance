from django.urls import path
from .views import (
    dashboard,
    deposit_view,
    stock_list,
    portfolio_view,
    history,
    # chrysalis,
)
from .views.ai_views import chrysalis

urlpatterns = [
    path('paper-wallet/', dashboard, name='paper-wallet'),
     path('deposit/', deposit_view, name='deposit'),
     path('stocks/', stock_list, name='stock-list'),
     path('portfolio/', portfolio_view, name='portfolio'),
     path('history/', history, name='history'),

    #  ai endpoint
    # path('aichat/', chrysalis, name="chrysalis"),
]

# Rate Limit 
