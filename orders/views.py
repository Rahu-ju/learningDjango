from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import AddressSelectForm


# Create your views here.
class AddressSelectFormView(FormView):
    form_class = AddressSelectForm
    template_name = "orders/address_select.html"
