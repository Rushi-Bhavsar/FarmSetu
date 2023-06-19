from rest_framework import routers
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WeatherViewSet, RegionParamData, RegionYearTemperature, GetRegionInfo, GetData, Get2data, Fetchdata


router = DefaultRouter()
router.register('weather', WeatherViewSet, basename='Weather')

urlpatterns = [
    path('region_param_details/', RegionParamData.as_view()),
    path('region_temp_details/', RegionYearTemperature.as_view()),
    path('get_region_info/', GetRegionInfo.as_view()),
    path('get_data/', GetData.as_view()),
    path('Get2data/', Get2data.as_view()),
    path('Fetchdata/', Fetchdata.as_view())
]
urlpatterns += router.urls

