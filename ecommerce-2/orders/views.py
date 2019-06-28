from django.shortcuts import render, reverse, redirect
from django.http import Http404
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages

from .forms import AddressSelectForm, AddressCreateForm
from .models import UserAddress, UserCheckout, Order
from .mixin import CartOrderMixin, LoginRequiredMixin


# Create your views here.
class OrderDetail(DetailView):
    model = Order

    def dispatch(self, request, *args, **kwargs):
        """
        if user didn't sign in or continue as guest then it raise 404 page with the following
        message. Other wise user can see the detail page.
        """
        try:
            user_checkout_id = self.request.session.get("user_checkout_id")
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if not user_checkout:
                user_checkout = UserCheckout.objects.get(user=request.user)
        except:
            user_checkout = None

        obj = self.get_object()
        if obj.user == user_checkout or user_checkout != None:
            return super(OrderDetail, self).dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "You need to continue as guest or sign in to see your previous order details..")
            raise Http404



class OrderList(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()

    def get_queryset(self):
        user_checkout_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        return super(OrderList, self).get_queryset().filter(user=user_checkout)


class AddressCreateView(CartOrderMixin, CreateView):
    form_class = AddressCreateForm
    template_name = "orders/address_create.html"
    success_url = "/order/address/" # To the AddressSelectFormView

    # def get_checkout_user(self):
    #     user_checkout_id = self.request.session.get("user_checkout_id")
    #     user_checkout = UserCheckout.objects.get(id=user_checkout_id)
    #     return user_checkout

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
        # user_checkout_id = self.request.session.get("user_checkout_id")
        # user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        b_address = UserAddress.objects.filter(
            user = self.get_checkout_user(),
            type = 'billing'
        )
        s_address = UserAddress.objects.filter(
            user = self.get_checkout_user(),
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
