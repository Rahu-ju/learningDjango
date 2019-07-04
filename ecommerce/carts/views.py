from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from products.models import Product

from .models import Cart, CartItem

# Create your views here.
def view(request):
    # retrive cart from session, making context, render
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    
    if the_id:
        cart = Cart.objects.get(id=the_id)
        context = {'cart': cart}
    else:
        context = {'empty': True}
    
    template = 'carts/cart.html'
    return render(request, template, context)



# 
def update_cart(request, slug):
    # retrive the product
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExists:
        pass
    except:
        pass
    
    # retrive the cart
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    # Feed to the CartItem
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # update quantity, price
    try:
        qty = request.GET.get('qty')
        if qty == 0:
            cart_item.delete()
        else:
            cart_item.quantity = qty
            cart_item.save()
    except:
        pass

    new_total = 0.00
    for item in cart.cartitem_set.all():
        line_total = float(item.product.price) * item.quantity
        new_total += line_total

    cart.total = new_total
    cart.save()

    request.session['items_total'] = cart.cartitem_set.count()

    return HttpResponseRedirect(reverse('cart'))



