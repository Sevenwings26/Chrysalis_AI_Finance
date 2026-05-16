from decimal import Decimal
import uuid
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Wallet, Transaction



@login_required
def dashboard(request):
    # wallet = request.user.wallet
    wallet, created = Wallet.objects.get_or_create(
        user=request.user
    )
    transactions = wallet.transactions.all().order_by('-created_at')[:10]

    context = {
        'wallet': wallet,
        'transactions': transactions
    }

    return render(
        request,
        "market/paperT-home.html",
        context
    )


@login_required
def deposit_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)

            if amount <= 0:
                messages.error(request, "Invalid deposit amount")
                return redirect('paper-wallet')

            wallet = request.user.wallet

            wallet.balance += amount
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                transaction_type='DEPOSIT',
                amount=amount,
                status='SUCCESS',
                reference=str(uuid.uuid4())
            )
            messages.success(
                request,
                f"₦{amount} deposited successfully"
            )
        except Exception as e:
            print(e)
            messages.error(request, "Deposit failed")
    return redirect('paper-wallet')


