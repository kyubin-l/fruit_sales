from multiprocessing.sharedctypes import Value
from random import choices
from django import forms
from .models import City, Shop
from django.utils import timezone


def get_cities():
    return [
        (city.id, city.name) 
        for 
        city 
        in
        City.objects.all()
    ]

class CityForm(forms.Form):
    name = forms.CharField(label='City name', max_length=100)


class ShopForm(forms.Form):
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all())
    name = forms.CharField(label='Shop name', max_length=100)
    code = forms.CharField(label='Code', max_length=5)
    address = forms.CharField(label='Address', max_length=100)
    postcode = forms.CharField(label='Postcode', max_length=100)
    year_opened = forms.IntegerField(label='Year opened')


    # Overwriting the parents is_valid function
    def is_valid(self):
        valid = super(ShopForm, self).is_valid()
        if not valid:
            return valid

        year_opened = self.cleaned_data['year_opened']
        if (year_opened < 1850) or (year_opened > timezone.now().year):
            return False

        return True

