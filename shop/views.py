from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Card, Good
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from producthunt.decorators import timeit
from django.views import View


@timeit
@login_required(login_url='/accounts/login')
def card(request):
    total_price = 0
    card = request.user.cards.all()
    for e in card:
        total_price += e.good.price * e.quantity
    return render(request, 'products/card.html', {'card':card, 'total_price':total_price})

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class CardListView(ListView):
    template_name = 'products/card.html'

    def get_queryset(self):
        return self.request.user.cards.all()

    def get_context_data(self, total_price=0, **kwargs):
        context = super().get_context_data(**kwargs)
        for e in self.get_queryset():
            total_price += e.good.price * e.quantity
        context['total_price'] = total_price
        return context

@method_decorator(timeit, name='dispatch')
class ShopView(View):
    def get(self, request):
        goods = Good.objects.all()
        good_list = [goods[i:i+3] for i in range(0, len(goods), 3)]
        return render(request, 'shop/good_list.html', {'good_list': good_list})

@timeit
def add_good_to_card(request, good_id):
    try:
        card = Card.objects.get(good_id=good_id, owner_id=request.user)
        card.quantity += 1
        card.save()
        return redirect('card')
    except Card.DoesNotExist:
        card = Card.objects.create(good_id=good_id, owner_id=request.user.id, quantity=1)
        return redirect('card')
