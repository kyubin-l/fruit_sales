from django.shortcuts import render
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse, reverse_lazy

import shops.models as models
from .forms import CityForm, ShopForm


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
    form_class = ShopForm
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
    form_class = ShopForm
    template_name = 'shops/shop_update_form.html'
    success_url = reverse_lazy('shop_list')
