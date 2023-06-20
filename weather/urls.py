from rest_framework import routers
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WeatherViewSet, RegionParamData, RegionYearTemperature, GetRegionInfo, RegionWeatherParameter, \
    WeatherParameterYear, RegionYear


router = DefaultRouter()
router.register('weather', WeatherViewSet, basename='Weather')

urlpatterns = [
    path('region_param_details/', RegionParamData.as_view()),
    path('region_temp_details/', RegionYearTemperature.as_view()),
    path('get_region_info/', GetRegionInfo.as_view()),
    path('region_weather_param/', RegionWeatherParameter.as_view()),
    path('weather_param_year/', WeatherParameterYear.as_view()),
    path('region_year/', RegionYear.as_view())
]
urlpatterns += router.urls

