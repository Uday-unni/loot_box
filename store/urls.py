from django.contrib.auth.password_validation import password_validators_help_text_html
from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('product/<slug:slug>',views.product_detail,name='product_detail'),
    path('cart/',views.cart,name='cart'),
    path('add-to-cart/<int:product_id>',views.add_to_cart,name='add_to_cart'),
    path('category_detail/<slug:slug>',views.category_detail,name='category_detail'),
    path('search',views.search,name='search'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

]