"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from carts.views import CartView, CartItemCountView, CheckoutView, CheckoutFinalView
from orders.views import AddressSelectFormView, AddressCreateView, OrderList, OrderDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    # For joins app
    path('join', include('joins.urls')),
    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # user app
    path('user/', include('users.urls')),
    # Product app
    path('product/', include('products.urls')),
    path('category/', include('products.urls_category')),
    # Cart app
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/count', CartItemCountView.as_view(), name='item_count'),
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/checkout/final/', CheckoutFinalView.as_view(), name='final_checkout'),
    # orders app
    path('order/address/', AddressSelectFormView.as_view(), name='address_select'),
    path('order/address/add/', AddressCreateView.as_view(), name='address_create'),
    path('order/list/', OrderList.as_view(), name='order_list'),
    path('order/detail/<int:pk>/', OrderDetail.as_view(), name='order_detail'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
