from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)