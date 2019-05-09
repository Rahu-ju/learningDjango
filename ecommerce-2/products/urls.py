from django.urls import path

from .views import ProductDetailView, product_detail_view, ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<pk>', ProductDetailView.as_view(), name='product_detail'),
    path('fbv/<id>', product_detail_view, name='product_detail'),
]
