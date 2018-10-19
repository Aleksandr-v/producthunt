from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name='create_product'),
    path('<int:product_id>', views.detail, name='detail'),
    path('upvote/<int:product_id>', views.upvote, name='upvote')
]
