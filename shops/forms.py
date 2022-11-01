from random import choices
from django import forms
from .models import City, Shop


def get_cities():
    return [
        (city.id, city.name) 
        for 
        city 
        in
        City.objects.all()
    ]

class CityForm(forms.Form):
    city_name = forms.CharField(label='City name', max_length=100)


class ShopForm(forms.Form):
    city = forms.ChoiceField(label='City', choices=get_cities)
    name = forms.CharField(label='Shop name', max_length=100)
    code = forms.CharField(label='Code', max_length=5)
    address = forms.CharField(label='Address', max_length=100)
    postcode = forms.CharField(label='Postcode', max_length=100)
    year_opened = forms.IntegerField(label='Year opened')

