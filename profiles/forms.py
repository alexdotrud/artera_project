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

class ProfileSignupForm(SignupForm):
    full_name = forms.CharField(max_length=100, required=False, label="Full name")
    phone_number = forms.CharField(max_length=20, required=False, label="Phone number")
    address_line_delivery = forms.CharField(max_length=255, required=False, label="Delivery address")
    address_line_living = forms.CharField(max_length=255, required=False, label="Living address")
    city = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=20, required=False, label="Postal code")
    country = forms.CharField(max_length=100, required=False)

    def save(self, request):
        # create the user first (Allauth handles username/email/password)
        user = super().save(request)

        # make sure a profile exists, then persist extra fields
        profile, _ = Profile.objects.get_or_create(user=user)
        cd = self.cleaned_data
        profile.full_name = cd.get("full_name", "")
        profile.phone_number = cd.get("phone_number", "")
        profile.address_line_delivery = cd.get("address_line_delivery", "")
        profile.address_line_living = cd.get("address_line_living", "")
        profile.city = cd.get("city", "")
        profile.postal_code = cd.get("postal_code", "")
        profile.country = cd.get("country", "")
        profile.save()

        return user