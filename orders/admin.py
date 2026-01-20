from django.contrib import admin
from .models import Order,OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total_price','paid','status','created_at')
    list_filter = ('status','paid','created_at')
    search_fields = ('user__username','id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display =('order_id','order','price','quantity','product')
    list_select_related = ('order','product')

