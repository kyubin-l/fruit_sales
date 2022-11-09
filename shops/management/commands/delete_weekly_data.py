from django.core.management.base import BaseCommand
import shops.models as models

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        delete_data = input('You are about to delete all existing weekly data, are you sure? (YES/Y to confirm, any other key to quit)')
        if delete_data.lower() not in ['y', 'yes']:
            pass
        else:
            models.WeeklyOverhead.objects.all().delete()
            models.WeeklySale.objects.all().delete()
            models.WeeklyShopSummary.objects.all().delete()
            models.Fruit.objects.all().delete()