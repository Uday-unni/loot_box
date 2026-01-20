# store/admin.py
from django.contrib import admin
from .models import Category, CartItem, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','image')
    search_fields = ('name',)
    readonly_fields = ('slug',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'desc')
    readonly_fields = ('created_at',)

    fields = ('name',  'category', 'desc', 'image', 'price', 'stock', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'product', 'quantity')
    list_filter = ('product__category',)
    search_fields = ('product__name', 'user__username', 'session_key')