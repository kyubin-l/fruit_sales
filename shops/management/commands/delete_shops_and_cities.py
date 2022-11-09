from django.core.management.base import BaseCommand
import shops.models as models

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        delete_data  = input('You are about to delete all existing shops and cities, are you sure? (YES/Y to confirm, any other key to quit) ')
        if delete_data.lower() not in ['y', 'yes']:
            pass
        else:
            models.Shop.objects.all().delete()
            models.City.objects.all().delete()
            