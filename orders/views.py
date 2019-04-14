from django.shortcuts import render, reverse
from django.views.generic.edit import FormView

from .forms import AddressSelectForm
from .models import UserAddress


# Create your views here.
class AddressSelectFormView(FormView):
    form_class = AddressSelectForm
    template_name = "orders/address_select.html"

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        # feed the the form field with the data from databse.
        form.fields["billing_address"].quesryset = UserAddress.objects.filter(
                user__email=self.request.user.email,
                type="billing"
        )
        form.fields["shipping_address"].quesryset = UserAddress.objects.filter(
                user__email=self.request.user.email,
                type="shipping"
        )
        return form

    def form_valid(self, form, *args, **kwargs):


        # Taking the billing and shipping address objects from the submitted form.
        billing_address = form.cleaned_data["billing_address"]
        shipping_address =form.cleaned_data["shipping_address"]

        # Feeding the addressess objects id to the session dict.
        self.request.session["billing_address_id"] = billing_address.id
        self.request.session["shipping_address_id"] = shipping_address.id
        return super(AddressSelectFormView,self).form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return reverse("checkout")
