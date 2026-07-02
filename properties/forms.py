from django import forms
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'listing_type', 'property_type',
            'city', 'district', 'address',
            'price', 'area', 'bedrooms', 'bathrooms', 'floor', 'finishing',
            'has_garage', 'has_garden', 'has_pool', 'has_elevator', 'has_security',
            'latitude', 'longitude',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: شقة فاخرة 3 غرف في القاهرة الجديدة'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'اكتب وصفاً تفصيلياً للعقار...'
            }),
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'العنوان التفصيلي'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'المساحة بالمتر المربع'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الدور'
            }),
            'finishing': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }