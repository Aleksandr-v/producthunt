from django.contrib import admin
from .models import Product, Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'hunter', 'pub_date')

    list_filter = ('hunter', 'pub_date')

    search_fields = ('title', 'body')

    raw_id_fields = ('votes', 'hunter')

    date_hierarchy = 'pub_date'

    ordering = ('pub_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'receiver', 'content', 'pub_date')
