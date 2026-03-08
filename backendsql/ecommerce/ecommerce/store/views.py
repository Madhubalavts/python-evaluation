

# Create your views here.
import razorpay
from django.conf import settings
from django.shortcuts import render
from .models import Product, Cart, Order

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def product_list(request):
    products = Product.objects.all()
    return render(request,'products.html',{'products':products})


def checkout(request):

    cart_items = Cart.objects.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    payment = client.order.create({
        "amount": int(total * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request,'checkout.html',{
        'payment':payment,
        'total':total
    })