# chrysalis/ai/tools/wallet_tool.py
from market.models import Wallet, Portfolio, PortfolioHolding


class WalletTool:

    def get_wallet(self, user):
        try:
            wallet = Wallet.objects.get(user=user)

            # Get main portfolio
            portfolio = Portfolio.objects.filter(user=user).first()
            if not portfolio:
                portfolio = Portfolio.objects.create(user=user)

            holdings = PortfolioHolding.objects.filter(portfolio=portfolio)

            holdings_data = []
            total_equity_value = Decimal('0')

            for holding in holdings:
                current_price = self._get_current_price(holding.symbol)
                
                invested = holding.quantity * holding.average_buy_price
                current_value = holding.quantity * (current_price or holding.average_buy_price)

                total_equity_value += current_value

                holdings_data.append({
                    "symbol": holding.symbol,
                    "quantity": float(holding.quantity),
                    "avg_buy_price": float(holding.average_buy_price),
                    "current_price": float(current_price) if current_price else None,
                    "invested": float(invested),
                    "current_value": float(current_value),
                    "pnl_percent": float(((current_value - invested) / invested * 100)) if invested > 0 else 0
                })

            total_portfolio_value = wallet.balance + total_equity_value

            return {
                "cash_balance": float(wallet.balance),
                "total_portfolio_value": float(total_portfolio_value),
                "total_equities_value": float(total_equity_value),
                "equities_percentage": float((total_equity_value / total_portfolio_value * 100)) if total_portfolio_value > 0 else 0,
                "cash_percentage": float((wallet.balance / total_portfolio_value * 100)) if total_portfolio_value > 0 else 0,
                "holdings": holdings_data,
                "total_holdings": len(holdings_data)
            }

        except Wallet.DoesNotExist:
            return {"cash_balance": 0.0, "holdings": [], "total_portfolio_value": 0.0}
        except Exception as e:
            print(f"WalletTool Error: {e}")
            return {"error": str(e), "cash_balance": 0.0, "holdings": []}

    def _get_current_price(self, symbol):
        try:
            from market.services.ngxpulse import NGXStockProvider
            provider = NGXStockProvider()
            stocks = provider.get_all_stocks()
            
            for stock in stocks:
                if stock.get("symbol", "").upper() == symbol.upper():
                    return stock.get("price") or stock.get("current_price")
            return None
        except:
            return None
        