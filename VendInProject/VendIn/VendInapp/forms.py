# vendors/forms.py
from django import forms
from .models import Vendor

class VendorRegistrationForm(forms.ModelForm):
    operating_days = forms.MultipleChoiceField(
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Vendor
        fields = ['name', 'phone', 'business_type', 'location', 'start_time','end_time']
