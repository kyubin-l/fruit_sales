from django.contrib import admin
from shops import models

admin.site.register(models.City)
admin.site.register(models.Shop)
admin.site.register(models.Fruit)
admin.site.register(models.WeeklySale)
admin.site.register(models.WeeklyShopSummary)
admin.site.register(models.WeeklyOverhead)


# Register your models here.
