from django.urls import path
from .views import (
    VendorRegistrationView,
    VendorListView,
    VendorDetailView,
    register_vendor_api,
    HomeView
)
from django.views.generic import TemplateView

urlpatterns = [
    # Web UI URLs
    path('', HomeView.as_view(), name='home'),
    path('', VendorListView.as_view(), name='vendor_list'),  # Home page
    path('register/', VendorRegistrationView.as_view(), name='vendor_register'),
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('registration-success/',
         TemplateView.as_view(template_name='VendInapp/registration_success.html'),
         name='registration_success'),

    # API URLs
    path('api/register/', register_vendor_api, name='register_vendor_api'),
]