from django import forms
import shops.models as models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

import re

class CityForm(forms.ModelForm):
    class Meta:
        model = models.City
        fields = ['name']


class ShopForm(forms.ModelForm):
    class Meta:
        model = models.Shop
        fields = ['city', 'name', 'code', 'address', 'postcode', 'year_opened']

    def is_valid(self):
        if not super(ShopForm, self).is_valid():
            return False

        if not (1850 < self.cleaned_data['year_opened'] < timezone.now().year):
            return False

        return True


class WeeklySummaryForm(forms.ModelForm):
    class Meta:
        model = models.WeeklyShopSummary
        fields = ['upload']

    # validation function
    def clean_upload(self):
        # Checking if file type and format is corrext
        name = self.cleaned_data['upload'].name
        if '.xlsx' not in name:
            raise ValidationError('Invalid file type - data must be of type .xlsx')
        name = name.replace('.xlsx', '')
        r = re.compile('.{4}-.{2}-.{2}-.{4}')
        if len(name) != 16 or (not r.match(name)):
            raise ValidationError('File name must be of format \'yyyy-mm-dd-shopcode\'')
        date, shop_code = name.rsplit('-', 1)
        try:
            date_object = timezone.make_aware(datetime.strptime(date, '%Y-%m-%d'))
        except ValueError:
            raise ValidationError('Date not in correct format: \'yyyy-mm-dd\'')
        try:
            shop = models.Shop.objects.get(code=shop_code)
        except ObjectDoesNotExist:
            raise ValidationError('Incorrect shop code or or data already exists')
        # Checking if given date is correct
        if date_object.year < shop.year_opened:
            raise ValidationError('Invalid year - must be later than shop opening date')
        if date_object.weekday() is not 0:
            raise ValidationError('Day is not a Monday')
        if date_object > timezone.now():
            raise ValidationError('Date must be an earlier date than today')

        return self.cleaned_data['upload']


