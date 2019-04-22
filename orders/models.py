from decimal import Decimal

import braintree

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings

from carts.models import Cart


if settings.DEBUG:
    gateway = braintree.BraintreeGateway(
      braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id= settings.BRAINTREE_MERCHAND,
        public_key= settings.BRAINTREE_PUBLIC,
        private_key=settings.BRAINTREE_PRIVATE
      )
    )



#User checkout model
class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True) #optional as it also used by guest user
    email = models.EmailField(unique=True)
    braintree_id = models.CharField(max_length=120, blank=True, null=True)

    # merchant_id

    def __str__(self):
        return self.email

    # Braintree functionality
    @property
    def get_customer_braintree_id(self):
        # its create customer braintree  account and
        # return that customer id and save it to the database.
        instance = self
        if not instance.braintree_id:
            result = gateway.customer.create({
                "email": instance.email
            })
            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id

    # Using customer id it generate client token and retur that.
    def get_client_token(self):
        client_token = gateway.client_token.generate({
            "customer_id": self.get_customer_braintree_id
        })
        return client_token

def update_braintree_id(sender, instance, *args, **kwargs):
    instance.get_customer_braintree_id
post_save.connect(update_braintree_id, sender=UserCheckout)


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

    def get_address(self):
        return "%s, %s, %s-%s" % (self.street, self.city, self.state, self.zipcode)


# Order model
ORDER_STATUS_CHOICES = (
    ('completed', 'Completed'),
    ('created', 'Created')
)

class Order(models.Model):
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(UserCheckout, on_delete=models.CASCADE, null=True)
    billing_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE,related_name="billing_address", null=True)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE,related_name="shipping_address", null=True)
    shipping_total_price = models.DecimalField(max_digits=50, decimal_places=2, default=5)
    order_total = models.DecimalField(max_digits=50, decimal_places=2)
    # order_id

    def __str__(self):
        return str(self.id)

    def mark_completed(self):
        self.status = 'completed'
        self.save()

# Calculate the order total before save the order model.
def order_pre_save(sender, instance, *args, **kwargs):
    shipping_total = instance.shipping_total_price
    cart_total = instance.cart.total
    order_total = Decimal(shipping_total) + Decimal(cart_total)
    instance.order_total  = Decimal(order_total)
pre_save.connect(order_pre_save, sender=Order)
