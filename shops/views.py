from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
# Create your views here.
from .models import City, Shop
from .forms import CityForm, ShopForm


def home(request):
    return render(request, 'shops/home.html')


class CityView(generic.ListView):
    template_name = 'shops/city.html'
    context_object_name = 'all_cities'

    def get_queryset(self):
        return City.objects.all()


class CityDetailView(generic.DetailView):
    model = City
    template_name = 'shops/citydetail.html'


class ShopView(generic.ListView):
    template_name = 'shops/shop.html'
    context_object_name = 'all_shops'

    def get_queryset(self):
        return Shop.objects.all()


class ShopDetailView(generic.DetailView):
    model = Shop
    template_name = 'shops/shopdetail.html'


def city_form(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_city = City(name=name)
            new_city.save()
            return HttpResponseRedirect(reverse('city'))
    else:
        form = CityForm()

    return render(request,'shops/cityform.html', {'form': form})


def shop_form(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            year_opened = form.cleaned_data['year_opened']
            new_shop = Shop(
                city=city,
                name=name,
                code=code,
                address=address,
                postcode=postcode,
                year_opened=year_opened,
            )
            new_shop.save()
            return HttpResponseRedirect(reverse('shop'))
    else:
        form = ShopForm()

    return render(request,'shops/shopform.html', {'form': form})