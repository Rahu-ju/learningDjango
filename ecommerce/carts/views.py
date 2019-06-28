from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from products.models import Product

from .models import Cart

# Create your views here.
def view(request):
    # retrieve the data from cart
    cart = Cart.objects.all()[0]
    context = {'cart': cart}
    template = 'carts/cart.html'
    return render(request, template, context)



# 
def update_cart(self, slug):
    # retrive the product
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExists:
        pass
    except:
        pass
    
    # retrive the cart, checking the product or remove
    cart = Cart.objects.all()[0]
    if not product in cart.products.all():
        cart.products.add(product)
    else:
        cart.products.remove(product)

    # update price, save
    new_total = 0.00
    for item in cart.products.all():
        new_total += float(item.price)

    cart.total = new_total
    cart.save()

    return HttpResponseRedirect(reverse('cart'))



