from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def chrysalis(requests):
    return render(requests, 'ai/chrysalis-ai.html')


