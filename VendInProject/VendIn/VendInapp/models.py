from django.db import models
from django.core.validators import RegexValidator


class Vendor(models.Model):
    CUISINE_CHOICES = [
        ('asian', 'Asian'),
        ('mexican', 'Mexican'),
        ('italian', 'Italian'),
        ('american', 'American'),
        ('indian', 'Indian'),
        ('other', 'Other'),
    ]

    business_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)

    address = models.TextField()
    cuisine = models.CharField(max_length=20, choices=CUISINE_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name


class OperatingDay(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name='operating_days'
    )
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    class Meta:
        unique_together = ['vendor', 'day']

    def __str__(self):
        return f"{self.vendor.business_name} - {self.day}"


class Event(models.Model):
    EVENT_TYPES = [
        ('FOOD-FESTIVAL', 'Food Festival'),
        ('MARKET', 'Market'),
        ('POPUP', 'Pop-up')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=EVENT_TYPES)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.date}"
class EventReview(models.Model):
    event_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()
    user_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Rating(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='ratings', on_delete=models.CASCADE)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.rating}"


# Contact model for "Contact Us" form (optional)
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.email}"


class Review(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reviews')
    # Rating can be kept as IntegerField for simplicity
    rating = models.IntegerField(default=0)
    review_text = models.TextField()

    def __str__(self):
        return f"Review for {self.vendor.name} - Rating: {self.rating}"