from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=50, decimal_places=2, default=29.99)
    sale_price = models.DecimalField(max_digits=50, decimal_places=2, null=True, blank=True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        return self.productimage_set.all()[0].image.url



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images')
    feature = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.title



class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)
    
    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')

VAR_CATEGORIES = (
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(ProductImage, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self):
        return self.title
    
    