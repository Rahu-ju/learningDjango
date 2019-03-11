from django.db import models
from django.contrib.auth.models import AbstractUser


#  models here.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

#Modelling the user profile
# class UserProfile(models.Model):
#     '''It's only take the user headshot.'''
#     user = models.OneToOneField(
#         CustomUser,
#          on_delete=models.CASCADE,
#     )
#     image = models.ImageField(upload_to='media/')
#
#
#     def __str__(self):
#         return self.user.email
