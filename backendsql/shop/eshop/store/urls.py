from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
]