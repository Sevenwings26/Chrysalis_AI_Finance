from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..services.ngxpulse import NGXStockProvider


# @login_required
# def stock_list(request):

#     provider = NGXStockProvider()

#     stocks = provider.get_all_stocks()

#     stocks = sorted(
#         stocks,
#         key=lambda stock: stock.get("change_percent", 0),
#         reverse=True
#     )

#     context = {
#         "stocks": stocks[:30],
#         "api_failed": len(stocks) == 0
#     }

#     return render(
#         request,
#         "market/paperT-invest.html",
#         context
#     )


@login_required
def stock_list(request):
    provider = NGXStockProvider()
    query = request.GET.get("q", "").strip()

    stocks = provider.search_stocks(query) if query else provider.get_all_stocks()

    stocks = sorted(
        stocks,
        key=lambda stock: stock.get("change_percent", 0),
        reverse=True
    )

    context = {
        "stocks": stocks[:30],
        "api_failed": len(stocks) == 0,
        "search_query": query,       # so the input stays filled
        "total_count": len(stocks),  # for the "See all N Equities" button
    }

    return render(request, "market/paperT-invest.html", context)


# def buy stock 