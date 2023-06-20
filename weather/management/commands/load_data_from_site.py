import logging
from django.core.management.base import BaseCommand
from weather.utils.get_weather_data import get_region_wise_data, WeatherData


class Command(BaseCommand):
    help = 'To Load Data from Website.'

    def add_arguments(self, parser):
        parser.add_argument('--load_data', type=str, help='Parameter that will decide to load the data or not')

    def handle(self, *args, **kwargs):
        if kwargs['load_data'] == 'load':
            WeatherData.objects.all().delete()
            get_region_wise_data()
            self.stdout.write(f"Data Loading completed.")
        else:
            self.stdout.write(f"Data will not be loaded. Pass input parameter as 'load'")

