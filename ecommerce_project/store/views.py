from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, Category, Wishlist, Review
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from django.shortcuts import render, redirect
def home(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    search = request.GET.get('search')

    category_id = request.GET.get('category')
    wishlist_products = []

    if request.user.is_authenticated:

        wishlist_products = Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)

    if search:

        products = products.filter(name__icontains=search)

    if category_id:

        products = products.filter(category_id=category_id)

    paginator = Paginator(products, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request,
                  'store/home.html',
                  {
                      'page_obj': page_obj,
                      'categories': categories,
                      'wishlist_products': wishlist_products,
                  })


from django.contrib import messages

def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)

    reviews = Review.objects.filter(product=product)

    already_reviewed = False

    if request.user.is_authenticated:

        already_reviewed = Review.objects.filter(
            user=request.user,
            product=product
        ).exists()

    if request.method == 'POST':

        if already_reviewed:

            pass

        else:

            rating = request.POST.get('rating')

            comment = request.POST.get('comment')

            image = request.FILES.get('image')

            video = request.FILES.get('video')

            Review.objects.create(

                user=request.user,

                product=product,

                rating=rating,

                comment=comment,

                image=image,

                video=video
            )

    return render(request,
                  'store/product_detail.html',
                  {
                      'product': product,
                      'reviews': reviews,
                      'already_reviewed': already_reviewed
                  })
#remove cart view
@login_required
def remove_from_cart(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    cart_item.delete()

    return redirect('cart')
#register view
def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = RegisterForm()

    return render(request,
                  'store/register.html',
                  {'form': form})
#login view
def user_login(request):

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:

        form = AuthenticationForm()

    return render(request,
                  'store/login.html',
                  {'form': form})
#logout view
def user_logout(request):

    logout(request)

    return redirect('home')
#user specific cart
@login_required


def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(

        user=request.user,

        product=product

    )

    if created:

        cart_item.quantity = quantity

    else:

        cart_item.quantity += quantity

    cart_item.save()

    return redirect('/cart/')
#update cart view
@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:

        total += item.product.price * item.quantity

    return render(request,
                  'store/cart.html',
                  {
                      'cart_items': cart_items,
                      'total': total
                  })
#checkout view
@login_required


def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:

        total += item.product.price * item.quantity

    if request.method == "POST":

        address = request.POST.get('address')

        phone = request.POST.get('phone')

        request.session['address'] = address
        request.session['phone'] = phone

        return redirect('payment')

    return render(request,
                  'store/checkout.html',
                  {'total': total})
#orders view
@login_required


def orders(request):

    orders = Order.objects.filter(user=request.user)

    reviewed_products = []

    for order in orders:

        already_reviewed = Review.objects.filter(
            user=request.user,
            product=order.product
        ).exists()

        reviewed_products.append({

            'order': order,

            'already_reviewed': already_reviewed

        })

    return render(request,
                  'store/orders.html',
                  {
                      'reviewed_products': reviewed_products
                  })
#payment view
@login_required



def payment(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:

        total += item.product.price * item.quantity

    if request.method == "POST":

        for item in cart_items:

            # CREATE ORDER

            Order.objects.create(

                user=request.user,

                product=item.product,

                quantity=item.quantity,

                total_price=item.product.price * item.quantity,

                status="Placed"
            )

            # REDUCE PRODUCT STOCK

            product = item.product

            product.stock -= item.quantity

            # PREVENT NEGATIVE STOCK

            if product.stock < 0:

                product.stock = 0

            product.save()

        # CLEAR CART

        cart_items.delete()

        return redirect("orders")

    return render(request,
                  "store/payment.html",
                  {
                      "total": total
                  })


# wishlist view

from django.shortcuts import redirect
from .models import Wishlist, Product
@login_required
def add_to_wishlist(request, product_id):

    product = Product.objects.get(id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('/')


@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(request,
                  'store/wishlist.html',
                  {
                      'wishlist_items': wishlist_items
                  })
#profile view
@login_required
def profile(request):

    orders = Order.objects.filter(user=request.user)

    return render(request,
                  'store/profile.html',
                  {
                      'orders': orders
                  })
#invoice view
@login_required
def invoice(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="invoice.pdf"'
    )

    p = canvas.Canvas(response)

    p.drawString(100, 800, "MyShop Invoice")

    orders = Order.objects.filter(user=request.user)

    y = 750

    for order in orders:

        p.drawString(
            100,
            y,
            f"{order.product.name} - ₹{order.total_price}"
        )

        y -= 30

    p.showPage()

    p.save()

    return response
from .models import Cart, Wishlist

# UPDATE QUANTITY

def update_cart_quantity(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    quantity = int(request.POST.get('quantity'))

    cart_item.quantity = quantity

    cart_item.save()

    return redirect('/cart/')


# MOVE TO WISHLIST

def move_to_wishlist(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    Wishlist.objects.get_or_create(

        user=request.user,

        product=cart_item.product

    )

    cart_item.delete()

    return redirect('/cart/')
def remove_from_wishlist(request, wishlist_id):

    item = Wishlist.objects.get(id=wishlist_id)

    item.delete()

    return redirect('wishlist')