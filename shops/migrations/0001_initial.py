# Generated by Django 4.1.2 on 2022-11-03 12:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=5)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('postcode', models.CharField(blank=True, max_length=100, null=True)),
                ('year_opened', models.IntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.city')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklySale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fruit', models.CharField(max_length=100)),
                ('units_bought', models.IntegerField(default=0)),
                ('cost_per_unit', models.IntegerField(default=0)),
                ('units_sold', models.IntegerField(default=0)),
                ('price_per_unit', models.IntegerField(default=0)),
                ('units_wastage', models.IntegerField(default=0)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
        ),
    ]
