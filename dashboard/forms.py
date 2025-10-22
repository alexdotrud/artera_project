from django import forms
from shop.models import Artwork

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = [
            "name", "price", "sku", "category", "description",
            "image", "image_url", "is_active"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
        }

class StatusForm(forms.Form):
    status = forms.ChoiceField(choices=[
        ("new", "New"),
        ("in_review","In review"),
        ("accepted","Accepted"),
        ("rejected","Rejected"),
    ])
