from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import View

from products.models import Variation
from carts.models import Cart

# Create your views here.

class CartView(View):
    # It takes item, qty(quanty), delete from the ulr
    # then retrive the item instance from variation model,
    # create cart instane and then
    # Finally create CartItem instance then save it. and redirect to home page.
    def get(self, request, *args, **kwargs):
        item_id = request.GET.get('item')
        qty = request.GET.get('qty')
        delete_item = request.GET.get("delete")

        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            cart = Cart.objects.all().first()
            cart_item = CartItem.objects.get_or_create(cart=cart, item=item_instance)[0]

            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()

        return HttpResponseRedirect('/')
