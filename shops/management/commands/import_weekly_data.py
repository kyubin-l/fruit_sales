from django.core.management.base import BaseCommand, CommandError
import shops.models as models
import pathlib
import re
from django.utils import timezone
from datetime import datetime
import shops.utilities.import_helpers as import_helpers
from django.core.files import File
import os
from pathlib import Path

import pandas as pd


class Command(BaseCommand):
    help = 'Deletes all previous weekly shop data from current database and \
        store new data from the excel sheets'

    
    def add_arguments(selef, parser):
        pass


    def handle(self, *args, **kwargs):
        delete_data = input('You are about to delete all existing weekly data, \
            are you sure? (YES/Y to confirm, any other key to quit)')
        if delete_data.lower() not in ['y', 'yes']:
            pass
        else:
            delete_all_objects()
            data_path = './data/weekly_shop_'
            for weekly_data in pathlib.Path(data_path).iterdir():
                fruit_data, overhead_data, shop_code, date_object \
                    = import_helpers.import_data(weekly_data)
                shop = models.Shop.objects.get(code=shop_code)
                weekly_shop_summary = models.WeeklyShopSummary(
                    shop=shop, 
                    date=date_object
                    )
                weekly_shop_summary.upload = File(
                    file=open(weekly_data, 'rb'),
                     name=Path(weekly_data).name
                     )
                weekly_shop_summary.save()
                fruit_data.apply(
                    import_helpers.create_sale_objects, 
                    axis=1, 
                    weekly_shop_summary=weekly_shop_summary
                    )
                overhead_data.apply(
                    import_helpers.create_overhead_objects, 
                    axis=1, 
                    weekly_shop_summary=weekly_shop_summary
                    )


def delete_all_objects():
    models.WeeklyOverhead.objects.all().delete()
    models.WeeklySale.objects.all().delete()
    models.WeeklyShopSummary.objects.all().delete()
    models.Fruit.objects.all().delete()




