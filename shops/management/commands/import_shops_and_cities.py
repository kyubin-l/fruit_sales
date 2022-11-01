from venv import create
from django.core.management.base import BaseCommand, CommandError
from shops.models import City, Shop

import pandas as pd


class Command(BaseCommand):
    help = 'Deletes all cities and shops from current database and \
        store new data from the excel sheet.'
    
    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **kwargs):
        # delete_data = input('You are about to delete all existing shops and cities, are you sure? (y/n) ')
        # if delete_data == 'y':
        if True:
            self.stdout.write('Continuing to delete')
            self.stdout.write(f'Deleting {Shop.objects.count()} Shop objects')
            Shop.objects.all().delete()
            self.stdout.write(f'Deleting {City.objects.count()} City objects')
            City.objects.all().delete()
            data = import_data()
            data.apply(create_objects, axis=1)
            self.stdout.write(f'Created {City.objects.count()} City objects')
            self.stdout.write(f'Created {Shop.objects.count()} Shop objects')
        

def import_data():
    raw_data = pd.read_excel('shops.xlsx')
    return raw_data


def create_objects(row):
    city, created = City.objects.get_or_create(name=row['Name'])
    shop = Shop(
        city=city,
        name=row['City'],
        code=row['Code'],
        address='tmp',
        postcode=row['Code'],
    )
    shop.save()
    