from rest_framework import serializers
from .models import WeatherData


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'
