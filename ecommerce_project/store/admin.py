from django.contrib import admin
from .models import Product, Cart, Order, Category,Wishlist, Review

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Review)