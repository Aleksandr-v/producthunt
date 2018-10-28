from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .models import Product, Comment
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from producthunt.decorators import timeit, user_is_product_hunter
from .forms import CommentForm

@method_decorator(timeit, name='dispatch')
class ProductList(ListView):
    model = Product

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class ProductCreate(CreateView):
    model = Product
    fields = ('title', 'body', 'url', 'icon', 'image')

    def form_valid(self, form):
        form.instance.hunter = self.request.user
        form.instance.save()
        return super().form_valid(form)


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm
            context['comments'] = Comment.first_level.filter(product=kwargs['object'].id).order_by('-pub_date')
        return context

@method_decorator(require_http_methods(["POST"]), name='dispatch')
class AddComment(View):
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        product = get_object_or_404(Product, pk=kwargs.get('pk'))

        if form.is_valid():
            comment = Comment()
            comment.product = product
            comment.author = request.user
            comment.content = form.cleaned_data['comment_area']
            if form.cleaned_data['parent_comment'] is not None:
                comment.parent = get_object_or_404(Comment, pk=form.cleaned_data['parent_comment'])
                comment.receiver = get_object_or_404(User, pk=form.cleaned_data['receiver'])
            comment.save()
        return redirect(product.get_absolute_url())


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
@method_decorator(user_is_product_hunter, name='dispatch')
class ProductUpdate(UpdateView):
    model = Product
    template_name_suffix = '_update'
    fields = ('title', 'body', 'url', 'icon', 'image')

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
@method_decorator(user_is_product_hunter, name='dispatch')
class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('home')

@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class ProductUpvote(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        if product.votes.filter(pk=request.user.id).exists():
            product.votes.remove(request.user)
        else:
            product.votes.add(request.user)
        return redirect(product.get_absolute_url())
