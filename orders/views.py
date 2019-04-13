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

    def form_valid(self, *args, **kwargs):
        form = super(AddressSelectFormView,self).form_valid(*args, **kwargs)
        print(form)
        return form

    def get_success_url(self):
        return reverse("checkout")
