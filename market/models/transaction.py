from django.db import models
from decimal import Decimal
from .wallet import Wallet


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Deposit'
        WITHDRAW = 'WITHDRAW', 'Withdraw'
        BUY = 'BUY', 'Buy Stock'
        SELL = 'SELL', 'Sell Stock'

    class TransactionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )

    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.SUCCESS
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference
    