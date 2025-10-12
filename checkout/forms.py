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
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # autofocus on first field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            # Country usually uses a select; skip placeholder to avoid odd UX
            if field_name != 'country':
                placeholder = placeholders.get(field_name, '')
                if field.required and placeholder:
                    placeholder = f'{placeholder} *'
                if placeholder:
                    field.widget.attrs['placeholder'] = placeholder

            field.widget.attrs['class'] = 'stripe-style-input'
            field.label = False