from django.shortcuts import render, reverse, redirect
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.contrib import messages

from .forms import AddressSelectForm, AddressCreateForm
from .models import UserAddress, UserCheckout, Order
from .mixin import CartOrderMixin


# Create your views here.
class OrderList(ListView):
    queryset = Order.objects.all()

    def get_queryset(self):
        user_checkout_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        return super(OrderList, self).get_queryset().filter(user=user_checkout)


class AddressCreateView(CreateView):
    form_class = AddressCreateForm
    template_name = "orders/address_create.html"
    success_url = "/order/address/"

    def get_checkout_user(self):
        user_checkout_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        return super(AddressCreateView, self).form_valid(form, *args, **kwargs)


class AddressSelectFormView(CartOrderMixin, FormView):
    form_class = AddressSelectForm
    template_name = "orders/address_select.html"

    def dispatch(self, *args, **kwargs):
        b_address, s_address = self.get_addresses()
        if b_address.count() == 0:
            messages.success(self.request, "Please add a billing address before continuing.")
            return redirect("address_create")
        elif s_address.count() == 0:
            messages.success(self.request, "Please add a shipping address before continuing.")
            return redirect("address_create")
        return super(AddressSelectFormView, self).dispatch(*args, **kwargs)

    def get_addresses(self):
        user_checkout_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        b_address = UserAddress.objects.filter(
            user = user_checkout,
            type = 'billing'
        )
        s_address = UserAddress.objects.filter(
            user = user_checkout,
            type = 'shipping'
        )
        return b_address, s_address


    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)

        # feed the the form field with the data from databse.
        b_address, s_address = self.get_addresses()
        form.fields["billing_address"].quesryset = b_address
        form.fields["shipping_address"].quesryset = s_address
        return form

    def form_valid(self, form, *args, **kwargs):


        # Taking the billing and shipping address objects from the submitted form.
        billing_address = form.cleaned_data["billing_address"]
        shipping_address =form.cleaned_data["shipping_address"]

        # Feeding the address objects into the order instance coming from mixin
        new_order = self.get_order()
        new_order.billing_address = billing_address
        new_order.shipping_address = shipping_address
        new_order.save()
        # # Feeding the addressess objects id to the session dict.
        # self.request.session["billing_address_id"] = billing_address.id
        # self.request.session["shipping_address_id"] = shipping_address.id
        return super(AddressSelectFormView,self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse("checkout")
