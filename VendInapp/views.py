from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
import json

from .models import Vendor, OperatingDay, Event, Review
from .forms import VendorRegistrationForm
from django.db.models import Avg  # To calculate average ratings


class HomeView(TemplateView):
    template_name = 'VendInapp/base.html'


class VendorRegistrationView(CreateView):
    model = Vendor
    form_class = VendorRegistrationForm
    template_name = 'VendInapp/registration.html'
    success_url = reverse_lazy('registration_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'] = [
            'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday'
        ]
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            vendor = form.save()

            # Handle operating days
            operating_days = request.POST.getlist('operating_days')
            for day in operating_days:
                OperatingDay.objects.create(
                    vendor=vendor,
                    day=day.capitalize()
                )

            messages.success(request, 'Registration successful! Your application is under review.')
            return redirect('registration_success')
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return self.form_invalid(form)


class VendorListView(ListView):
    model = Vendor
    template_name = 'VendInapp/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10

    def get_queryset(self):
        return Vendor.objects.prefetch_related('operating_days')


class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'VendInapp/vendor_detail.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.prefetch_related('operating_days')


@csrf_exempt
def register_vendor_api(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)

            # Create Vendor instance
            vendor = Vendor.objects.create(
                business_name=data.get('business_name'),  # Ensure this field exists in the model
                owner_name=data.get('owner_name'),  # Ensure this field exists in the model
                phone=data.get('phone'),  # Ensure this field exists in the model
                address=data.get('address'),  # Ensure this field exists in the model
                cuisine=data.get('cuisine'),  # Ensure this field exists in the model
                open_time=data.get('open_time'),  # Ensure this field exists in the model
                close_time=data.get('close_time')  # Ensure this field exists in the model
            )

            # Create Operating Days
            operating_days = data.get('operating_days', [])
            for day in operating_days:
                OperatingDay.objects.create(
                    vendor=vendor,
                    day=day.capitalize()
                )

            return JsonResponse({
                'status': 'success',
                'message': 'Vendor registered successfully',
                'vendor_id': vendor.id
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'message': 'Method not allowed'
    }, status=405)

# Optional: Success page view
class RegistrationSuccessView(TemplateView):
    template_name = 'VendInapp/registration_success.html'


class CustomLoginView(LoginView):
    template_name = 'VendInapp/login_page.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('vendor_list')  # Redirect to vendor list after login

    def get_success_url(self):
        return self.success_url

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)


class EventsView(ListView):
    model = Event
    template_name = 'VendInapp/local_event.html'  # Changed from local_event.html to match the template
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.all().order_by('date')


class KarnatakaView(TemplateView):
    template_name = 'VendInapp/karanataka.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Karunadu Swada - Karnataka Food Festival'
        return context

    def post(self, request, *args, **kwargs):
        # Handle review submission
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        # Add your logic to save the review
        return JsonResponse({'status': 'success', 'message': 'Review submitted successfully'})


class MangoMelaView(TemplateView):
    template_name = 'VendInapp/mango_mela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mango Mela 2024'
        return context
class PeanutMelaView(TemplateView):
    template_name = 'VendInapp/peanut _mela.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Peanut Mela 2024'
        return context
# Contact Page View
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Implement logic to handle contact form submission (e.g., send an email or save to the database)
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
    return render(request, 'VendInapp/vendor_contact.html')

# Rating Page View
def rate_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        try:
            rating = float(rating)
            # Save rating to the database (assuming a `rating` field exists in the Vendor model or a related Rating model)
            vendor.ratings.create(rating=rating)  # Assuming a related `ratings` model
            messages.success(request, 'Thank you for your rating!')
        except ValueError:
            messages.error(request, 'Invalid rating value. Please enter a valid number.')
    # Calculate the average rating for the vendor
    average_rating = vendor.ratings.aggregate(Avg('rating'))['rating__avg']  # Assuming a `ratings` model
    context = {'vendor': vendor, 'average_rating': average_rating}
    return render(request, 'VendInapp/ratings.html', context)
def vendor_list(request):
    vendors = Vendor.objects.all()
    star_range = range(1,6)
    search_query = request.GET.get('q')
    if search_query:
        vendors = vendors.filter(name__icontains=search_query)
    return render(request, 'VendInapp/ratings_list.html', {'vendors': vendors,'star_range': star_range})

def rate_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        Review.objects.create(vendor=vendor, rating=rating, review_text=review_text)
        vendor.rating = vendor.reviews.aggregate(Avg('rating'))['rating__avg']
        vendor.save()
        return redirect('vendor_list')
    return render(request, 'VendInapp/ratings.html', {'vendor': vendor})

def vendor_reviews(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    # reviews = vendor.reviews.all()
    return render(request, 'VendInapp/vendor_reviews.html', {'vendor': vendor})