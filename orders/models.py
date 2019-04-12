from django.db import models
from django.conf import settings

# Create your models here.
class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True) #optional as it also used by guest user
    email = models.EmailField(unique=True)

    # merchant_id

    def __str__(self):
        return self.email
