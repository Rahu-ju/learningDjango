from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.conf import settings

from products.models import Variation

# Create your models here.
class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

    print(line_item_total)
    def __str__(self):
        return self.item.title

    def get_product_title(self):
        return self.item.product.title

    def get_variation_title(self):
        return self.item.title

    def remove(self):
        return self.item.remove_from_cart()

# Calculate and feed the line total before the cart item save using pre save signals
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    price = instance.item.get_price()
    line_item_total = Decimal(qty) * Decimal(price)
    instance.line_item_total = line_item_total
pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


# Calculate tand feed he subtotal after the cart item save using post save signal
def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()
post_save.connect(cart_item_post_save_receiver, sender=CartItem)

# If any cart item remove from cart then its call to update the subtotal again.
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(Variation, through=CartItem)
    timestamp =  models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # the default number in the following  field is not matter because 
    # those field is feeded in time as it is need.
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
    tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.085)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        items = self.cartitem_set.all()
        subtotal = 0
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()

# Calculate and feed the tax_total and total before the cart save
def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
    subtotal = Decimal(instance.subtotal)
    tax_total = round(subtotal * Decimal(0.085), 2)
    total =round(subtotal + Decimal(tax_total), 2)
    instance.tax_total = tax_total
    instance.total = total
pre_save.connect(do_tax_and_total_receiver, sender=Cart)


    # users
    # item
    # timestamp **created
    # update  **updated

    # subtotal price
    # texes subtotal
    # discounts
    # total price
