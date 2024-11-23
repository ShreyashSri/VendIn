from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Vendor, OperatingDay
from .forms import VendorRegistrationForm
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'VendInapp/base.html'

class VendorRegistrationView(CreateView):
    model = Vendor
    form_class = VendorRegistrationForm
    template_name = 'VendInapp/registration.html'
    success_url = reverse_lazy('registration_success')  # Updated to use reverse_lazy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operating_days'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # Handle operating days
        days_data = self.request.POST.getlist('operating_days')
        for day in days_data:
            OperatingDay.objects.create(vendor=self.object, day=day)
        messages.success(self.request, 'Registration successful! Your application is under review.')
        return response

class VendorListView(ListView):
    model = Vendor
    template_name = 'VendInapp/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().prefetch_related('operating_days')

class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'VendInapp/vendor_detail.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('operating_days')

@csrf_exempt
def register_vendor_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vendor = Vendor.objects.create(
                name=data['name'],
                phone=data['phone'],
                business_type=data['business_type'],
                location=data['location'],
                start_time=data['start_time'],
                end_time=data['end_time']
            )

            for day in data.get('operating_days', []):
                OperatingDay.objects.create(vendor=vendor, day=day.lower())

            return JsonResponse({
                'status': 'success',
                'message': 'Vendor registered successfully',
                'vendor_id': vendor.id
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'message': 'Method not allowed'}, status=405)