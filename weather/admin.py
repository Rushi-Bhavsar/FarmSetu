from django.contrib import admin
from .models import WeatherData


class WeatherAdmin(admin.ModelAdmin):
    list_display = ['id', 'region', 'weather_parameter']
    search_fields = ['region', 'weather_parameter']
    list_filter = ['weather_parameter', 'region']


admin.site.register(WeatherData, WeatherAdmin)
