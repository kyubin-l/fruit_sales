from django.core.management.base import BaseCommand, CommandError
import shops.models as models
import pathlib
import re
from django.utils import timezone
from datetime import datetime

import pandas as pd


class Command(BaseCommand):
    help = 'Deletes all previous weekly shop data from current database and \
        store new data from the excel sheets'

    
    def add_arguments(selef, parser):
        pass


    def handle(self, *args, **kwargs):
        delete_data = input('You are about to delete all existing weekly data, are you sure? (YES/Y to confirm, any other key to quit)')
        if delete_data.lower() in ['y', 'yes']:
            delete_all_objects()
            data_path = './data/weekly_shop_data'
            for weekly_data in pathlib.Path(data_path).iterdir():
                fruit_data, overhead_data, shop_code, date_object = import_data(weekly_data)
                shop = models.Shop.objects.get(code=shop_code)
                weekly_shop_summary = models.WeeklyShopSummary(shop=shop, date=date_object)
                weekly_shop_summary.save()
                fruit_data.apply(create_sale_objects, axis=1, weekly_shop_summary=weekly_shop_summary)
                overhead_data.apply(create_overhead_objects, axis=1, weekly_shop_summary=weekly_shop_summary)


def delete_all_objects():
    models.WeeklyOverhead.objects.all().delete()
    models.WeeklySale.objects.all().delete()
    models.WeeklyShopSummary.objects.all().delete()
    models.Fruit.objects.all().delete()


def import_data(file_path: str):
    data = pd.read_excel(file_path, sheet_name=None)
    fruit_data, overhead_data = data['by fruit'], data['overheads']
    date_code = str(file_path).split('/')[-1]
    date, shop_code = date_code.rsplit('-', 1)
    shop_code = shop_code.replace('.xlsx', '')
    print(date, shop_code)
    date_object = timezone.make_aware(datetime.strptime(date, '%Y-%m-%d'))

    return fruit_data, overhead_data, shop_code, date_object


def create_sale_objects(row, weekly_shop_summary):
    fruit, created = models.Fruit.objects.get_or_create(name=row['fruit'])

    new_sale = models.WeeklySale(
        shop_date=weekly_shop_summary,
        fruit = fruit,
        units_bought = row['units bought'],
        cost_per_unit=row['cost per unit'],
        units_sold=row['units sold'],
        price_per_unit=row['price per unit'],
        units_wastage=row['units wastage'],
    )    
    new_sale.save()


def create_overhead_objects(row, weekly_shop_summary):
    overhead_types = [choice[0] for choice in models.WeeklyOverhead.overhead.field.choices]
    for overhead in overhead_types:
        new_weekly_overhead = models.WeeklyOverhead(
            shop_date=weekly_shop_summary,
            overhead=overhead,
            amount=row[overhead]
        )
        new_weekly_overhead.save()

