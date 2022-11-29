from django.shortcuts import render
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
from django.db.models import Q, F, Avg, Max, Sum, Window, Subquery
from django.conf import settings
from datetime import datetime, date
import django.db.models.functions as functions
from shops import models

from bokeh import plotting
from bokeh import palettes
from bokeh import embed

import shops.forms as forms
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


def upload_data(request):
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
                import_helpers.create_all_objects(
                    fruit_data=fruit_data,
                    overhead_data=overhead_data,
                    weekly_shop_summary=form.instance
                )
                messages.info(request, 'File uploaded successfully')
            return HttpResponseRedirect(reverse('upload_data'))
    else:
        form = forms.WeeklySummaryForm()
    return render(request, 'shops/upload_data.html', {'form': form})


class SummaryReportView(generic.TemplateView):
    template_name = 'shops/summary_report.html'

    def get_context_data(self, *args, **kwargs):
        """
        New method using more Python methods and less Django querying. 
        Seems a bit smoother and faster, still need to investigate bit more 
        about django annotation with windows (branch part_3_1).
        """
        all_fruits = models.Fruit.objects.all().order_by('name')
        first_date = (
            models.WeeklyShopSummary.objects
            .order_by('date')
            .first()
            .date
        )
        start_date = first_date
        start_date = start_date - timedelta(days=start_date.weekday())
        last_date = (
            models.WeeklyShopSummary.objects
            .order_by('date')
            .last()
            .date
        )
        sale_data = (
            models.WeeklySale.objects
            .filter(weekly_shop_summary__date__gte=start_date)
            .annotate(revenue=F('units_sold')*F('price_per_unit'))
        )

        summary_cleaned = {}
        cur_date = start_date
        period_duration = timedelta(weeks=4)

        while cur_date < last_date:
            summary_cleaned[cur_date] = {}
            next_date = cur_date + period_duration
            duration_data = sale_data.filter(
                        weekly_shop_summary__date__gte=cur_date,
                        weekly_shop_summary__date__lt=next_date,
            )
            for fruit in all_fruits:
                total_revenue = (
                    duration_data
                    .filter(fruit=fruit)
                    .aggregate(Sum('revenue'))
                )
                summary_cleaned[cur_date][fruit.name] = \
                    total_revenue['revenue__sum']
            cur_date = next_date

        plot = plotting.figure()

        for i, fruit in enumerate(all_fruits):
            plot.line(
                x=list(range(len(summary_cleaned))),
                y=list(
                    summary_cleaned[period_date][fruit.name] 
                    for period_date in summary_cleaned.keys()
                ),
                legend_label=fruit.name,
                line_color=palettes.Category20_20[i]
            )
        plot_script, plot_div = embed.components(plot)

        return {
            'summary_cleaned': summary_cleaned,
            'all_fruits': all_fruits,
            'plot_script': plot_script,
            'plot_div': plot_div,
            }
