from django.urls import path

from .views import CategorylistView, CategoryDetailView


urlpatterns = [
    path('', CategorylistView.as_view(), name='categories'),
    path('<slug>/', CategoryDetailView.as_view(), name='category_detail'),
]
