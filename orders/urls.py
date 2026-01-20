 # orders/urls.py

from django.urls import path
from . import views

app_name = 'orders'  

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('history/', views.order_history, name='history'),
    path('detail/<int:order_id>/', views.order_detail, name='detail'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel'),  
]