# Generated by Django 4.1.2 on 2022-11-08 14:47

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0006_alter_weeklyshopsummary_shop_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyshopsummary',
            name='upload',
            field=models.FileField(upload_to=pathlib.PurePosixPath('/mnt/c/Users/klee/OneDrive - Dare International LTD/Documents/workspace/training/django/fruit_sales/data/uploads')),
        ),
    ]
