from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )
        labels = {
            'street_address1': 'Delivery address',
            'street_address2': 'Spare address',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels,
        and set autofocus on the first field.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Delivery Adress',
            'street_address2': 'Spare Adress',
            'county': 'County, State or Locality',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
        # Add star only once
            if field.required and ('*' not in (field.label or '')):
               field.label = f"{field.label}\u00A0*"