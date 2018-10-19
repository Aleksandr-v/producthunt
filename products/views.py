from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product
from django.utils import timezone

def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products':products})

@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = Product()
            product = form.save(commit=False)
            product.icon = form.cleaned_data['icon']
            product.image = form.cleaned_data['image']
            product.hunter = request.user
            product.save()
            return redirect('detail', product_id=product.id)
    else:
        form = ProductForm()
        return render(request, 'products/create.html', {'form':form})

@login_required(login_url='/accounts/login')
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required(login_url='/accounts/login')
def upvote(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.votes_total += 1
    product.save()
    return redirect('detail', product_id=product.id)
