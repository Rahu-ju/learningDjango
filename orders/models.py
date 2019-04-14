from django.db import models
from django.conf import settings

from carts.models import Cart

#User checkout model
class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True) #optional as it also used by guest user
    email = models.EmailField(unique=True)

    # merchant_id

    def __str__(self):
        return self.email


# User address model.
address_type = (
    ('billing', 'billing'),
    ('shipping', 'shipping'),
)

class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout, on_delete=models.CASCADE)
    type = models.CharField(max_length=120, choices=address_type)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)

    def __str__(self):
        return self.street


# Order model
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(UserCheckout, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE,related_name="billing_address")
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE,related_name="shipping_address")
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5)
    order_total = models.DecimalField(max_digits=50, decimal_places=2)
    # order_id

    def __str__(sefl):
        return self.cart.id
