from django.urls import path
from .views import (
    dashboard,
    deposit_view,
    stock_list,
    portfolio_view,
    history,
    withdraw_view,
    buy_stock,
    sell_stock,
    # chrysalis,
)


urlpatterns = [
    path('paper-wallet/', dashboard, name='paper-wallet'),
     path('wallet/deposit/', deposit_view, name='deposit'),
     path("wallet/withdraw/",withdraw_view, name="withdraw",),
     path('stocks/', stock_list, name='stock-list'),
     path('portfolio/', portfolio_view, name='portfolio'),
     path('history/', history, name='history'),

     path("trade/buy/",  buy_stock,  name="buy_stock"),
    path("trade/sell/", sell_stock, name="sell_stock"),

    #  ai endpoint
    # path('aichat/', chrysalis, name="chrysalis"),
]

# Rate Limit 
