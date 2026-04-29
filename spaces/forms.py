from django import forms
from .models import Space, SpaceImage


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['title', 'description', 'space_type', 'city', 'address',
                  'price_per_day', 'capacity', 'area_sqm', 'status']
        labels = {
            'title': 'اسم المساحة',
            'description': 'الوصف',
            'space_type': 'نوع المساحة',
            'city': 'المدينة',
            'address': 'العنوان',
            'price_per_day': 'السعر / اليوم (ريال)',
            'capacity': 'السعة (أشخاص)',
            'area_sqm': 'المساحة (متر مربع)',
            'status': 'الحالة',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SpaceImageForm(forms.ModelForm):
    class Meta:
        model = SpaceImage
        fields = ['image', 'is_main']
        labels = {
            'image': 'الصورة',
            'is_main': 'صورة رئيسية',
        }
