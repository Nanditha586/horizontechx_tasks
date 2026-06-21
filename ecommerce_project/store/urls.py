from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
     
    path('product/<int:product_id>/',
         views.product_detail,
         name='product_detail'),

    path('add-to-cart/<int:product_id>/',
         views.add_to_cart,
         name='add_to_cart'),

    path('cart/',
         views.cart,
         name='cart'),

    path('remove/<int:cart_id>/',
         views.remove_from_cart,
         name='remove_from_cart'),

    path('register/',
         views.register,
         name='register'),

    path('login/',
         views.user_login,
         name='login'),

    path('logout/',
         views.user_logout,
         name='logout'),

    path('checkout/',
         views.checkout,
         name='checkout'),

    path('orders/',
         views.orders,
         name='orders'),
    path('payment/',
         views.payment,
         name='payment'),
    path('profile/',
         views.profile,
         name='profile'), 
    path('wishlist/',
         views.wishlist,
         name='wishlist'),
    path('add-to-wishlist/<int:product_id>/',
         views.add_to_wishlist,
         name='add_to_wishlist'),
    path('invoice/',
         views.invoice,
         name='invoice'),
     path('update-cart/<int:cart_id>/',
     views.update_cart_quantity,
     name='update_cart_quantity'),

path('move-to-wishlist/<int:cart_id>/',
     views.move_to_wishlist,
     name='move_to_wishlist'),
     path(
    'remove-from-wishlist/<int:wishlist_id>/',
    views.remove_from_wishlist,
    name='remove_from_wishlist'
),
]