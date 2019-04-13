from django.db import models
from django.conf import settings

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
