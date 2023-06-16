from django.db import models


class WeatherData(models.Model):
    region = models.CharField(max_length=50, blank=False, null=False)
    weather_parameter = models.CharField(max_length=50, blank=False, null=False)
    year = models.IntegerField(blank=True, null=True)
    jan = models.FloatField(max_length=20, blank=True, null=True)
    feb = models.FloatField(max_length=20, blank=True, null=True)
    mar = models.FloatField(max_length=20, blank=True, null=True)
    apr = models.FloatField(max_length=20, blank=True, null=True)
    may = models.FloatField(max_length=20, blank=True, null=True)
    jun = models.FloatField(max_length=20, blank=True, null=True)
    jul = models.FloatField(max_length=20, blank=True, null=True)
    aug = models.FloatField(max_length=20, blank=True, null=True)
    sep = models.FloatField(max_length=20, blank=True, null=True)
    oct = models.FloatField(max_length=20, blank=True, null=True)
    nov = models.FloatField(max_length=20, blank=True, null=True)
    dec = models.FloatField(max_length=20, blank=True, null=True)
    win = models.FloatField(max_length=20, blank=True, null=True)
    spr = models.FloatField(max_length=20, blank=True, null=True)
    sum = models.FloatField(max_length=20, blank=True, null=True)
    aut = models.FloatField(max_length=20, blank=True, null=True)
    ann = models.FloatField(max_length=20, blank=True, null=True)

