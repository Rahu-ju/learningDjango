from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from products.models import Variation
from carts.models import Cart, CartItem

# Create your views here.

class CartView(SingleObjectMixin, View):
    model = Cart
    template_name ="carts/view.html"

    def get_object(self, *args, **kwargs):
        # if session dict have cart id then it retrive the cart instance using that id
        # or it create new cart and then append the new cart id to the session dict
        # then retrive that cart instance using new cart id and last return the cart object.
        self.request.session.set_expiry(0) #session close when web browser close
        cart_id = self.request.session.get('cart_id')
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated:
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        # It takes item, qty(quanty), delete from the ulr
        # then retrive the item instance from variation model,
        # create cart instane and then
        # Finally create CartItem instance then save it. and redirect to home page.

        item_id = request.GET.get('item')
        qty = request.GET.get('qty', 1)
        delete_item = request.GET.get("delete")

        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            cart = self.get_object()
            cart_item = CartItem.objects.get_or_create(cart=cart, item=item_instance)[0]

            if delete_item:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
        # if request.is_ajax():
        #     return JsonResponse({"success": True})

        context ={"object": self.get_object()}
        template = self.template_name
        return render(request, template, context)
