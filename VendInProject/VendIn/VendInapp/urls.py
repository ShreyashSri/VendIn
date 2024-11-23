from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('register/', views.VendorRegistrationView.as_view(), name='register'),
    path('api/register/', views.register_vendor_api, name='register_api'),
    path('list/', views.VendorListView.as_view(), name='vendor_list'),
    path('vendor/<int:pk>/', views.VendorDetailView.as_view(), name='vendor_detail'),
]