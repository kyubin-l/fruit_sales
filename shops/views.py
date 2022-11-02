from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

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
            form.save()
            return HttpResponseRedirect(reverse('city_list'))
    else:
        form = CityForm()

    return render(request,'shops/cityform.html', {'form': form})


def shop_form(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shop_list'))
    else:
        form = ShopForm()

    return render(request,'shops/shopform.html', {'form': form})