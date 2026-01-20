from django.db.models import F, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from .models import Product, Category, CartItem


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:8]
    return render(request, 'home.html', {
        'categories': categories,
        'products': products
    })

def search(request):
    query = request.GET.get('q', '').strip()
    
    # Start with all products that have stock > 0 (instead of 'available=True')
    products = Product.objects.filter(stock__gt=0)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(desc__icontains=query) |  # 'desc' is your field name
            Q(category__name__icontains=query)
        ).distinct()  # Avoid duplicates if category matches

    context = {
        'products': products,
        'query': query,
        'count': products.count()
    }
    return render(request, 'store/search_results.html', context)

def category_detail(request,slug):
    category=get_object_or_404(Category,slug=slug)
    products=Product.objects.filter(category=category)
    return render(request,'store/category_detail.html',{
        'category':category,
        'products':products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Handle session for guest users
    if not request.session.session_key:
        request.session.create()
    filters = {
        'product': product,
    }
    if request.user.is_authenticated:
        filters['user'] = request.user
        filters['session_key'] = None
    else:
        filters['user'] = None
        filters['session_key'] = request.session.session_key

    # Get or create cart item
    item, created = CartItem.objects.get_or_create(
        **filters,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity = F('quantity') + 1
        item.save(update_fields=['quantity'])

    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart')


def cart(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user).select_related('product')
    else:
        if not request.session.session_key:
            request.session.create()
        items = CartItem.objects.filter(
            session_key=request.session.session_key,
            user=None
        ).select_related('product')

    # Calculate total and count safely (in case cart is empty)
    total = sum(item.product.price * item.quantity for item in items)
    count = sum(item.quantity for item in items)

    return render(request, 'store/cart.html', {
        'cart_items': items,  # renamed for clarity in template
        'total': total,
        'count': count
    })


def update_cart(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 0))  # Current quantity from input
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Security check 
        if (request.user.is_authenticated and cart_item.user == request.user) or \
           (not request.user.is_authenticated and cart_item.session_key == request.session.session_key):
            
            if action == 'increase':
                if quantity < cart_item.product.stock:
                    cart_item.quantity = quantity + 1
                    messages.success(request, 'Quantity increased!')
                else:
                    messages.warning(request, 'Maximum stock reached!')
            elif action == 'decrease':
                if quantity > 1:
                    cart_item.quantity = quantity - 1
                    messages.success(request, 'Quantity decreased!')
                else:
                    cart_item.delete()
                    messages.success(request, 'Item removed from cart!')
            else:
                # Fallback if no action (e.g., user typed a number and submitted)
                if 1 <= quantity <= cart_item.product.stock:
                    cart_item.quantity = quantity
                    messages.success(request, 'Cart updated!')
                else:
                    messages.error(request, 'Invalid quantity!')
            
            cart_item.save()  # Save only if not deleted
        else:
            messages.error(request, 'Invalid cart item.')
    
    return redirect('cart')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)  #

    # Security check
    if item.user == request.user or (not item.user and item.session_key == request.session.session_key):
        item.delete()
        messages.success(request, "Item removed from cart")

    return redirect('cart')