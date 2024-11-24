from django import forms
from .models import Vendor

class VendorRegistrationForm(forms.ModelForm):
    open_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time', 'class': 'form-control'}
        )
    )
    close_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time', 'class': 'form-control'}
        )
    )

    class Meta:
        model = Vendor
        fields = [
            'business_name',
            'owner_name',
            'phone',
            'address',
            'cuisine',
            'open_time',
            'close_time',
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your business name'
            }),
            'owner_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter owner name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your business address'
            }),
            'cuisine': forms.Select(attrs={
                'class': 'form-control'
            }),
        }