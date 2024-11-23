# VendInapp/models.py
from django.db import models
from django.core.validators import RegexValidator

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    business_type = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

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

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='operating_days'
    )
    day = models.CharField(
        max_length=10,
        choices=DAYS_OF_WEEK
    )

    class Meta:
        unique_together = ['vendor', 'day']

    def __str__(self):
        return f"{self.vendor.name} - {self.day}"