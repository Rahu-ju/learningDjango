from django.shortcuts import render, get_object_or_404
from django.urls import reverse
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
        item_added = False
        cart = self.get_object()
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            if created:
                item_added = True
                flash_message = "Successfully added to the cart."
            if not created:
                flash_message = "Quantity successfully updated."

            # if qyt is less than 1 then it should delete the cart item. security purpose
            try:
                if int(qty) < 1:
                    delete_item = True
                    flash_message = "Item removed successfully."
            except:
                raise Http404

            # Delete the cart item
            if delete_item:
                cart_item.delete()
                flash_message = "Item removed successfully."
            else:
                cart_item.quantity = qty
                cart_item.save()

            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))

        if request.is_ajax():
            # Checking the line total
            try:
                line_total = cart_item.line_item_total
            except:
                line_total = None

            # Checking the subtotal
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None

            return JsonResponse({
                "line_total": line_total,
                "subtotal": subtotal,
                "delete": delete_item,
                "flash_message": flash_message
            })

        context ={"object": self.get_object()}
        template = self.template_name
        return render(request, template, context)
