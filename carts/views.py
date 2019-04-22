from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from products.models import Variation
from .models import Cart, CartItem
from orders.forms import GuestCheckoutForm
from orders.models import UserCheckout, UserAddress, Order
from orders.mixin import CartOrderMixin

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
            # line_item_total, subtotal, tax_total and total
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
            # retrieve tax_total
            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None

            # retrive cart total
            try:
                total = cart_item.cart.total
            except:
                total = None

            return JsonResponse({
                "line_total": line_total,
                "subtotal": subtotal,
                "delete": delete_item,
                "flash_message": flash_message,
                "tax_total": tax_total,
                "total": total
            })

        context ={"object": self.get_object()}
        template = self.template_name
        return render(request, template, context)



# Checkout View
class CheckoutView(CartOrderMixin, FormMixin, DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"
    form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart == None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        # if user is not authenticated or user checkout id is not exist
        # (Where user checkout id coming from session dict which is feeded inside the post function.
        # it is feeded when user submit guest form.)
        # then it show the guest user form and user singn in form.
        # therwise it redirect to the AddressCreateView
        # then it redirect to AddressSelectFormView
        # then it redirect to CheckoutView once again and show the order deatils.

        user_can_continue = False
        user_checkout_id = self.request.session.get("user_checkout_id")

        # If user is authenticated then it automatically create userchecout
        # object depending on that user.
        # and then feeding the user checkout id to the session dict.
        if self.request.user.is_authenticated:
            email = self.request.user.email
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)
            user_checkout.user = self.request.user
            user_checkout.save()
            self.request.session["user_checkout_id"] = user_checkout.id
            context["client_token"] = user_checkout.get_client_token
            user_can_continue = True

        elif not self.request.user.is_authenticated and user_checkout_id == None:
            context["login_form"] = AuthenticationForm()
            # build Absolute url for this view and feed to the context dict
            context["next_url"] = self.request.build_absolute_uri()
            context["guest_form"] = self.get_form()
        else:
            pass
        if user_checkout_id != None:
            user_can_continue = True
            if not self.request.user.is_authenticated:
                user_checkout2 = UserCheckout.objects.get(id=user_checkout_id)
                context["client_token"] = user_checkout2.get_client_token

        context["user_can_continue"] = user_can_continue
        # Feeding order instance
        context['order'] = self.get_order()
        return context

    def post(self, request, *args, **kwargs):
        # Process the data from guest checkout form.
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data['email']

            # Create userchecout object if the email is not already exist
            # if it exist then it get the object instance.
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)

            # Feeded the user checkout id into the session dict
            request.session["user_checkout_id"] = user_checkout.id

            # return self.form_valid(form)
            # its better to use  the following redirect url when the form is valid
            return self.get_success_url()
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        # take data from user address form and  feed to the order instance and save.


        cart = self.get_cart()
        if cart == None:
            messages.info(request, "Your order is being processed less than 24 hours..")
            return redirect("cart")
        new_order = self.get_order()
        user_checkout_id = request.session.get('user_checkout_id')
        if user_checkout_id != None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if new_order.billing_address == None or new_order.shipping_address == None:
                return redirect(reverse("address_select"))
            new_order.user = user_checkout
            new_order.save()

        return super(CheckoutView, self).get(request, *args, **kwargs)


    def get_success_url(self):
        return HttpResponseRedirect(reverse("checkout"))


class CheckoutFinalView(CartOrderMixin, View):
    def post(self, request, *args, **kwargs):
        """ As the form submitted, It's save the order status as completed,
            delete cart_id, new_order_id from session and then redirect to
            the CheckoutView, it's redirect to the CartView as the cart_id doesn't
            exist.
        """
        order = self.get_order()
        if request.POST.get("payment_token") == "abc":
            order.mark_completed()
            del request.session["cart_id"]
            del request.session["new_order_id"]
            messages.success(request, "Thank you for your order.")
        return redirect('order_detail', pk=order.pk)

    def get(self, request, *args, **kwargs):
        return redirect('checkout')
