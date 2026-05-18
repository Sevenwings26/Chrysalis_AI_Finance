# market/services/trading.py
import uuid
from decimal import Decimal
from django.db import transaction as db_transaction
from ..models import Wallet, Portfolio, PortfolioHolding, Transaction


class TradingError(Exception):
    pass


class TradingService:

    def __init__(self, user):
        self.user = user
        self.wallet = self._get_or_create_wallet()
        self.portfolio = self._get_or_create_portfolio()

    # ── internal helpers ──────────────────────────────────────────────

    def _get_or_create_wallet(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.user)
        return wallet

    def _get_or_create_portfolio(self):
        portfolio, _ = Portfolio.objects.get_or_create(
            user=self.user,
            name="Main Portfolio"
        )
        return portfolio

    def _make_reference(self, prefix="TXN"):
        return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"

    # ── public API ────────────────────────────────────────────────────

    def buy(self, symbol: str, name: str, price: float, quantity: int):
        """
        Deduct wallet, upsert holding, log transaction.
        Everything runs in one atomic block.
        """
        price = Decimal(str(price))
        quantity = Decimal(str(quantity))
        total_cost = price * quantity

        with db_transaction.atomic():
            # Re-fetch wallet inside the lock to prevent race conditions
            wallet = Wallet.objects.select_for_update().get(pk=self.wallet.pk)

            if wallet.balance < total_cost:
                raise TradingError(
                    f"Insufficient balance. Need ₦{total_cost:,.2f}, "
                    f"have ₦{wallet.balance:,.2f}."
                )

            # Deduct wallet
            wallet.balance -= total_cost
            wallet.save(update_fields=["balance", "updated_at"])

            # Upsert holding (weighted average price)
            holding, created = PortfolioHolding.objects.get_or_create(
                portfolio=self.portfolio,
                symbol=symbol,
                defaults={
                    "quantity": quantity,
                    "average_buy_price": price,
                }
            )
            if not created:
                total_qty = holding.quantity + quantity
                holding.average_buy_price = (
                    (holding.quantity * holding.average_buy_price + quantity * price)
                    / total_qty
                )
                holding.quantity = total_qty
                holding.save(update_fields=["quantity", "average_buy_price", "updated_at"])

            # Log transaction
            Transaction.objects.create(
                wallet=wallet,
                transaction_type=Transaction.TransactionType.BUY,
                amount=total_cost,
                status=Transaction.TransactionStatus.SUCCESS,
                reference=self._make_reference("BUY"),
                symbol=symbol,
                name=name,
                quantity=quantity,
                price_per_unit=price,
            )

            # Update portfolio totals
            self.portfolio.total_invested += total_cost
            self.portfolio.save(update_fields=["total_invested", "updated_at"])

        return {
            "success": True,
            "message": f"Bought {int(quantity)} unit(s) of {symbol} for ₦{total_cost:,.2f}",
            "new_balance": float(wallet.balance),
        }

    def sell(self, symbol: str, name: str, price: float, quantity: int):
        """
        Credit wallet, reduce holding, log transaction.
        """
        price = Decimal(str(price))
        quantity = Decimal(str(quantity))
        total_proceeds = price * quantity

        with db_transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(pk=self.wallet.pk)

            try:
                holding = PortfolioHolding.objects.select_for_update().get(
                    portfolio=self.portfolio,
                    symbol=symbol
                )
            except PortfolioHolding.DoesNotExist:
                raise TradingError(f"You don't hold any {symbol}.")

            if holding.quantity < quantity:
                raise TradingError(
                    f"You only hold {holding.quantity} unit(s) of {symbol}."
                )

            # Credit wallet
            wallet.balance += total_proceeds
            wallet.save(update_fields=["balance", "updated_at"])

            # Reduce or delete holding
            holding.quantity -= quantity
            if holding.quantity == 0:
                holding.delete()
            else:
                holding.save(update_fields=["quantity", "updated_at"])

            # Log transaction
            Transaction.objects.create(
                wallet=wallet,
                transaction_type=Transaction.TransactionType.SELL,
                amount=total_proceeds,
                status=Transaction.TransactionStatus.SUCCESS,
                reference=self._make_reference("SELL"),
                symbol=symbol,
                name=name,
                quantity=quantity,
                price_per_unit=price,
            )

        return {
            "success": True,
            "message": f"Sold {int(quantity)} unit(s) of {symbol} for ₦{total_proceeds:,.2f}",
            "new_balance": float(wallet.balance),
        }
    