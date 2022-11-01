from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.name


class Shop(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    year_opened = models.IntegerField(default=0)
