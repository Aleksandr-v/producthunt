from django.urls import path
from . import views

urlpatterns = [
    path('create', views.ProductCreate.as_view(), name='create_product'),
    path('<int:pk>', views.ProductDetail.as_view(), name='detail'),
    path('<int:pk>/add-comment', views.AddComment.as_view(), name='add_comment'),
    path('<int:pk>/update', views.ProductUpdate.as_view(), name='update'),
    path('<int:pk>/delete', views.ProductDelete.as_view(), name='delete'),
    path('upvote/<int:product_id>', views.ProductUpvote.as_view(), name='upvote'),
]
