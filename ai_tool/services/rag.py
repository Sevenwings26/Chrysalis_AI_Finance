import json
from django.core.cache import cache
from market.services.ngxpulse import NGXStockProvider


class Retriever:
    """
    RAG Retriever for Chrysalis AI
    """

    def __init__(self):
        self.stock_provider = NGXStockProvider()
        self.cache_key = "financial_knowledge_base"

    def search(self, query: str, top_k: int = 5):
        """
        Main search method
        """
        results = []

        # 1. Live Market Context
        market_context = self._get_market_context(query)
        if market_context:
            results.append({
                "type": "market_data",
                "content": market_context
            })

        # 2. Knowledge Base
        knowledge = self._get_knowledge_base(query, top_k=top_k)
        results.extend(knowledge)

        return results

    def _get_market_context(self, query: str):
        """Get relevant live stock data"""
        try:
            stocks = self.stock_provider.get_all_stocks()

            query_lower = query.lower()
            relevant = []

            common_symbols = ["UBA", "ACCESSCORP", "DANGCEM", "BUAFOODS", "DANGSUGAR", 
                            "ZENITHBANK", "GTCO", "MTNN", "AIRTELAFRI", "SEPLAT"]

            for symbol in common_symbols:
                if symbol in query_lower:
                    stock = next((s for s in stocks if s.get("symbol", "").upper() == symbol), None)
                    if stock:
                        relevant.append(stock)

            if not relevant:
                # Return top movers
                sorted_stocks = sorted(stocks, key=lambda x: abs(x.get("change_percent", 0)), reverse=True)
                relevant = sorted_stocks[:8]

            return {
                "relevant_stocks": relevant,
                "note": "Live market data from NGX Pulse"
            }

        except Exception as e:
            print("Market Context Error:", e)
            return None

    def _get_knowledge_base(self, query: str, top_k: int = 5):
        """Static knowledge base with relevance scoring"""
        knowledge = cache.get(self.cache_key)

        if not knowledge:
            knowledge = self._build_knowledge_base()
            cache.set(self.cache_key, knowledge, timeout=3600)

        query_lower = query.lower()
        scored = []

        for item in knowledge:
            score = 0
            content_lower = item.get('content', '').lower()
            title_lower = item.get('title', '').lower()

            # Simple keyword matching
            words = query_lower.split()
            for word in words:
                if word in content_lower or word in title_lower:
                    score += 5

            if "pe ratio" in content_lower and "pe" in query_lower:
                score += 15
            if any(x in query_lower for x in ["buy", "sell", "recommend"]) and "recommend" in content_lower:
                score += 10

            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        
        # FIXED: Use the passed top_k parameter
        return [item for score, item in scored[:top_k]] if scored else knowledge[:top_k]

    def _build_knowledge_base(self):
        return [
            {"type": "knowledge", "title": "PE Ratio", "content": "Price-to-Earnings Ratio shows how much investors pay for every ₦1 of earnings. Lower PE often suggests better value, but compare within the same sector."},
            {"type": "knowledge", "title": "Upside Potential", "content": "Estimated percentage increase in stock price based on valuation models."},
            {"type": "knowledge", "title": "NGX Trading", "content": "The Nigerian Exchange operates Monday to Friday. Major sectors include Banking, Oil & Gas, Industrials, and Consumer Goods."},
            {"type": "knowledge", "title": "Investment Signals", "content": "STRONG BUY = Strong momentum + attractive valuation. HOLD = Neutral. SELL = Weak outlook or overvalued."},
        ]
    
