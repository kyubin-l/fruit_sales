"""fruit_sales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import shops.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', shops.views.HomeView.as_view(), name='home'),
    path('city/', shops.views.CityView.as_view(), name='city_list'),
    path('city/<int:pk>/', shops.views.CityDetailView.as_view(), name='citydetail'),
    path('shop/', shops.views.ShopView.as_view(), name='shop_list'),
    path('shop/<int:pk>/', shops.views.ShopDetailView.as_view(), name='shopdetail'),
    path('cityform/', shops.views.CityCreateView.as_view(), name='create_city'),
    path('shopform/', shops.views.ShopCreateView.as_view(), name='create_shop'),
    path('<int:pk>/deletecity/', shops.views.CityDeleteView.as_view(), name='delete_city'),
    path('<int:pk>/updatecity/', shops.views.CityUpdateView.as_view(), name='update_city'),
    path('<int:pk>/deleteshop/', shops.views.ShopDeleteView.as_view(), name='delete_shop'),
    path('<int:pk>/updateshop/', shops.views.ShopUpdateView.as_view(), name='update_shop'),
    path('weekly_import/', shops.views.WeeklyImportYearView.as_view(), name='weekly_import_yearview'),
    path(
        'weekly_import/<int:year>/',
        shops.views.WeeklyImportMonthView.as_view(), 
        name='weekly_import_monthview'
    ),
    path(
        'weekly_import/<int:year>/<int:month>/', 
        shops.views.WeeklyImportWeekView.as_view(), 
        name='weekly_import_weekview'
    ),
    path(
        'weekly_import/<int:year>/<int:month>/<int:week>/', 
        shops.views.WeeklyImportShopView.as_view(), 
        name='weekly_import_shopview'
    ),
    path(
        'weekly_import/<int:year>/<int:month>/<int:week>/<str:shopcode>', 
        shops.views.WeeklyImportShopDetail.as_view(), 
        name='weekly_import_shopdetail'
    ),
    path(
        'weekly_import_details/',
        shops.views.WeeklyImportDropView.as_view(),
        name='weekly_views'
    ),
    path(
        'weekly_import_details/show/',
        shops.views.WeeklyImportDetailView.as_view(),
        name='show_details'
    )
]
