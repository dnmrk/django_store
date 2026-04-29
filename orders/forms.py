from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address', 'city', 'postal_code']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan dela Cruz'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'juan@email.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '123 Rizal St, Barangay...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manila'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1000'}),
        }