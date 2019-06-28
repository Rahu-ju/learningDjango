from django.shortcuts import render
from django.http import Http404

from .models import Product

# Create your views here.

def home(request):
    template = 'home.html'
    context = {}
    return render(request, template, context)


def category(request):
    template = 'category/category.html'

    # retrive products from the database
    try:
        products = Product.objects.all()
        context = {'products': products }
        return render(request, template, context)
    except:
        raise Http404
    
def detail(request, slug):
    template = 'detail.html'

    # retrive the product(using slug) from the database
    try:
        product = Product.objects.get(slug=slug)
        context = {'product': product }
        return render(request, template, context)
    except:
        raise Http404
