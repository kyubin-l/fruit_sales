# Generated by Django 4.1.2 on 2022-11-01 11:07

from django.db import migrations, models
import django.db.models.deletion


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
                ('code', models.CharField(blank=True, max_length=5, null=True)),
                ('address', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=100)),
                ('year_opened', models.IntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shops.city')),
            ],
        ),
    ]
