from django import forms
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'listing_type', 'property_type',
            'city', 'district', 'address',
            'price', 'area', 'bedrooms', 'bathrooms', 'floor', 'finishing',
            'phone', 'whatsapp',
            'has_garage', 'has_garden', 'has_pool', 'has_elevator', 'has_security',
            'latitude', 'longitude',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'finishing': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
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
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01000000000'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01000000000'
            }),
            'has_garage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_garden': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_elevator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_security': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # تحديد التسمية الافتراضية للخيارات المنسدلة لضمان ظهور التلميح للعميل
        if 'property_type' in self.fields:
            self.fields['property_type'].empty_label = "اختر نوع العقار"
        if 'city' in self.fields:
            self.fields['city'].empty_label = "اختر المدينة"
        if 'district' in self.fields:
            self.fields['district'].empty_label = "اختر الحي"
        if 'finishing' in self.fields:
            self.fields['finishing'].empty_label = "اختر نوع التشطيب"

        # ملء بيانات التواصل تلقائياً إن وجدت للمستخدم
        if user and not self.initial.get('phone'):
            user_phone = getattr(user, 'phone', '') or getattr(getattr(user, 'profile', None), 'phone', '')
            if user_phone:
                if 'phone' in self.fields:
                    self.fields['phone'].initial = user_phone
                if 'whatsapp' in self.fields:
                    self.fields['whatsapp'].initial = user_phone


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }