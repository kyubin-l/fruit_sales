from django.shortcuts import render
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

import shops.models as models
import shops.forms as forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

import re
import pandas as pd
import shops.utilities.import_helpers as import_helpers


class HomeView(generic.base.TemplateView):
    template_name = 'shops/home.html'


class CityView(generic.ListView):
    template_name = 'shops/city.html'
    context_object_name = 'all_cities'

    def get_queryset(self):
        return models.City.objects.all()


class CityDetailView(generic.DetailView):
    model = models.City
    template_name = 'shops/citydetail.html'


class ShopView(generic.ListView):
    template_name = 'shops/shop.html'
    context_object_name = 'all_shops'

    def get_queryset(self):
        return models.Shop.objects.all()


class ShopDetailView(generic.DetailView):
    model = models.Shop
    template_name = 'shops/shopdetail.html'


class CityCreateView(generic.CreateView):
    model = models.City
    template_name = 'shops/cityform.html'
    fields = 'name',
    success_url = reverse_lazy('city_list')
    

class ShopCreateView(generic.CreateView):
    form_class = forms.ShopForm
    template_name = 'shops/shopform.html'
    success_url = reverse_lazy('shop_list')


class CityDeleteView(generic.DeleteView):
    model = models.City
    success_url = reverse_lazy('city_list')


class CityUpdateView(generic.UpdateView):
    model = models.City
    fields = ['name']
    template_name = 'shops/city_update_form.html'
    success_url = reverse_lazy('city_list')
    

class ShopDeleteView(generic.DeleteView):
    model = models.Shop
    success_url = reverse_lazy('shop_list')


class ShopUpdateView(generic.UpdateView):
    model = models.Shop
    form_class = forms.ShopForm
    template_name = 'shops/shop_update_form.html'
    success_url = reverse_lazy('shop_list')


class WeeklyImportYearView(generic.TemplateView):
    template_name = 'shops/weekly_import.html'

    def get_context_data(self, *args, **kwargs):
        dates = models.WeeklyShopSummary.objects.all().values_list('date', flat=True).distinct()
        years = set([date.year for date in dates])
        return {'years': years}


class WeeklyImportMonthView(generic.TemplateView):
    template_name = 'shops/weekly_import_monthview.html'

    def get_context_data(self, *args, **kwargs):
        dates = models.WeeklyShopSummary.objects.filter(
            date__year=kwargs['year']
            ).values_list(
                'date', flat=True
                ).distinct()
        dates_uniquemonths = []
        for date in dates:
            if date.month not in [date_unique.month for date_unique in  dates_uniquemonths]:
                dates_uniquemonths.append(date)
        return {'months': dates_uniquemonths, 'year': kwargs['year']}


class WeeklyImportWeekView(generic.TemplateView):
    template_name = 'shops/weekly_import_weekview.html'

    def get_context_data(self, *args, **kwargs):
        dates = models.WeeklyShopSummary.objects.filter(
            date__year=kwargs['year'],  
            date__month=kwargs['month'],
            ).values_list(
                'date', flat=True
                ).distinct()
        dates_uniqueweek = []
        for date in dates:
            if date.day not in [date_unique.day for date_unique in  dates_uniqueweek]:
                dates_uniqueweek.append(date)
        
        return {'weeks': dates_uniqueweek, 'year': kwargs['year'], 'month': kwargs['month']}


class WeeklyImportShopView(generic.TemplateView):
    template_name = 'shops/weekly_import_shopview.html'

    def get_context_data(self, *args, **kwargs):
        weekly_summaries = models.WeeklyShopSummary.objects.filter(
            date__year=kwargs['year'],  
            date__month=kwargs['month'],
            date__day=kwargs['week'],
            )
        
        return {'weekly_summaries': weekly_summaries, 'year': kwargs['year'], 'month': kwargs['month'], 'week':kwargs['week']}


class WeeklyImportShopDetail(generic.TemplateView):
    template_name = 'shops/weekly_import_shopdetail.html'
    
    def get_context_data(self, *args, **kwargs):
        weekly_shop_summary = models.WeeklyShopSummary.objects.get(
            shop=models.Shop.objects.get(code=kwargs['shopcode']),
                date__year=kwargs['year'],  
                date__month=kwargs['month'],
                date__day=kwargs['week'],
            )

        weekly_sales = models.WeeklySale.objects.filter(
            weekly_shop_summary=weekly_shop_summary
            )

        weekly_overheads = models.WeeklyOverhead.objects.filter(
            weekly_shop_summary=weekly_shop_summary
            )

        return {'weekly_sales': weekly_sales, 'weekly_overheads': weekly_overheads}


class WeeklyImportDropView(generic.TemplateView):
    template_name = 'shops/weekly_imports_all.html'

    def get_context_data(self, **kwargs):

        # Don't need this query below as the datepicker is used instead
        dates = models.WeeklyShopSummary.objects.all().values_list(
            'date', 
            flat=True
            ).distinct()

        shops = models.Shop.objects.all().values_list(
            'code', 
            flat=True
            ).distinct()

        return {'shops': shops, 'dates': dates}


class WeeklyImportDetailView(generic.TemplateView):
    template_name = 'shops/partials/weekly_imports_all_details.html'

    def get_context_data(self, **kwargs):
        # Getting the closest monday
        input_date = datetime.strptime(
            self.request.GET['chosen_date'],
            '%Y-%m-%d'
            ).date()
        monday = input_date - timedelta(days=input_date.weekday())
        weekly_shop_summary = models.WeeklyShopSummary.objects.get(
            shop=models.Shop.objects.get(code=self.request.GET['chosen_shop']),
                date=monday
            )

        weekly_sales = models.WeeklySale.objects.filter(
            weekly_shop_summary=weekly_shop_summary
            )

        weekly_overheads = models.WeeklyOverhead.objects.filter(
            weekly_shop_summary=weekly_shop_summary
            )

        return {'weekly_sales': weekly_sales, 'weekly_overheads': weekly_overheads}


def weekly_summary_upload(request):
    if request.method == 'POST':
        form = forms.WeeklySummaryForm(request.POST, request.FILES)
        if form.is_valid():
            with form.instance.upload.open() as input_file:
                fruit_data, overhead_data, shop_code, date_object \
                    = import_helpers.import_data(input_file)
                shop = models.Shop.objects.get(code=shop_code)
                form.instance.shop = shop
                form.instance.date = date_object
                form.save()
                fruit_data.apply(
                    import_helpers.create_sale_objects, 
                    axis=1, 
                    weekly_shop_summary=form.instance
                    )
                overhead_data.apply(
                    import_helpers.create_overhead_objects, 
                    axis=1, 
                    weekly_shop_summary=form.instance
                    )
                messages.info(request, 'File uploaded successfully')
            return HttpResponseRedirect(reverse('upload_summary'))
    else:
        form = forms.WeeklySummaryForm()
    return render(request, 'shops/weekly_summary_form.html', {'form': form})






