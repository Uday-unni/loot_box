from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from store.models import CartItem, Product  
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('cart')  

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()

        if not address:
            messages.warning(request, "Please enter your delivery address")
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total': total
            })

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=total,
                address=address,
                paid=True,  # Change to False for real payment
                status='processing'
            )

            # Create order items and reduce stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

                # Reduce stock
                if item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()
                else:
                    messages.error(request, f"Not enough stock for {item.product.name}")
                    raise ValueError("Insufficient stock")

            
            cart_items.delete()

        messages.success(request, f"Your order #{order.id} has been successfully placed!")
        return redirect('orders:success', order_id=order.id)  

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})  


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status not in ['pending', 'processing']:
        messages.error(request, "This order cannot be canceled.")
        return redirect('orders:detail', order_id=order.id)
    
    if request.method == 'POST':
        order.status = 'canceled'
        order.save()
        
        for item in order.orderitem_set.all():
            item.product.stock += item.quantity
            item.product.save()
        
        messages.success(request, f"Order #{order.id} has been canceled successfully.")
        return redirect('orders:history')
    
    return redirect('orders:detail', order_id=order.id)