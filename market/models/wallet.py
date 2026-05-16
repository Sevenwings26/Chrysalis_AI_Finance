from django.db import models
from django.conf import settings
from decimal import Decimal


class Wallet(models.Model):
    """Simple Cash Wallet"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')

    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - ₦{self.balance}"


class Portfolio(models.Model):
    """User's Investment Portfolio"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100, default="Main Portfolio")
    
    total_invested = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.email} - {self.name}"


class PortfolioHolding(models.Model):
    """Individual Stock Holdings"""
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    
    symbol = models.CharField(max_length=20)          # e.g., UBA, ACCESSCORP
    quantity = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0'))
    average_buy_price = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('portfolio', 'symbol')

    def __str__(self):
        return f"{self.symbol} ({self.quantity} units)"
    