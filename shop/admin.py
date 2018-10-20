from django.contrib import admin
from .models import Good, Card

@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('owner',)
