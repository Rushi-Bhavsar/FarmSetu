from django.shortcuts import render
from rest_framework import viewsets
from .models import WeatherData
from .serializer import WeatherSerializer


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all()[:10]
    serializer_class = WeatherSerializer
