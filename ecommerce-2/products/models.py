from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
# class ProductQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True)
#
#
class ProductManager(models.Manager):
    def get_related(self, instance):
        product_one = self.get_queryset().filter(categories__in=instance.categories.all())
        default = self.get_queryset().filter(default=instance.default)
        qs = (product_one | default).exclude(id=instance.id).distinct()
        return qs

class Product(models.Model):
    title = models.CharField(max_length=120)
    descripttion = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=60 )
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product_category', blank=True, null=True)
    # Slug
    # Inventory

    # Intanciate Product Manager, if you create custom model manager see below
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def get_img_url(self):
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=60)
    sale_price = models.DecimalField(decimal_places=2, max_digits=60, blank=True, null=True)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" % (reverse("cart"), self.id)

# Save the default variation when the Product model is saved
def product_post_save_recevier(sender, instance, created, *args, **kwargs):
    print(sender, instance, created)
    product = instance
    variations = product.variation_set.all()
    print(variations.count())
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()

post_save.connect(product_post_save_recevier, sender=Product)


# Product Images
def image_upload_to(instance, filename):
    title = instance.product.title
    slug =slugify(title)
    basename, extention = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, extention)
    return "products/%s/%s" % (slug, new_filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)


# Product category
class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


# Featured product
def upload_to_feature(instance, filename):
    title = instance.product.title
    slug =slugify(title)
    basename, extention = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, extention)
    return "products/featured/%s/%s" % (slug, new_filename)

class ProductFeatured(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_feature)
    title = models.CharField(max_length=120, blank=True, null=True)
    text = models.TextField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title

    def get_absolute_url(self):
        return self.product.get_absolute_url()
