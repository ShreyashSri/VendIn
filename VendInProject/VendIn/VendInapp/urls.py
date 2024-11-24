from django.urls import path

from . import views
from .views import (
    VendorRegistrationView,
    VendorListView,
    VendorDetailView,
    register_vendor_api,
    HomeView, RegistrationSuccessView,
    CustomLoginView, EventsView, KarnatakaView,
    MangoMelaView, PeanutMelaView,
    rate_vendor,  # Import the RatingsView
    contact_us,  # Import the ContactView
    vendor_list,
    vendor_reviews
)
from django.views.generic import TemplateView

urlpatterns = [
    # Web UI URLs
    path('', HomeView.as_view(), name='home'),
    path('register/', VendorRegistrationView.as_view(), name='vendor_register'),
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('registration-success/', RegistrationSuccessView.as_view(), name='registration_success'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('events/', EventsView.as_view(), name='events'),
    path('karanataka/', KarnatakaView.as_view(), name='karnataka'),
    path('mango-mela/', MangoMelaView.as_view(), name='mango_mela'),
    path('peanut-mela/', PeanutMelaView.as_view(), name='peanut_mela'),
# Ratings page
    path('ratings/', rate_vendor, name='ratings'),  # Add the ratings page URL

    # Contact page
    path('contact/', views.contact_us, name='vendor_contact'),  # Add the contact page URL

    # API URLs
    path('api/register/', register_vendor_api, name='register_vendor_api'),

    path('showratings/', vendor_list, name='vendor_list_ratings'),
    path('rate-vendor/<int:vendor_id>/', views.rate_vendor, name='rate_vendor'),
    path('vendor-reviews/<int:vendor_id>/', views.vendor_reviews, name='vendor_reviews'),

    # API URLs
    path('api/register/', register_vendor_api, name='register_vendor_api'),
]