# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Vendor(models.Model):
    BUSINESS_TYPES = [
        ('food', 'Food'),
        ('retail', 'Retail'),
        ('services', 'Services'),
        ('crafts', 'Crafts'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES)
    location = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def _str_(self):
        return f"{self.name} - {self.business_type}"

class OperatingDay(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='operating_days')
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    is_open = models.BooleanField(default=True)

    class Meta:
        unique_together = ['vendor', 'day']

    def _str_(self):
        return f"{self.vendor.name}-{self.day}"