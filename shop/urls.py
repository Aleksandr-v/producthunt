from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopView.as_view(), name='good-list'),
    path('card', views.CardListView.as_view(), name='card'),
    path('card/add/<int:good_id>', views.add_good_to_card, name='add-good-to-card'),
]
