from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from decimal import Decimal
from ..models import Wallet, Portfolio, PortfolioHolding


@login_required
def portfolio_view(request):
    """Portfolio Dashboard View"""
    
    # Get user's wallet
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)

    # Get user's main portfolio
    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user, 
        name="Main Portfolio"
    )

    # Get holdings
    holdings = PortfolioHolding.objects.filter(portfolio=portfolio).select_related()

    # Calculate values
    total_equities_value = Decimal('0')
    holdings_data = []

    for holding in holdings:
        current_price = holding.current_price if hasattr(holding, 'current_price') else None
        if not current_price:
            # Fallback: try to get live price
            current_price = Decimal('0')  # You can enhance this with NGXStockProvider

        invested = holding.quantity * holding.average_buy_price
        current_value = holding.quantity * (current_price or holding.average_buy_price)

        total_equities_value += current_value

        pnl = current_value - invested
        pnl_percent = (pnl / invested * 100) if invested > 0 else 0

        holdings_data.append({
            'symbol': holding.symbol,
            'quantity': holding.quantity,
            'avg_buy_price': holding.average_buy_price,
            'current_price': current_price,
            'current_value': current_value,
            'pnl': pnl,
            'pnl_percent': pnl_percent,
        })

    total_portfolio_value = wallet.balance + total_equities_value
    cash_percentage = (wallet.balance / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
    equities_percentage = 100 - cash_percentage

    context = {
        'wallet': wallet,
        'portfolio': portfolio,
        'total_portfolio_value': total_portfolio_value,
        'total_equities_value': total_equities_value,
        'cash_percentage': round(cash_percentage, 2),
        'equities_percentage': round(equities_percentage, 2),
        'holdings': holdings_data,
        'total_holdings': len(holdings_data),
    }

    return render(
        request,
        "market/paperT-portfolio.html",
    )


@login_required
def history(request):

    return render(
        request,
        "market/paperT-history.html",
    )


