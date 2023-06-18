from rest_framework import routers
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WeatherViewSet, RegionParamData, RegionYearTemperature


router = DefaultRouter()
router.register('weather', WeatherViewSet, basename='Weather')

urlpatterns = [
    path('region_param_details/', RegionParamData.as_view()),
    path('region_temp_details/', RegionYearTemperature.as_view())
]
urlpatterns += router.urls

