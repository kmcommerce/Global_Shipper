from django import forms
from .models import Order


class FCLQuoteForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'origin_region',
            'destination_country',
        ]

        widgets = {
            'origin_region': forms.Select(attrs={'class': 'form-control'}),
            'destination_country': forms.Select(attrs={'class': 'form-control'}),
        }
