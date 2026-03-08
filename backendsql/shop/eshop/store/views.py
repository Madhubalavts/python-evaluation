import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm


# ---------------- REGISTER ----------------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- HOME ----------------
from .models import Product, Category
from django.db.models import Q

def home(request):

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.filter(is_available=True)
    # categories = Category.objects.all()
    categories = Category.objects.filter(parent__isnull=True)

    # 🔎 Search filter
    if query and query.strip() != "":
        products = products.filter(
            Q(name__icontains=query.strip()) |
            Q(description__icontains=query.strip())
        )

    # 📂 Category filter
   
    if category_id:
        selected_category = Category.objects.filter(id=category_id).first()

        if selected_category:
            subcategories = selected_category.subcategories.all()

            if subcategories.exists():
                products = products.filter(
                    Q(category=selected_category) |
                    Q(category__in=subcategories)
                )
            else:
                products = products.filter(category=selected_category)

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
    })


# ---------------- ADD TO CART ----------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# ---------------- CART PAGE ----------------
@login_required
def cart_page(request):
    cart = Cart.objects.filter(user=request.user).first()

    cart_items = []
    total_price = 0
    cart_count = 0

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            item.subtotal = item.product.price * item.quantity
            total_price += item.subtotal
            cart_count += item.quantity

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count
    })
    
from django.shortcuts import get_object_or_404, redirect
from .models import CartItem

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


# ---------------- CHECKOUT ----------------
@login_required
def checkout(request):

    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return redirect("cart")

    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect("cart")

    total = sum(item.product.price * item.quantity for item in items)

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")
        phone = request.POST.get("phone")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        payment = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": "1"
        })

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            postal_code=postal_code,
            phone=phone,
            total=total,
            razorpay_order_id=payment['id']
        )

        return render(request, "store/payment.html", {
            "order": order,
            "payment": payment,
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    return render(request, "store/checkout.html", {
        "cart_items": items,
        "total": total
    })


@login_required
def payment_success(request):

    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("razorpay_payment_id")

    order = get_object_or_404(Order, id=order_id, user=request.user)

    if payment_id:
        order.razorpay_payment_id = payment_id
        order.paid = True
        order.save()

        # Clear Cart
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            CartItem.objects.filter(cart=cart).delete()

    return render(request, "store/payment_success.html", {"order": order})

