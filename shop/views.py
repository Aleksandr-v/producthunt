from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Card, Good

@login_required(login_url='/accounts/login')
def card(request):
    total_price = 0
    card = request.user.cards.all()
    for e in card:
        total_price += e.good.price * e.quantity
    return render(request, 'products/card.html', {'card':card, 'total_price':total_price})
