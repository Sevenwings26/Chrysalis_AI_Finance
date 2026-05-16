import re
from django.core.cache import cache
from market.services.ngxpulse import NGXStockProvider   # ← Your existing provider


class MarketTool:

    def __init__(self):
        self.provider = NGXStockProvider()

    def get_all_stocks(self, force_refresh=False):
        return self.provider.get_all_stocks(force_refresh=force_refresh)

    def get_stock(self, symbol: str):
        """Get single stock - very useful for chatbot"""
        if not symbol:
            return None
            
        stocks = self.get_all_stocks()
        symbol = symbol.upper()
        
        for stock in stocks:
            if stock.get("symbol", "").upper() == symbol:
                return stock
        return None

    def extract_symbol(self, query: str) -> str | None:
        """Simple symbol extractor"""
        query = query.upper()
        # Common Nigerian stocks
        common_symbols = ["UBA", "ACCESSCORP", "DANGCEM", "BUAFOODS", "DANGSUGAR", 
                         "ZENITHBANK", "GTCO", "SEPLAT", "MTNN", "AIRTELAFRI"]
        
        for symbol in common_symbols:
            if symbol in query:
                return symbol
        return None

    def _signal(self, change_percent):
        if change_percent >= 5:
            return "STRONG BUY"
        elif change_percent > 1.5:
            return "BUY"
        elif change_percent <= -5:
            return "STRONG SELL"
        elif change_percent < -1.5:
            return "SELL"
        return "HOLD"
    
