from django.core.management.base import BaseCommand, CommandError
import shops.models as models
from django.utils import timezone
from datetime import datetime

import pandas as pd



def import_data(file_path: str):
    data = pd.read_excel(file_path, sheet_name=None)
    fruit_data, overhead_data = data['by fruit'], data['overheads']
    date_code = str(file_path).split('/')[-1]
    date, shop_code = date_code.rsplit('-', 1)
    shop_code = shop_code.replace('.xlsx', '')
    date_object = timezone.make_aware(datetime.strptime(date, '%Y-%m-%d'))

    return fruit_data, overhead_data, shop_code, date_object


def create_sale_objects(row, weekly_shop_summary):
    fruit, _ = models.Fruit.objects.get_or_create(name=row['fruit'])

    new_sale = models.WeeklySale(
        weekly_shop_summary=weekly_shop_summary,
        fruit = fruit,
        units_bought = row['units bought'],
        cost_per_unit=row['cost per unit'],
        units_sold=row['units sold'],
        price_per_unit=row['price per unit'],
        units_wastage=row['units wastage'],
    )    
    new_sale.save()


def create_overhead_objects(row, weekly_shop_summary):
    # TODO: change list of choices to TextChoice class
    overhead_types = [choice[0] for choice in models.WeeklyOverhead.overhead.field.choices]
    for overhead in overhead_types:
        new_weekly_overhead = models.WeeklyOverhead(
            weekly_shop_summary=weekly_shop_summary,
            overhead=overhead,
            amount=row[overhead]
        )
        new_weekly_overhead.save()