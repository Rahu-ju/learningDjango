from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from products.models import Variation
from carts.models import Cart, CartItem

# Create your views here.
class CartItemCountView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get('cart_id')
            if cart_id == None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()

                request.session["cart_item_count"] = count
            return JsonResponse({"cart_item": count})
        else:
            raise Http404


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
        # get item_id, qty and delete_item from the url

        # then Create the variation instance from item_id
        # create the cart instance
        # then create the cartItem instance from those

        # now show the flash message if
        # new cart item is create or
        # quantity is update or not

        # now checking if it is requested to delete the cart item or not.
        # at last save the cart item.

        # get parameter from url
        item_id = request.GET.get('item')
        qty = request.GET.get('qty', 1)
        delete_item = request.GET.get("delete")

        if item_id:
            # Creating instance area
            item_instance = get_object_or_404(Variation, id=item_id)
            cart = self.get_object()
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)

            # flash message for create new cart item or update quantity or not.
            if created:
                flash_message = "Successfully added to the cart."
            else:
                if cart_item.quantity == int(qty):
                    flash_message = "This product already added to cart."
                else:
                    flash_message = "Quantity successfully updated."

            # if qyt is less than 1 then it should delete the cart item. security purpose
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404

            # delete the cartItem if it is requested to delete.
            if delete_item:
                cart_item.delete()
                flash_message = "Item removed successfully."
            else:
                cart_item.quantity = qty
                cart_item.save()

            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))

        if request.is_ajax():
            # For ajax response it retrive
            # line_item_total and subtotal
            # and take flash message.
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
