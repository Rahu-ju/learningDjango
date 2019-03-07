from django.urls import path
from django.views.generic import TemplateView

from .views import join_view, share_view

urlpatterns = [
    path('', join_view, name='join_view'),
    path('join', TemplateView.as_view(template_name='joins/join.html'), name='join'),
    path('share/<str:ref_id>', share_view, name='share'),
]
