from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name=models.CharField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='products/')
    stock=models.PositiveIntegerField(default=0)
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    razorpay_order_id = models.CharField(max_length=200)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)

    total = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
