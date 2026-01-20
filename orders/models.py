from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    address=models.TextField()
    paid= models.BooleanField(default=False)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}-{self.user.username}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        total = self.quantity * self.price
        return f"{self.product.name} × {self.quantity} - ₹{total}"

    
    def get_total(self):
        return self.quantity * self.price
