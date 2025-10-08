from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'phone_number', 'address_line_delivery',
            'address_line_living', 'city', 'postal_code', 'country'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_living': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'address_line_delivery': 'Delivery Address',
            'address_line_living': 'Living Address',
            'city': 'City',
            'postal_code': 'Postal Code',
            'country': 'Country',
        }