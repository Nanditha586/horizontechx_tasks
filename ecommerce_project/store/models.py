from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='products/'
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.name


class Cart(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name
    
#order model
class Order(models.Model):

    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Processing', 'Processing'),

        ('Shipped', 'Shipped'),

        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)

    quantity = models.IntegerField()

    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2)

    address = models.TextField()

    phone = models.CharField(max_length=15)

    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user.username
#wishlist model
class Wishlist(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)

    

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.user.username
#review model
class Review(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)

    rating = models.IntegerField()

    comment = models.TextField()

    image = models.ImageField(upload_to='reviews/images/',
                              blank=True,
                              null=True)

    video = models.FileField(upload_to='reviews/videos/',
                             blank=True,
                             null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('user', 'product')

    def __str__(self):

        return self.user.username