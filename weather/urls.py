from rest_framework import routers
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import WeatherViewSet


router = DefaultRouter()
router.register('weather', WeatherViewSet, basename='Weather')

urlpatterns = router.urls

