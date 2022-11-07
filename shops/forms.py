from django import forms
from .models import City, Shop
from django.utils import timezone


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['city', 'name', 'code', 'address', 'postcode', 'year_opened']


    def is_valid(self):
        if not super(ShopForm, self).is_valid():
            return False

        if not (1850 < self.cleaned_data['year_opened'] < timezone.now().year):
            return False

        return True


