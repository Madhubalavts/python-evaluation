from .models import Cart, CartItem

def cart_count(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = sum(item.quantity for item in cart_items)

    return {'cart_count': cart_count}