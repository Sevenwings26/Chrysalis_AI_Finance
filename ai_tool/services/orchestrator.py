from dataclasses import dataclass
from typing import Dict
import json

from .market_tool import MarketTool
from .wallet_tool import WalletTool
from .rag import Retriever
from .llm import LLMClient


@dataclass
class AIContext:
    user: object
    query: str
    intent: str = None
    stock_symbol: str = None
    tools_data: Dict = None
    rag_context: list = None

    def __post_init__(self):
        if self.tools_data is None:
            self.tools_data = {}
        if self.rag_context is None:
            self.rag_context = []


class Orchestrator:

    def __init__(self):
        self.market_tool = MarketTool()
        self.wallet_tool = WalletTool()
        self.retriever = Retriever()
        self.llm = LLMClient()

    def process(self, user, query: str):
        context = AIContext(user=user, query=query)

        # Step 1: Classify Intent
        context.intent = self._classify_intent(query)

        # Step 2: Route Tools
        context = self._route_tools(context)

        # Step 3: Retrieve RAG Context
        context.rag_context = self._retrieve_context(query, context.stock_symbol)

        # Step 4: Build Prompt
        prompt = self._build_prompt(context)

        # Step 5: Generate Response
        response = self.llm.generate(prompt)

        return self._format_response(response, context)

    def _classify_intent(self, query: str) -> str:
        q = query.lower()
        
        if any(word in q for word in ["price", "quote", "trading", "cost", "how much", "current price"]):
            return "MARKET_QUERY"
        
        if any(word in q for word in ["buy", "sell", "recommend", "should i", "worth", "good stock", "investment", "outlook"]):
            return "FINANCIAL_ADVICE"
        
        if any(word in q for word in ["wallet", "balance", "portfolio", "holding", "my position", "what i own"]):
            return "WALLET_QUERY"
        
        return "GENERAL_QUERY"

    def _route_tools(self, context: AIContext) -> AIContext:
        # Extract stock symbol if mentioned
        symbol = self.market_tool.extract_symbol(context.query)
        context.stock_symbol = symbol

        if context.intent in ["MARKET_QUERY", "FINANCIAL_ADVICE"]:
            if symbol:
                context.tools_data["market"] = self.market_tool.get_stock(symbol)
            else:
                # Return top movers / active stocks
                context.tools_data["market"] = self.market_tool.get_all_stocks()[:10]

        if context.intent == "WALLET_QUERY":
            context.tools_data["wallet"] = self.wallet_tool.get_wallet(context.user)

        return context

    def _retrieve_context(self, query: str, stock_symbol=None):
        """Get relevant knowledge from RAG"""
        return self.retriever.search(query, top_k=5)

    def _build_prompt(self, context: AIContext) -> str:
        system_prompt = """
You are Chrysalis AI, a helpful, honest, and easy-to-understand financial intelligence assistant for the Nigerian Stock Market (NGX).

Core Rules:
- Always ground your answers in the provided market data and knowledge.
- Use simple, clear language suitable for retail investors in Nigeria.
- Be transparent about uncertainty.
- Always add this disclaimer when giving opinions: "This is not financial advice."
- Never guarantee profits or future performance.
"""

        market_data = context.tools_data.get("market")
        wallet_data = context.tools_data.get("wallet")
        rag_context = context.rag_context or []

        # Format data nicely for LLM
        market_str = json.dumps(market_data, indent=2, default=str) if market_data else "No specific market data available."
        wallet_str = json.dumps(wallet_data, indent=2, default=str) if wallet_data else "No wallet/portfolio data available."

        rag_str = "\n".join([
            f"- {item.get('title', 'Info')}: {item.get('content', '')}" 
            for item in rag_context
        ])

        return f"""{system_prompt}

CURRENT USER QUERY: {context.query}
DETECTED INTENT: {context.intent}
MENTIONED STOCK: {context.stock_symbol or 'None'}

=== LIVE MARKET DATA ===
{market_str}

=== USER WALLET & PORTFOLIO ===
{wallet_str}

=== RELEVANT KNOWLEDGE ===
{rag_str}

Answer the user's question naturally, helpfully, and accurately:
"""

    def _format_response(self, llm_response: str, context: AIContext):
        return {
            "message": llm_response,
            "intent": context.intent,
            "stock_symbol": context.stock_symbol,
            "type": "ai_response"
        }
    

