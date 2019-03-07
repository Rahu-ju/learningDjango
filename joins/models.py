from django.db import models

# Create your models here.
class Join(models.Model):
    ''' Its a model to save user email who joins some offer.'''
    email = models.EmailField(unique=True)
    friend = models.ForeignKey('self', on_delete=models.CASCADE, related_name='referal', null=True, blank=True)
    ref_id = models.CharField(max_length=100, default='abd')
    ip_address = models.CharField(max_length=120, default='abc')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

    class META:
        unique_together = ("email", "ref_id")
