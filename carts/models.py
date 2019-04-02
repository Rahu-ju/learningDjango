from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings

from products.models import Variation

# Create your models here.
class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.item.title

    def get_product_title(self):
        return self.item.product.title

    def get_variation_title(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()

# pre save signals
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    price = instance.item.get_price()
    line_item_total = Decimal(qty) * Decimal(price)
    instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp =  models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id)

    # users
    # item
    # timestamp **created
    # update  **updated

    # subtotal price
    # texes subtotal
    # discounts
    # total price
