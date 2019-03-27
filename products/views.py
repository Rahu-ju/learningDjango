from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.utils import timezone
from django.db.models import Q

from .models import Product, Category

# Create your views here.
class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = self.model.objects.filter(
                    Q(title__icontains=query) |
                    Q(descripttion__icontains=query)
                )
            try:
                qs2 = self.model.objects.filter(
                        Q(price=query)
                )
                # make sure both are same models object
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs


class ProductDetailView(DetailView):
    model = Product
    # default template name 'appname/modelname_detail.html'

# example of detail function base view
def product_detail_view(request, id):
    product_instance = get_object_or_404(Product, id=id)
    # Instead of using the get_object_or_404 you can use the following code
    # try:
    #     product_instance = Product.objects.get(id=id)
    # except Product.DoesNotExist:
    #     raise Http404
    # except:
    #     raise Http404

    template = 'products/product_detail.html'
    context = {
        'object': product_instance
    }

    return render(request, template, context)


# Category list view
class CategorylistView(ListView):
    model = Category
    template_name = 'products/product_list.html'

class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        productset = obj.product_set.all()
        product_category = obj.product_category.all()
        products = (productset | product_category).distinct()
        context['products'] = products
        return context
