from django import forms
from shops import models
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
        # Checking if file name matches given format pf yyyy-mm-dd-xxxx
        r = re.compile('.{4}-.{2}-.{2}-.{4}')
        if len(name) != 16 or (not r.match(name)):
            raise ValidationError('File name must be of format \'yyyy-mm-dd-shopcode\'')
        raw_date, shop_code = name.rsplit('-', 1)
        try:
            data = timezone.make_aware(datetime.strptime(raw_date, '%Y-%m-%d'))
        except ValueError:
            raise ValidationError('Date not in correct format: \'yyyy-mm-dd\'')
        if not models.Shop.objects.filter(code=shop_code).exists():
            raise ValidationError('Incorrect shop code or or data already exists')
        shop = models.Shop.objects.get(code=shop_code)
        # Checking if given date is correct
        if data.year < shop.year_opened:
            raise ValidationError('Invalid year - must be later than shop opening date')
        if data.weekday() is not 0:
            raise ValidationError('Day is not a Monday')
        if data > timezone.now():
            raise ValidationError('Date must be an earlier date than today')

        return self.cleaned_data['upload']


