# market/services/ngxpulse.py 
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings
from django.core.cache import cache


class NGXStockProvider:

    BASE_URL = "https://www.ngxpulse.ng/api/ngxdata/stocks"

    CACHE_KEY = "ngx_market_stocks"

    CACHE_TIMEOUT = 60

    def __init__(self):

        self.session = requests.Session()

        retries = Retry(
            total=5,
            connect=5,
            read=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            raise_on_status=False
        )

        adapter = HTTPAdapter(
            max_retries=retries,
            pool_connections=20,
            pool_maxsize=20
        )

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get_all_stocks(self, force_refresh=False):
        if not force_refresh:
            cached_data = cache.get(self.CACHE_KEY)

            if cached_data:
                return cached_data
        headers = self.build_headers()
        try:
            response = self.session.get(
                self.BASE_URL,
                headers=headers,
                timeout=(5, 20)
            )
            print("NGX STATUS:", response.status_code)
            response.raise_for_status()
            
            # Inside get_all_stocks method
            data = response.json()

            # The API returns a dictionary with a 'stocks' key
            stocks_list = data.get('stocks', [])
            if not isinstance(stocks_list, list):
                print("Expected a list under 'stocks' key, got:", type(stocks_list))
                return []

            normalized_data = self.normalize_stock_data(stocks_list)
            
            cache.set(
                self.CACHE_KEY,
                normalized_data,
                timeout=self.CACHE_TIMEOUT
            )
            return normalized_data
        
        except requests.exceptions.SSLError as e:
            print("NGX SSL ERROR:", str(e))
            return self.get_fallback_cache()

        except requests.exceptions.Timeout as e:
            print("NGX TIMEOUT ERROR:", str(e))
            return self.get_fallback_cache()

        except requests.exceptions.ConnectionError as e:
            print("NGX CONNECTION ERROR:", str(e))
            return self.get_fallback_cache()
        
        except requests.exceptions.HTTPError as e:
            print("NGX HTTP ERROR:", str(e))
            return self.get_fallback_cache()

        except requests.exceptions.RequestException as e:
            print("NGX REQUEST ERROR:", str(e))
            return self.get_fallback_cache()

        except ValueError as e:
            print("NGX JSON ERROR:", str(e))
            return self.get_fallback_cache()

        except Exception as e:
            print("NGX UNKNOWN ERROR:", str(e))
            return self.get_fallback_cache()

    def build_headers(self):

        return {
            "X-API-Key": settings.NGX_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://www.ngxpulse.ng",
            "Referer": "https://www.ngxpulse.ng/",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            )
        }

    def get_fallback_cache(self):
        fallback = cache.get(self.CACHE_KEY)
        if fallback:
            print("Using cached NGX fallback data")
            return fallback

        return []

    def normalize_stock_data(self, stocks):
        normalized = []
        for stock in stocks:
            try:
                current_price = self.safe_float(stock.get("current_price", 0))
                pe_ratio = self.safe_float(stock.get("pe_ratio", 0))

                change_percent = self.safe_float(stock.get("change_percent", 0))

                volume = self.safe_int(stock.get("volume", 0))

                upside = self.calculate_upside(
                    current_price,
                    pe_ratio
                )

                recommendation = self.generate_recommendation(
                    change_percent,
                    pe_ratio
                )

                normalized.append({
                    "symbol": stock.get("symbol", ""),
                    "name": stock.get("name", ""),
                    "price": current_price,
                    "change_percent": change_percent,
                    "volume": volume,
                    "sector": stock.get("sector", ""),
                    "pe_ratio": pe_ratio,
                    "upside_potential": upside,
                    "recommendation": recommendation
                })

            except Exception as e:

                print("Stock normalization error:", str(e))

                continue

        return normalized

    def calculate_upside(self, price, pe_ratio):

        try:

            if price <= 0:
                return 0

            fair_value_multiplier = 1.15

            if pe_ratio > 20:
                fair_value_multiplier = 1.05

            elif pe_ratio < 10:
                fair_value_multiplier = 1.25

            fair_value = price * fair_value_multiplier

            upside = (
                (fair_value - price) / price
            ) * 100

            return round(upside, 2)

        except Exception:

            return 0

    def generate_recommendation(self, change_percent, pe_ratio):

        try:

            if change_percent >= 5 and pe_ratio < 15:
                return "STRONG BUY"

            if change_percent > 2:
                return "BUY"

            if change_percent <= -5:
                return "STRONG SELL"

            if change_percent < -2:
                return "SELL"

            return "HOLD"

        except Exception:

            return "HOLD"

    def safe_float(self, value, default=0):

        try:

            if value in [None, "", "N/A"]:
                return default

            return float(value)

        except (TypeError, ValueError):

            return default

    def safe_int(self, value, default=0):
        try:
            if value in [None, "", "N/A"]:
                return default
            return int(float(value))
        except (TypeError, ValueError):
            return default


    def search_stocks(self, query: str):
        """Filter already-fetched stocks by symbol or name (case-insensitive)."""
        all_stocks = self.get_all_stocks()
        query = query.strip().lower()
        if not query:
            return all_stocks
        return [
            s for s in all_stocks
            if query in s.get("symbol", "").lower()
            or query in s.get("name", "").lower()
        ]
