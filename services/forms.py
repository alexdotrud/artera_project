from django import forms
from .models import ArtworkRequest, Offer

class ArtworkRequestForm(forms.ModelForm):
    class Meta:
        model = ArtworkRequest
        fields = ["title", "description", "ref_image", "budget_cents"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "budget_cents": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["full_name", "email", "phone_number", "title", "description", "category", "sample_image"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
        }