from django.db import models
from django.utils import timezone
from django.conf import settings
import os
# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Shop(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    address = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    year_opened = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.code}'


class Fruit(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f'{self.name}'


class WeeklyShopSummary(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    upload = models.FileField(upload_to='uploads')

    def __str__(self) -> str:
        return f'{self.shop}, {self.date}'

    def filename(self):
        return settings.MEDIA_ROOT / self.upload.name


class WeeklySale(models.Model):
    weekly_shop_summary = models.ForeignKey(
        WeeklyShopSummary, 
        on_delete=models.PROTECT, 
        null=True
        )
    fruit = models.ForeignKey(Fruit, on_delete=models.PROTECT)

    units_bought = models.IntegerField(null=True, blank=True)
    cost_per_unit = models.FloatField(null=True, blank=True)
    units_sold = models.IntegerField(null=True, blank=True)
    price_per_unit = models.FloatField(null=True, blank=True)
    units_wastage = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.weekly_shop_summary}, {self.fruit}'
    

class WeeklyOverhead(models.Model):
    overhead_type = (
        ('Personnel cost', 'personnel cost'),
        ('Premises cost', 'premises cost'),
        ('Other overheads', 'other overheads'),
    )
    weekly_shop_summary = models.ForeignKey(
        WeeklyShopSummary, 
        on_delete=models.PROTECT
        )
    overhead = models.CharField(max_length=30, choices=overhead_type)
    amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.weekly_shop_summary}, {self.overhead}, {self.amount}'

    