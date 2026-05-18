# market/views/trading.py
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt   # remove if you send the CSRF token properly
from ..services.trading import TradingService, TradingError


@login_required
@require_POST
def buy_stock(request):
    try:
        data = json.loads(request.body)
        symbol   = data["symbol"].upper().strip()
        name     = data.get("name", symbol)
        price    = float(data["price"])
        quantity = int(data["quantity"])

        if quantity <= 0:
            return JsonResponse({"success": False, "error": "Quantity must be at least 1."}, status=400)

        service = TradingService(request.user)
        result  = service.buy(symbol, name, price, quantity)
        return JsonResponse(result)

    except TradingError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    except (KeyError, ValueError) as e:
        return JsonResponse({"success": False, "error": "Invalid request data."}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": "Something went wrong."}, status=500)
    # except Exception as e:
    #     import traceback
    #     traceback.print_exc()  # prints full traceback to Django console
    #     return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
@require_POST
def sell_stock(request):
    try:
        data = json.loads(request.body)
        symbol   = data["symbol"].upper().strip()
        name     = data.get("name", symbol)
        price    = float(data["price"])
        quantity = int(data["quantity"])

        if quantity <= 0:
            return JsonResponse({"success": False, "error": "Quantity must be at least 1."}, status=400)

        service = TradingService(request.user)
        result  = service.sell(symbol, name, price, quantity)
        return JsonResponse(result)

    except TradingError as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
    except (KeyError, ValueError):
        return JsonResponse({"success": False, "error": "Invalid request data."}, status=400)
    except Exception:
        return JsonResponse({"success": False, "error": "Something went wrong."}, status=500)

